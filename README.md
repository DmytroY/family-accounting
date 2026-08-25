# Family Accounting Application

A Django-based financial accounting and bookkeeping application with multi-family support, AI-powered assistant, and comprehensive API.

**[GitHub Repository](https://github.com/DmytroY/family-accounting)** | **[Report Issues](mailto:dmitry.yakovenko@gmail.com)**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Data Structure](#data-structure)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
  - [Environment Setup](#environment-setup)
  - [Deployment with Docker](#deployment-with-docker)
  - [Deployment on Google Cloud Run](#deployment-on-google-cloud-run)
- [Usage Guide](#usage-guide)
  - [Account Setup](#account-setup)
  - [Recording Transactions](#recording-transactions)
  - [Data Import/Export](#data-importexport)
- [API Documentation](#api-documentation)
- [AI Assistant Features](#ai-assistant-features)
- [Internationalization](#internationalization)
- [Important Notes](#important-notes)

---

## Overview

Family Accounting is a simple yet powerful financial management system designed to help families track income and expenses across multiple accounts and currencies. The application supports:

- **Multi-family organization** - Keep separate financial records for different families
- **Multi-currency support** - Manage transactions in multiple currencies
- **Multi-user access** - Share family finances with family members
- **Intelligent AI assistant** - Get financial insights and answers through natural language conversation
- **RESTful API** - Programmatic access for integrations

---

## Key Features

### 💰 Financial Management
- Track income and expense transactions
- Manage multiple accounts (Cash, Credit Cards, Deposits, etc.)
- Support for multiple currencies
- Transaction categorization
- Detailed financial reporting

### 🤖 AI Assistant Module
The application includes an intelligent AI assistant with four operational modes:

1. **GENERAL** - Open-ended financial guidance and conversational queries
2. **DOCUMENTATION** - RAG-powered assistance using vector embeddings (knowledge base grounded in UI/API specs)
3. **DATA** - Natural language to SQL queries against your transaction database
4. **COMMAND** - Chat history management and UI lifecycle triggers

### 📊 Data Management
- Bulk import/export via CSV
- Automatic account/currency/category creation during import
- Starting balance configuration

### 🌍 Multi-language Support
- English, Czech, and Ukrainian
- Selectable language via UI

### 🔐 Security
- User authentication and authorization
- Family-based access control
- Email-based password recovery

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django |
| **Database** | PostgreSQL (with pgvector extension) |
| **Web Server** | Gunicorn |
| **Containerization** | Docker |
| **LLM Provider** | Groq API (gpt-oss-120b) |
| **Embedding Model** | Azure OpenAI (text-embedding-3-small, 512-dim) |
| **Vector Database** | PostgreSQL with pgvector |
| **Frontend** | HTML, CSS (31.2%), JavaScript (33.8%) |

**Language Composition:**
- JavaScript: 33.8%
- CSS: 31.2%
- Python: 27.7%
- HTML: 7.0%
- Dockerfile: 0.3%

---

## Data Structure

The application uses a **Star Schema** database design for financial data:

### Fact Table
- **Transaction** - Historical financial records with sign convention:
  - Income: Positive amounts (> 0)
  - Expenses: Negative amounts (< 0)

### Dimension Tables
- **User** - User profiles organized by family
- **Family** - Family grouping for multi-user access
- **Currency** - Supported currencies (USD, EUR, etc.)
- **Account** - Financial accounts (Cash, Credit Card, Deposit, etc.)
- **Category** - Transaction categories (Salary, Entertainment, Transfer, etc.)

### Design Benefits
- Unified reporting across transaction types
- Flexible categorization (income, expense, or both)
- Simple filtering by amount sign
- Automatic account balance updates

---

## Project Structure

```
family-accounting/
├── documentation/                 # Project documentation
│   ├── API_specification.md      # REST API endpoints and examples
│   ├── UI_specification.md       # Web interface documentation
│   └── general_info.md           # User guide and AI assistant docs
├── family_acc/                    # Django project root
│   ├── assistant/                # AI assistant
│   ├── family_acc/               # Main Django app & settings
│   ├── locale/                   # Czech and Ukrainian translations
│   ├── members/                  # User management & authentication
│   ├── transactions/             # Financial transactions & accounting
│   ├── templates/                # HTML templates
│   ├── staticfiles/              # CSS and JS (development)
│   ├── productionfiles/          # Collected static files (production)
│   └── tests/                    # Unit and integration tests
├── Dockerfile                     # Container configuration
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project metadata
└── README.md                    # This file
```

---

## Quick Start

### Environment Setup

#### Prerequisites
- Python 3.8+
- PostgreSQL 12+ (or SQLite for development)
- Docker & Docker Compose (for containerized deployment)

#### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DmytroY/family-accounting.git
   cd family-accounting
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations:**
   ```bash
   python family_acc/manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python family_acc/manage.py createsuperuser
   ```

7. **Start development server:**
   ```bash
   python family_acc/manage.py runserver
   ```

   Visit http://localhost:8000

### Deployment with Docker

#### Step 1: Prepare Environment

Create `.env` file in the root directory with required environment variables:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/family_accounting
GROQ_API_KEY=your-groq-api-key
OPEN_AI_ENDPOINT=your-azure-endpoint
OPEN_AI_API_KEY=your-azure-api-key
OPEN_AI_EMBEDDING_DEPLOYMENT=your-deployment-name
DJANGO_EMAIL_HOST_USER=your-email@gmail.com
DJANGO_EMAIL_HOST_PASSWORD=your-app-password
```

#### Step 2: Build and Run

```bash
# Build the Docker image
docker build -t family-accounting-app .

# Run container with existing database
docker run --env-file .env -p 8000:8000 family-accounting-app

# Or run with database initialization
docker run --env-file .env -p 8000:8000 family-accounting-app
docker exec -it <container_id> python family_acc/manage.py migrate
docker exec -it <container_id> python family_acc/manage.py createsuperuser
```

#### Step 3: Access Application

Visit `http://localhost:8000` in your browser.

### Deployment on Google Cloud Run

#### Step 1: Create Google Cloud Resources

1. Create secrets in Google Cloud Secret Manager:
   - `DJANGO_SECRET_KEY`
   - `DATABASE_URL`
   - `DJANGO_EMAIL_HOST_USER`
   - `DJANGO_EMAIL_HOST_PASSWORD`
   - `GROQ_API_KEY`
   - `OPEN_AI_API_KEY`
   - `OPEN_AI_ENDPOINT`
   - `OPEN_AI_EMBEDDING_DEPLOYMENT`
   - `CSRF_TRUSTED_ORIGINS`
   - `ALLOWED_HOSTS`

2. Enable required APIs:
   - Compute Engine API
   - Cloud Run API
   - Cloud Build API

3. Grant Compute Engine service account access:
   - Add service account as principal with Secret Manager Secret Accessor role

#### Step 2: Push Docker Image

1. Create repository in Artifact Registry:
   ```bash
   gcloud artifacts repositories create family-accounting \
     --repository-format=docker \
     --location=europe-west1
   ```

2. Build and push image:
   ```bash
   docker build -t europe-west1-docker.pkg.dev/PROJECT_ID/family-accounting/app:latest .
   docker push europe-west1-docker.pkg.dev/PROJECT_ID/family-accounting/app:latest
   ```

#### Step 3: Deploy to Cloud Run

1. Create new Cloud Run service from container image
2. Configure security settings:
   - Set `ALLOWED_HOSTS` to external URL (without https://)
   - Set `CSRF_TRUSTED_ORIGINS` to external URL (with https://)
3. Map environment variables from Secret Manager
4. Deploy

---

## Usage Guide

### Account Setup

Follow this sequence to set up your family finances:

1. **Register Account**
   - First family member registers independently
   - Receive email verification link
   - System creates a new family profile

2. **Add Family Members** (Optional)
   - Home page → Family Members → Add Member
   - Additional members access the same financial data
   - Required for shared family accounting

3. **Create Currency**
   - Transactions → Currencies → New
   - Enter 3-letter code (USD, EUR, etc.) and description
   - Save

4. **Create Accounts**
   - Transactions → Accounts → New
   - Name: (e.g., "My Cash", "Credit Card", "Deposit")
   - Currency: Select from created currencies
   - Initial Balance: Set starting balance (optional)
   - Accounts with the same name can use different currencies

5. **Create Categories**
   - Transactions → Categories → New
   - Name: (e.g., "Salary", "Food", "Transfer")
   - Select appropriate flags:
     - ✓ Use it for income (income transactions)
     - ✓ Use it for expense (expense transactions)
     - ✓ Both (for account transfers)
   - Save

6. **Add Transactions**
   - Transactions → New Income (or New Expense)
   - Enter date, account, amount, category, and optional remark
   - System automatically applies correct sign (+ income, - expense)

### Recording Transactions

#### Income Transaction
- Amount recorded as positive value
- Updates account balance by adding amount
- Use income-flagged categories only

#### Expense Transaction
- Amount recorded as negative value
- Updates account balance by subtracting amount
- Use expense-flagged categories only

#### Account Transfers
Create two transactions with equal amounts:
- Example: Withdraw $100 from credit card to cash
  1. Expense: -$100 on Credit Card (category: Transfer)
  2. Income: +$100 on Cash (category: Transfer)

### Data Import/Export

#### Export to CSV
1. Transactions → View all transactions
2. Apply date filter (optional)
3. Click "Download CSV"
4. CSV includes: Date, Account, Amount, Currency, Category, Remark

#### Import from CSV
1. Transactions → Upload CSV
2. Prepare CSV file with columns: `date, account_name, amount, currency_code, category_name, remark`
3. Amount: positive for income, negative for expenses
4. Upload file

**Auto-Creation During Import:**
- Missing currencies will be created automatically
- Missing accounts will be created automatically
- Missing categories will be created automatically
- Adjust account balances and category flags after import

---

## API Documentation

The application provides a comprehensive RESTful JSON API. See [API_specification.md](documentation/API_specification.md) for detailed documentation.

### Quick API Reference

#### Authentication
```bash
# Get API token
curl -X POST -d "username=<username>&password=<password>" \
  https://yourdomain.com/api/token/

# Response
{"token": "your-api-token-here"}
```

#### Create Transaction
```bash
curl -X POST \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-23",
    "account": 9,
    "amount": 100.50,
    "category": 1,
    "remark": "Your remark"
  }' \
  https://yourdomain.com/transactions/api/income_create/
```

#### Query Transactions
```bash
# All transactions
curl -H "Authorization: Token YOUR_TOKEN" \
  https://yourdomain.com/transactions/api/transactions/

# Filtered by date range
curl -H "Authorization: Token YOUR_TOKEN" \
  "https://yourdomain.com/transactions/api/transactions/?from=2025-12-01&to=2025-12-31"

# By account and currency
curl -H "Authorization: Token YOUR_TOKEN" \
  "https://yourdomain.com/transactions/api/transactions/?account=Cash&currency=USD"
```

See [API_specification.md](documentation/API_specification.md) for complete endpoint reference.

---

## AI Assistant Features

### Architecture

```
User Query
    ↓
POST /assistant/chat/
    ↓
Intent Classification
    ├→ GENERAL: Open-ended guidance
    ├→ DOCUMENTATION: RAG with vector embeddings
    ├→ DATA: Natural language to SQL
    └→ COMMAND: Chat management
    ↓
JSON Response
    ↓
Frontend Display
```

### Intent Types

#### 1. GENERAL Intent
- Open-ended financial guidance
- Conversational queries
- Greeting and help requests

#### 2. DOCUMENTATION Intent (RAG)
- Questions about application features
- UI navigation assistance
- API usage help
- Grounded in markdown documentation:
  - `UI_specification.md` - Interface guide
  - `API_specification.md` - API endpoints
  - `general_info.md` - System information

#### 3. DATA Intent
- Financial analysis questions
- Transaction queries
- Balance and spending reports
- Example: "How much did I spend on groceries in 2025?"

#### 4. COMMAND Intent
- `CLEAR_HISTORY` - Clear chat history
- `SUMMARIZE_CHAT` - Summarize conversation
- `EXPORT_CHAT` - Export chat transcript

### Using the AI Assistant

1. Navigate to: **Home → Chat** (or `/ai/chat/`)
2. Type your question or request
3. Assistant responds based on intent classification
4. Conversation history maintained during session

### Ingesting Documentation

Update AI knowledge base from markdown files:

```bash
# Ingest general information
python family_acc/manage.py ingest_docs documentation/general_info.md --category general

# Ingest UI documentation
python family_acc/manage.py ingest_docs documentation/UI_specification.md --category ui

# Ingest API documentation
python family_acc/manage.py ingest_docs documentation/API_specification.md --category api
```

### Technical Details

- **LLM:** Groq API (gpt-oss-120b for completions, gpt-oss-20b for intent classification)
- **Embeddings:** Azure OpenAI (text-embedding-3-small, 512 dimensions)
- **Vector Storage:** PostgreSQL with pgvector extension
- **Context:** Top-3 nearest document chunks via cosine similarity
- **Temperature:** 0.0 (DATA), 0.3 (DOCUMENTATION), 0.5 (GENERAL)

---

## Internationalization

The application supports multiple languages: **English**, **Czech**, **Ukrainian**.

### Using Translation in Templates

```django
{% load i18n %}

{% trans "Text to translate" %}
{% blocktrans %}Longer text to translate{% endblocktrans %}
```

### Using Translation in Views

```python
from django.utils.translation import gettext as _

context = {'message': _("text to translate")}
```

### Generating/Compiling Messages

```bash
# Generate .po files for Ukrainian
python family_acc/manage.py makemessages -l uk -i venv

# Edit .po files with translations

# Compile messages
python family_acc/manage.py compilemessages -l uk -i venv
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_SECRET_KEY` | ✓ | Django cryptographic signing key |
| `DATABASE_URL` | Optional | PostgreSQL connection string (uses SQLite if absent) |
| `DJANGO_DEBUG` | Optional | Set to False in production |
| `ALLOWED_HOSTS` | For production | Comma-separated allowed hosts |
| `CSRF_TRUSTED_ORIGINS` | For production | CSRF trusted origin URLs |
| `DJANGO_EMAIL_HOST_USER` | Optional | Email for password recovery |
| `DJANGO_EMAIL_HOST_PASSWORD` | Optional | Email app password (Gmail) |
| `GROQ_API_KEY` | For AI features | Groq API key from https://groq.com/ |
| `OPEN_AI_ENDPOINT` | For AI features | Azure OpenAI endpoint |
| `OPEN_AI_API_KEY` | For AI features | Azure OpenAI API key |
| `OPEN_AI_EMBEDDING_DEPLOYMENT` | For AI features | Azure embedding model deployment name |

---

## Important Notes

### ⚠️ Non-Commercial Use
- This system is provided **free of charge** for personal use
- Not intended for commercial applications

### 📌 Data Availability & Backup
- The developer does **not guarantee**:
  - Permanent data storage
  - System stability
  - Continuous uptime
- **Strongly recommended:** Regular backups via CSV export

### 🔒 Security Considerations
- All API requests require HTTPS in production
- Use secure environment variable management
- Regularly rotate API keys and tokens
- Keep dependencies updated

---

## Support & Contribution

### Report Issues
- Email: [dmitry.yakovenko@gmail.com](mailto:dmitry.yakovenko@gmail.com)
- GitHub Issues: [Open an issue](https://github.com/DmytroY/family-accounting/issues)

### Documentation
- [API Specification](documentation/API_specification.md) - REST API reference
- [UI Specification](documentation/UI_specification.md) - Web interface guide
- [General Info](documentation/general_info.md) - System overview and AI assistant guide

### Source Code
- Repository: https://github.com/DmytroY/family-accounting

---

## License

See [LICENSE](LICENSE) file for details.

---
