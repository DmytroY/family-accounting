# FAMILY ACCOUNTING application

## What is it?
It is family financial accounting and bookkeeping application

## Main technologies used in the project:
- Django framework
- PostgreSQL
- Docker
- Gunicorn

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

## REMARKS
### Mooving from sqlite to PostgreSQL

DATABASES block in settings.py secure automatic fallback to local SQLite in case of DATABASE_URL env var not configured.

1. Use Django ORM exports to get data from SQLite:
```
python3 family_acc/manage.py dumpdata --natural-foreign --natural-primary --exclude auth.permission --exclude contenttypes > data.json
```
1. Set environment variable DATABASE_URL as PostgreSQL connection string. 
1. Create identical schema on PostgreSQL via Django migrations ```python family_acc/manage.py migrate```
1. Import data:
```python3 family_acc/manage.py loaddata data.json```


If you prefer do not import data admin user should be created manualy:
```python family_acc/manage.py createsuperuser```

### Secrets
During development secrets was stored in **secrets.py** in same directory with settings.py, in format:
```
SECRET_K = '...............'
USER = '.....'
PASSWORD = '...........'
```
Proper secret storage (env vars or secret management system) should be used for production.

### Deployment on Ubuntu server

I deploy on Ubuntu server and forward port to interned with [ngrok API Gateway](https://ngrok.com/).
#### Instaling from github
```
git clone https://github.com/DmytroY/family-accounting.git
cd family-accounting
```

#### Preparing environment.
Using venv is recomended.
```
python3 -m venv venv
source venv/bin/activate
```
We will keep next secrets as environment variables:
1. DJANGO_SECRET_KEY - Used for cryptographic signing in Django,
1. DJANGO_EMAIL_HOST_USER - host email for ending password recovery link
1. DJANGO_EMAIL_HOST_PASSWORD - password to the host email, in case of gmail it generates in [App passwords management](myaccount.google.com/apppasswords)
1. DATABASE_URL - Database connection string. If absent application fallback to local SQLite.

with online generator or in Python console generate secret key for django
```
import secrets
print(secrets.token_urlsafe(50))
```
add to ~/.bashrc or ~/.bash_profile strings with django secret key, host email and email password:
```
 export DJANGO_SECRET_KEY='generated secret key'
 export DJANGO_EMAIL_HOST_USER='email'
 export DJANGO_EMAIL_HOST_PASSWORD='email password'
 export DATABASE_URL='postgresql://neondb_owner:....@.....eu-central-1.aws.neon.tech/neondb?sslmode=require'
```
apply it with `source ~/.bashrc` and check with `echo $DJANGO_SECRET_KEY`


#### migrate DB and create superuser
```
python3 family_acc/manage.py migrate
python3 family_acc/manage.py createsuperuser
```

#### collectstatic
```
python3 family_acc/manage.py collectstatic
```

#### Run Gunicorn
from root directory of project(family-accounting) run gunicorn:

```
gunicorn --pythonpath family_acc family_acc.wsgi
```
[ngrok](ngrok.com) can be used to forward port to interned

```
ngrok http 8000 --url <yuor public ngrok domain>
```

Note! do tot forget to add yuor public ngrok domain to CSRF_TRUSTED_ORIGINS in settings.py

### Deployment in container
* Create .env file in root directory near Dockerfile. List there environment variables without quotes:
```
DJANGO_SECRET_KEY=generated_secret_key
DJANGO_EMAIL_HOST_USER=some@email.com
DJANGO_EMAIL_HOST_PASSWORD=email password spases are OK
DATABASE_URL=postgresql://neondb_owner:....
```
* build an image `docker build -t family-accounting-app .`
* run container `docker run --env-file .env -p 8000:8000 family-accounting-ap`

Note. No need in next steps in case we will use existing DB, we used before with thes app

* find container_id with `docker ps`
* run the migrations `docker exec -it <container_id> python3 family_acc/manage.py migrate`
* create superuser `docker exec -it <container_id> python3 family_acc/manage.py createsuperuser`

### How to
#### Translation: 
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