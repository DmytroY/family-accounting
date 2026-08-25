# FAMILY ACCOUNTING application

## What is it?
It is family financial accounting and bookkeeping application

## Main technologies used in the project:
- Django framework
- PostgreSQL with pgvector extention, https://neon.com/ based
- Docker
- Gunicorn
- LLM, https://groq.com/ based
- Embedding model, MS Azure AI based

## Data structure
Star-scheme used for keeping data. Fact table and corresponding Django models class **Transaction** contains historical financial  records complemented by dimension tables/Django models classes:
- **User**, user profile includes family fild which allows separate different families bookkeeping
- **Currency** i.e. USD, EUR, other.
- **Account** i.e. Cash, Credit card, Deposit...
- **Category**, can be income category like "Salary" or expence category like "Entertiment" or both like "Transfer between accounts"

Income transactions have positive amounts in **Transaction** table, expences have negative amounts.

## Project folders structure
- **documentation** folder which includes:
  - API specifications,
- **family_acc** folder which includes Django applications and related resourses:
  - **family_acc** - default application, home folder for settings.py
  - **members** - application for user management
  - **transactions** - application for financial transactions, currency, financial accounts and income/expence categories management
  - **tests** folder which includes unit tests, unit integration tests, API tests.
  - **templates** contains high level html templates like global layout template
  - **staticfiles** contains css and js used during development
  - **productionfiles** here will be collected staticfiles during release

## Environment variables used in the project
1. DJANGO_SECRET_KEY - Used for cryptographic signing in Django,
1. DJANGO_EMAIL_HOST_USER - host email for ending password recovery link
1. DJANGO_EMAIL_HOST_PASSWORD - password to the host email, in case of gmail it generates in [App passwords management](myaccount.google.com/apppasswords)
1. DATABASE_URL - Database connection string. If absent application fallback to local SQLite.
1. GROQ_API_KEY - https://groq.com/ API key
1. OPEN_AI_ENDPOINT - Azure embedded model endpoint
1. OPEN_AI_API_KEY - Azure embedded model API key
1. OPEN_AI_EMBEDDING_DEPLOYMENT  - Azure embedded model development name


## Deployment in container
* Create .env file in root directory near Dockerfile. List all environment variables without quotes similar to:
```
DJANGO_SECRET_KEY=dkn342ldma;q$@fama;adkey
```
* build an image `docker build -t family-accounting-app .`
* run container `docker run --env-file .env -p 8000:8000 family-accounting-ap`

Note. No need in next steps in case we will use existing DB, we used before with thes app

* find container_id with `docker ps`
* run the migrations `docker exec -it <container_id> python3 family_acc/manage.py migrate`
* create superuser `docker exec -it <container_id> python3 family_acc/manage.py createsuperuser`

## Deployment on Google Run
- Create secterets in Google Cloud Secret Manager.
- Enable the Compute Engine API.
- Grant Compute Engine access to the secrets - add default compute engine as principal with  Secret Manager Secret Accessor role.
- Greate repo in GC Artifact Registry.
- Tag properly and push docker image to GC Artifact Registry.
- In Google Cloud Run create new deployment from container. Do not forget in security management:
1. sets environment variables 
ALLOWED_HOSTS as external url of this app run without "https://" prefix and
CSRF_TRUSTED_ORIGINS as external url of this app run with "https://" prefix.
2. map DATABASE_URL, DJANGO_SECRET_KEY, DJANGO_EMAIL_HOST_USER and DJANGO_EMAIL_HOST_PASSWORD to values from Google Cloud Secret Manager
- Deploy

## How to
### Translation: 
in templates:
 {% load i18n %},
{% blocktrans %}text to translate{% endblocktrans %}, {% trans "text to translate" %}

in vievs:
from django.utils.translation import gettext as _
context = {'data': _("text to translate")}

Generate .po files for each specific language:
```
python3 family_acc/manage.py makemessages -l uk -i venv
```

edit  .po files, Run the compile command
```
python3 family_acc/manage.py compilemessages -l uk -i venv
```

---------------------------------------------------------------------
# AI instruments

After simple AI chat was implemented on the site I desided to extend it ability with RAG grounded to document **UI_specification.md** which describe site UI.
Components description:
1. groq.com API as core LLM
1. pgvector extention for vector DB in PostgreSQL on [neon.tech](https://neon.com/docs/introduction)
1. embedding model **text-embedding-3-small** on Azure OpenAI. The model default size is 1536 dimention but I progrmmaticaly decrease dimentions to 512 to speeds up retrieval performance, cuts RAM usage and vector storage in 3 times.
For using Azure embedding model do not forget deploy embedding model instance in Azure and add environment variables
- OPEN_AI_ENDPOINT
- OPEN_AI_API_KEY
- OPEN_AI_EMBEDDING_DEPLOYMENT
to .env file.

I wrote custom command which can be used to generate vector DB from markdown documents:
``` 
python family_acc/manage.py ingest_docs documentation/general_info.md --category general
```
choose category:
- **ui** when ingest documentation/UI_specification.md, 
- **api** when ingest documentation/API_specification.md, 
- **general**  when ingest documentation/general_info.md.
those .md files can be updated and then re-ingested.
