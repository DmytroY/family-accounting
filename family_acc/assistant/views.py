from django.shortcuts import render

import json, os
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from groq import Groq
from .utils import generate_ai_system_prompt, retrieve_documentation_context, classify_intent, execute_read_only_sql

_CACHED_AI_SYSTEM_PROMPT = None

def get_ai_system_prompt():
    global _CACHED_AI_SYSTEM_PROMPT
    if _CACHED_AI_SYSTEM_PROMPT is None:
        # This will only execute once, on the very first chat request
        _CACHED_AI_SYSTEM_PROMPT =(
            "You are a concise financial assistant for a family accounting app. "
            "IMPORTANT: Provide only short, high-level summaries. Do not provide "
            "detailed breakdowns or long explanations unless specifically asked.\n")
    return _CACHED_AI_SYSTEM_PROMPT

@login_required
def ai_chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # frontend JS data
            conversation_history = data.get('history', [])
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

            # latest user message
            user_query = ""
            if conversation_history:
                latest_msg = conversation_history[-1]
                if latest_msg.get('role') == 'user':
                    user_query = latest_msg.get('content', '')

            print(f"--- DY --- User query: {user_query}")

            # classify user intent and extract command if exist
            result = classify_intent(client, user_query)
            intent = result.get("intent", "GENERAL")
            action = result.get("action")
            print(f"--- DY --- Intent is {intent}, Action is {action}")

            # process user query accordingly to intent
            if intent == "DOCUMENTATION":
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
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="openai/gpt-oss-120b",
                    max_completion_tokens=750,
                    temperature=0.2  # Lower temperature for higher factual grounding
                )
                return JsonResponse({'reply': chat_completion.choices[0].message.content})

            if intent == "DATA":
                schema_prompt = generate_ai_system_prompt()
                
                # Prompt the LLM to generate a raw PostgreSQL query
                sql_generation_prompt = (
                        f"{schema_prompt}\n"
                        "TASK: Write a valid, raw PostgreSQL query (SELECT only) to answer the user request.\n"
                        "RULES:\n"
                        "1. Use the EXACT Table and Column names listed in the schema above.\n"
                        "2. Do NOT invent model/table names like 'Transaction' or 'Category'—use the prefixed db_table names.\n"
                        "3. Remember: Income is positive, expenses are negative (use ABS() or SUM() filtering appropriately).\n"
                        "4. Return ONLY the SQL query as raw text. Do NOT use markdown code blocks or quotes.\n"
                    )
                
                sql_messages = [
                    {"role": "system", "content": sql_generation_prompt},
                    {"role": "user", "content": user_query}
                ]
                
                sql_completion = client.chat.completions.create(
                    messages=sql_messages,
                    model="openai/gpt-oss-120b",
                    temperature=0.0
                )
                
                generated_sql = sql_completion.choices[0].message.content.strip()
                
                # Remove standard Markdown formatting if present
                if generated_sql.startswith("```"):
                    generated_sql = generated_sql.split("```")[1]
                    if generated_sql.startswith("sql"):
                        generated_sql = generated_sql[3:]
                    generated_sql = generated_sql.strip()

                # Execute the query
                try:
                    query_results = execute_read_only_sql(generated_sql)
                    print(f"---DY--- SQL query: {generated_sql}")
                    print(f"---DY--- query result: {query_results}")
                except Exception as sql_err:
                    return JsonResponse({'reply': f"Could not retrieve data: {str(sql_err)}"})

                # Step 3: Summarize the database results
                summary_system_prompt = (
                    "You are a concise financial assistant for a family accounting app.\n"
                    "Synthesize the following database query results to directly answer the user's question.\n"
                    "Provide short, high-level summaries without unnecessary detailed breakdowns."
                )
                
                summary_messages = [
                    {"role": "system", "content": summary_system_prompt},
                    {"role": "user", "content": f"User question: {user_query}\nSQL used: {generated_sql}\nQuery results: {json.dumps(query_results, default=str)}"}
                ]
                
                summary_completion = client.chat.completions.create(
                    messages=summary_messages,
                    model="openai/gpt-oss-120b",
                    max_completion_tokens=750,
                    temperature=0.3
                )
                
                return JsonResponse({'reply': summary_completion.choices[0].message.content})

            if intent == "COMMAND":
                if action == "CLEAR_HISTORY":
                    return JsonResponse({
                        'reply': "Chat history cleared.",
                        'action': "CLEAR_HISTORY"  # Frontend JS reads this to clear UI state
                    })
                else:
                    return JsonResponse({'reply': "I recognized a command request, but I am unable to perform that action."})

            # default genearal conversation
            messages = [{"role": "system", "content": get_ai_system_prompt()}]
            messages.extend(conversation_history)

            chat_completion = client.chat.completions.create(
                messages=messages,
                model="openai/gpt-oss-120b",
                max_completion_tokens = 750,
                temperature = 0.3
            )
            print(f"--- DY --- message to AI: {messages}")
            print(f"--- DY --- responce of AI: {chat_completion.choices[0].message.content}")

            return JsonResponse({'reply': chat_completion.choices[0].message.content})
               
        except Exception as e:
            print(f"AI Chat Error: {str(e)}") # Log error to server console
            return JsonResponse({'reply': f"Error: {str(e)}"}, status=500)
    return JsonResponse({'reply': "Invalid request"}, status=400)
