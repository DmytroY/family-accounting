# Family Accounting System Guide

## Overview
This document provides instructions and guidelines for using the Family Accounting system, a simple and free application designed to help users track income and expenses across family accounts.

## Introduction
The system offers basic, essential functionality without unnecessary complexity. It allows users to manage shared family finances through a centralized dashboard.

## Registration and Account Setup
* **Family Grouping:** Financial records are structured around family units. Data stored within a family profile is accessible to all assigned members of that specific family.
* **Initial User:** The first family member registers independently and can subsequently create accounts for additional family members.
* **Email Verification:** Users must enter a valid email address during registration. The email is required to receive access restoration links in case of password loss.

## Recording Income and Expenses

To begin tracking transactions, follow this setup sequence:

1. **Create Currencies:** Define the currencies used for tracking transactions.
2. **Create Accounts:** 
   * Assign a currency to each account.
   * Accounts using different currencies can share the same name (e.g., "My cash (USD)" and "My cash (EUR)").
3. **Define Categories:**
   * Categories specify the type of transaction (e.g., "Salary", "Food", "Transfer between accounts").
   * Configure category usage by selecting the appropriate checkboxes:
     * **Use it for income**
     * **Use it for expense**
     * **Use for both** (e.g., for transfers)
4. **Create Financial Transactions:**
   * Once an account, currency, and category exist, new income or expense transactions can be added.
   * **Transfers Between Accounts:** Transfers require two transactions of equal amounts:
     * Example: Withdrawing cash from an ATM requires one expense transaction on the "Card" account and one income transaction on the "Cash" account.
   * **Transaction Signs:** Income is recorded as a positive value and expenses as a negative value. Sign assignment is handled automatically by the system based on the selected transaction type (income or expense).

## Data Import and Export (CSV)
* Users can import and export data using CSV files available on the relevant system pages.
* **Automatic Creation:** Importing transactions automatically creates missing currencies, accounts, and categories. Manual pre-creation of these items prior to import is not required.
* **Post-Import Maintenance:**
  * Adjust and set the correct starting balances for automatically created accounts.
  * Review created categories and uncheck "use for income" or "use for expense" as needed to refine transaction input options.

## Disclaimers and Operational Notes
* **Non-Commercial Product:** The system is provided free of charge for personal use.
* **Liability & Availability:** The developer does not guarantee permanent data storage, system stability, or continuous uptime.
* **Data Backups:** Regular data backups via CSV file export are strongly recommended to prevent potential data loss.

## Contact and Source Code
* **Source Code Repository:** https://github.com/DmytroY/family-accounting
* **Feedback & Support:** Suggestions and inquiries can be sent to [dmitry.yakovenko@gmail.com](mailto:dmitry.yakovenko@gmail.com).


# AI Assistant Module

## System Overview

The **AI Assistant** is a core component of the `family-accounting` application. It acts as an intelligent conversational interface capable of understanding multi-modal user queries. When a request is received, the assistant automatically classifies the user's intent and routes it through one of four specialized execution pipelines:

1. **GENERAL**: Open-ended conversational interface and financial guidance.
2. **DOCUMENTATION**: Retrieval-Augmented Generation (RAG) powered by vector embeddings to answer questions about application features, UI, and API specifications.
3. **DATA**: Text-to-SQL interface translating natural language queries into read-only PostgreSQL queries against the underlying transaction database.
4. **COMMAND**: Session management and UI lifecycle triggers (e.g., clearing chat history).

---

## Architecture Blueprint
Client / Frontend JS  -> (POST /ai-chat ) -> ai_chat_view (Django) -> classify_intent procedure ->
- option 1. GENERAL intent -> System Prompt, LLM Response.
- option 2. DOCUMENTATION intent -> pgvector Embeddings, RAG Contex, LLM Response.
- option 3. DATA intent -> Text-to-SQL, ReadOnly SQL Exec, LLM Response.
- option 4. COMMAND -> action processing bassed on defined action.

-> JsonResponse Output to Frontend.

## Intent Processing Pipelines

