from django.apps import apps
import os, json, logging
from openai import OpenAI
from pgvector.django import CosineDistance
from .models import UIDocumentationChunk
from groq import Groq
from django.db import connection
from typing import Any, Dict, List, Optional
from transactions.models import Category

logger = logging.getLogger(__name__)

_CACHED_AI_SYSTEM_PROMPT = None

def strip_code_fence(text: str) -> str:
    if not text:
        return text
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```", 2)
        # parts[0] is empty, parts[1] may include language, parts[2] the rest
        inner = parts[1] if len(parts) == 2 else parts[1] + (parts[2] if parts[2] else "")
        # If language token present like "sql\nSELECT..."
        if inner.startswith("sql"):
            inner = inner[3:]
        return inner.strip()
    return text

def get_ai_system_prompt() -> str:
    global _CACHED_AI_SYSTEM_PROMPT
    if _CACHED_AI_SYSTEM_PROMPT is None:
        # This will only execute once, on the very first chat request
        # _CACHED_AI_SYSTEM_PROMPT =(
        #     "You are a concise financial assistant for a family accounting app. "
        #     "IMPORTANT: Provide only short, high-level summaries. Do not provide "
        #     "detailed breakdowns or long explanations unless specifically asked.\n")
        _CACHED_AI_SYSTEM_PROMPT =(
            " You're a cynical, witty, sarcastic financial assistant for a family accounting app." 
            " You answers short. You always try to slip a joke and some advice to spend less on alcohol and more on charity.\n")

    return _CACHED_AI_SYSTEM_PROMPT

def get_latest_user_message(history: List[Dict[str, Any]]) -> str:
    if not history:
        return ""
    latest = history[-1]
    if latest.get("role") == "user":
        return latest.get("content", "") or ""
    return ""

def generate_ai_system_prompt() -> str:
    # # Project's core business logic
    # prompt = (
    #     "Data Structure (Star-scheme): Income is positive, expenses are negative.\n"
    #     "Current Schema:\n"
    # )
    
    # # Programmatically inspect models to get actual DB table and column names
    # app_config = apps.get_app_config('transactions')
    # for model in app_config.get_models():
    #     # Retrieve actual PostgreSQL table name (e.g., transactions_transaction)
    #     prompt += f"- Table: {model._meta.db_table}\n"
    #     for field in model._meta.fields:
    #         # Retrieve actual column name in DB
    #         prompt += f"  * Column: {field.column} ({field.get_internal_type()})\n"
            
    # return prompt

    prompt = (
        "Data Structure (Star-scheme): Income is positive, expenses are negative.\n"
        "Current Schema:\n"
    )
    
    app_config = apps.get_app_config('transactions')
    for model in app_config.get_models():
        prompt += f"- Table: {model._meta.db_table}\n"
        for field in model._meta.fields:
            prompt += f"  * Column: {field.column} ({field.get_internal_type()})\n"

# Filter categories by the current user's family
    category_qs = Category.objects.all()
    if user and hasattr(user, 'profile'):
        family = getattr(user.profile, 'family', None)
        if family:
            category_qs = category_qs.filter(family=family)

    raw_categories = category_qs.values_list('name', flat=True).distinct()
    categories = [str(cat) for cat in raw_categories if cat is not None]

    prompt += f"\nAvailable Database Categories: {', '.join(categories)}\n"
    prompt += (
        "CRITICAL MAPPING RULE:\n"
        "1. Join category table when filtering by category name (category.id = transaction.category_id).\n"
        "2. Match user request concepts to the most relevant exact category name listed above.\n"
    )
    return prompt

def classify_intent(client: Groq, user_query: str) -> str:
    """Classifies user query into GENERAL, DOCUMENTATION, DATA or COMMAND
    and extracts specific command actions."""
    classifier_prompt = (
        "Analyze the user message and classify it into exactly one category:\n"
        "1. GENERAL: Question not related finance data records. Greetings, small talk, social chitchat (e.g., 'hello', 'how are you').\n"
        "2. DOCUMENTATION: Questions about this application, capabilities, features, how to use it," 
        " UI, navigation, or API specs (e.g., 'what can I do with this app?', 'how do I use this?').\n"
        "3. DATA: Questions about specific account balances, transactions, spending, or income.\n"
        "4. COMMAND: Direct requests to perform session/app controls.\n\n"
        "Supported actions for COMMAND intent:\n"
        "- 'CLEAR_HISTORY': Request to clear, reset, or delete chat history.\n"
        "- 'SUMMARIZE_CHAT': Request to summarize, recap, or outline the current conversation.\n"
        "- 'EXPORT_CHAT': Request to export, download, or save the conversation.\n"
        "- 'UNKNOWN': Command is unrecognized.\n\n"
        "Examples:\n"
        'User: "what can I do with this app?" -> {"intent": "DOCUMENTATION", "action": null}\n'
        'User: "hi there" -> {"intent": "GENERAL", "action": null}\n\n'
        "Respond ONLY with a JSON object in this schema:\n"
        "{\n"
        '  "intent": "GENERAL" | "DOCUMENTATION" | "DATA" | "COMMAND",\n'
        '  "action": "CLEAR_HISTORY" | "SUMMARIZE_CHAT" | "EXPORT_CHAT" | "UNKNOWN" | null\n'
        "}"
    )
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": classifier_prompt},
                {"role": "user", "content": user_query}
            ],
            model="openai/gpt-oss-20b",
            response_format={"type": "json_object"},
            temperature=0.0
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"intent": "GENERAL", "action": None}

def get_query_embedding(query_text: str) -> list[float]:
    """Generates 512-dimension vector embedding using Azure OpenAI."""
    client = OpenAI(
        base_url=os.getenv("OPEN_AI_ENDPOINT"),
        api_key=os.getenv("OPEN_AI_API_KEY"),
    )
    deployment_name = os.getenv("OPEN_AI_EMBEDDING_DEPLOYMENT")
    
    response = client.embeddings.create(
        input=query_text,
        model=deployment_name,
        dimensions=512
    )
    return response.data[0].embedding

def retrieve_documentation_context(user_query: str, top_k: int = 3) -> str:
    """Fetches top-k nearest documentation chunks from pgvector."""
    query_vector = get_query_embedding(user_query)
    
    # Query pgvector DB ordered by Cosine Distance
    chunks = UIDocumentationChunk.objects.order_by(
        CosineDistance('embedding', query_vector)
    )[:top_k]
    
    if not chunks:
        return ""
    
    # Concatenate chunk contents for LLM context
    context_blocks = []
    for chunk in chunks:
        header = f"--- Source: {chunk.source_file} ({chunk.title}) ---"
        context_blocks.append(f"{header}\n{chunk.content}")
        
    return "\n\n".join(context_blocks)

def execute_read_only_sql(sql_query):
    # Ensure query is strictly a SELECT statement
    clean_sql = sql_query.strip().rstrip(';')
    if not clean_sql.upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")
    
    with connection.cursor() as cursor:
        cursor.execute(clean_sql)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def handle_documentation(client: Groq, conversation_history: List[Dict[str, Any]], user_query: str) -> Dict[str, Any]:
    rag_context = retrieve_documentation_context(user_query, top_k=3)
    doc_system_prompt = (
        "You are an expert assistant for the Family Accounting application. "
        "Use ONLY the following retrieved documentation to answer the user's question. "
        "Formatting Rules:\n"
        "- Do NOT reuse markdown headers, dividers or formatters (e.g., #, -, *) directly from the retrieved context.\n"
        "- Present instructions using clean, numbered steps or bullet points.\n"
        "- Keep text concise and easy to scan.\n"
        "If the answer cannot be found in the context, clearly state that you don't know.\n\n"
        f"DOCUMENTATION CONTEXT:\n{rag_context}"
    )
    messages = [{"role": "system", "content": doc_system_prompt}]
    messages.extend(conversation_history)

    completion = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-oss-120b",
        max_completion_tokens=750,
        temperature=0.2,
    )
    return {"reply": completion.choices[0].message.content}

def handle_data(client: Groq, conversation_history: List[Dict[str, Any]], user_query: str) -> Dict[str, Any]:
    schema_prompt = generate_ai_system_prompt()

    sql_generation_prompt = (
        f"{schema_prompt}\n"
        "TASK: Write a valid, raw PostgreSQL query (SELECT only) to answer the user request.\n"
        "RULES:\n"
        "0. Check whether the user's request is unambiguous and complete "
        "1. Use the EXACT Table and Column names listed in the schema above.\n"
        "2. Do NOT invent model/table names like 'Transaction' or 'Category'—use the prefixed db_table names.\n"
        "3. Remember: Income is positive, expenses are negative (use ABS() or SUM() filtering appropriately).\n"
        "4. Return ONLY the SQL query as raw text. Do NOT use markdown code blocks or quotes.\n"
    )

    sql_messages = [
        {"role": "system", "content": sql_generation_prompt},
        {"role": "user", "content": user_query},
    ]

    sql_completion = client.chat.completions.create(
        messages=sql_messages,
        model="openai/gpt-oss-120b",
        temperature=0.0,
    )

    generated_sql = strip_code_fence(sql_completion.choices[0].message.content.strip())
    logger.debug(f"-- AI chat: Generated SQL: {generated_sql}")

    try:
        query_results = execute_read_only_sql(generated_sql)
        logger.debug(f"-- AI chat: query result: {query_results}")
    except Exception as sql_err:
        # Let the dispatcher create the JsonResponse
        raise RuntimeError(f"I identified your message as a request to operate on stored data, but: {sql_err}. Please try rewording your request.")

    summary_system_prompt = (
        "You are a concise financial assistant for a family accounting app.\n"
        "Synthesize the following database query results to directly answer the user's question.\n"
        "Provide short, high-level summaries without unnecessary detailed breakdowns."
        "Do not include information when it is not clearly known to be correct."
        "For example, if no currency was specified in the request, you should not include any currency notation in the response.\n"
        "If a user's question includes terms related to alcohol, restaurants, bars, or beer,"
        " add a touch of sarcasm and suggest they spend more on sports rather than on those things. "
    )

    summary_messages = [
        {"role": "system", "content": summary_system_prompt},
        {
            "role": "user",
            "content": f"User question: {user_query}\nSQL used: {generated_sql}\nQuery results: {json.dumps(query_results, default=str)}",
        },
    ]

    summary_completion = client.chat.completions.create(
        messages=summary_messages,
        model="openai/gpt-oss-120b",
        max_completion_tokens=750,
        temperature=0.3,
    )

    return {"reply": summary_completion.choices[0].message.content}

def handle_command(action: Optional[str]) -> Dict[str, Any]:
    if action == "CLEAR_HISTORY":
        return {"reply": "Chat history cleared.", "action": "CLEAR_HISTORY"}
    return {"reply": "I recognized a command request, but I am unable to perform that action."}

def handle_general(client: Groq, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    messages = [{"role": "system", "content": get_ai_system_prompt()}]
    messages.extend(conversation_history)
    completion = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-oss-120b",
        max_completion_tokens=750,
        temperature=0.3,
    )

    logger.debug("-- AI chat: response = {completion.choices[0].message.content}")
    return {"reply": completion.choices[0].message.content}