from django.apps import apps
import os, json
from openai import OpenAI
from pgvector.django import CosineDistance
from .models import UIDocumentationChunk
from groq import Groq
from django.db import connection

def generate_ai_system_prompt():
    # Project's core business logic
    prompt = (
        "You are a concise financial assistant for a family accounting app. "
        "IMPORTANT: Provide only short, high-level summaries. Do not provide "
        "detailed breakdowns or long explanations unless specifically asked.\n\n"
        "Data Structure (Star-scheme): Income is positive, expenses are negative.\n"
        "Current Schema:\n"
    )
    
    # Programmatically inspect models to get actual DB table and column names
    app_config = apps.get_app_config('transactions')
    for model in app_config.get_models():
        # Retrieve actual PostgreSQL table name (e.g., transactions_transaction)
        prompt += f"- Table: {model._meta.db_table}\n"
        for field in model._meta.fields:
            # Retrieve actual column name in DB
            prompt += f"  * Column: {field.column} ({field.get_internal_type()})\n"
            
    return prompt

def classify_intent(client: Groq, user_query: str) -> str:
    """Classifies user query into GENERAL, DOCUMENTATION, DATA or COMMAND
    and extracts specific command actions."""
    classifier_prompt = (
        "Analyze the user message and classify it into exactly one category:\n"
        "1. GENERAL: Greetings, small talk, general financial advice.\n"
        "2. DOCUMENTATION: Questions about how to use the app, UI, navigation, or API specs.\n"
        "3. DATA: Questions about specific account balances, transactions, spending, or income.\n"
        "4. COMMAND: Direct requests to perform session/app controls.\n\n"
        "Supported actions for COMMAND intent:\n"
        "- 'CLEAR_HISTORY': Request to clear, reset, or delete chat history.\n"
        "- 'SUMMARIZE_CHAT': Request to summarize, recap, or outline the current conversation.\n"
        "- 'EXPORT_CHAT': Request to export, download, or save the conversation.\n"
        "- 'UNKNOWN': Command is unrecognized.\n\n"
        "Respond ONLY with a JSON object in this schema:\n"
        '{\n'
        '  "intent": "GENERAL" | "DOCUMENTATION" | "DATA" | "COMMAND",\n'
        '  "action": "CLEAR_HISTORY" | "SUMMARIZE_CHAT" | "EXPORT_CHAT" | "UNKNOWN" | null\n'
        '}'
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