### 1. Intent Classification

Every incoming message is passed to `classify_intent()`, which uses a lightweight model (`openai/gpt-oss-20b`) with a forced JSON response structure (`response_format={"type": "json_object"}`).

* **System Prompt:** Rules to evaluate intent into `GENERAL`, `DOCUMENTATION`, `DATA`, or `COMMAND`.
* **Output Schema:**
  ```json
  {
    "intent": "GENERAL" | "DOCUMENTATION" | "DATA" | "COMMAND",
    "action": "CLEAR_HISTORY" | "SUMMARIZE_CHAT" | "EXPORT_CHAT" | "UNKNOWN" | null
  }

###  2. Pipeline Execution Details
#### A. DOCUMENTATION Pipeline (RAG)
Used when users ask about application features, UI usage, navigation, or APIs.
Embedding Generation: Converts user prompt into a 512-dimensional vector using Azure OpenAI (get_query_embedding).
Vector Search: Performs cosine distance similarity search against UIDocumentationChunk stored in PostgreSQL using pgvector.
Context Assembly: Fetches top k=3 nearest document chunks.
LLM Completion: Sends context and message history to openai/gpt-oss-120b at temperature=0.3 to ensure factual grounding.

#### B. DATA Pipeline (Text-to-SQL)
Used when users query financial figures, balances, spending trends, or transactions.
Schema Inspection: Programmatically inspects Django's transactions app models via generate_ai_system_prompt(). It outputs exact database table names (model._meta.db_table) and SQL column names (field.column).
SQL Generation Step: LLM (temperature=0.0) turns the prompt into a raw PostgreSQL SELECT query.
Safe Execution: Executes the query using execute_read_only_sql(), which strips whitespace and verifies the string starts with SELECT before opening a cursor.
Summary Step: Passes the SQL execution result set (query_results) back to the LLM to format a natural language summary.

#### C. COMMAND Pipeline
Used for frontend state modifications and controls.
Supported Actions:
CLEAR_HISTORY: Returns JSON payload with action: "CLEAR_HISTORY", signaling frontend JS to reset UI history.
SUMMARIZE_CHAT / EXPORT_CHAT / UNKNOWN: Formatted system fallback notices.

#### D. GENERAL Pipeline
Used for open-ended financial guidance, greetings, and generic questions.
Execution: System prompt generated from dynamic app metadata combined with full conversation_history sent to openai/gpt-oss-120b (temperature=0.5).
Utility Functions & Database Schema Inspection
generate_ai_system_prompt()
Dynamically constructs database schema metadata by inspecting registered models under the transactions Django app. Cached in memory (_CACHED_AI_SYSTEM_PROMPT) to optimize repeated requests.
Convention Rules Encoded in Prompt:
Star-schema database layout.
Income amounts are recorded as positive numeric values (> 0).
Expense amounts are recorded as negative numeric values (< 0).
execute_read_only_sql(sql_query)
Executes raw SQL directly on the default PostgreSQL connection.
Security Controls: Strips trailing semicolons and raises a ValueError if the statement does not begin with SELECT.
Return Format: Returns a list of dictionaries mapping column names to row values: [{"column_name": value, ...}].
### API Reference & Interface Specification
#### Endpoint:
 POST /assistant/chat/ (Name: ai_chat_view)

#### Requirements
- Authentication: Required (@login_required).
- Request Content-Type: application/json

#### Request Payload
```
JSON
{
  "history": [
    {
      "role": "user",
      "content": "How much did I spend on groceries in 2025?"
    }
  ]
}
```

#### Response Formats
Standard Response (GENERAL, DOCUMENTATION, DATA)
```
JSON
{
  "reply": "In 2025, your total expenses for groceries amounted to $1,245.50."
}
```
#### Command Execution Response (COMMAND)
```
JSON
{
  "reply": "Chat history cleared.",
  "action": "CLEAR_HISTORY"
}
```
#### Error Response (HTTP 500)
```
JSON
{
  "reply": "Error: <error_message_details>"
}
```