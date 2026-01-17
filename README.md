# FAMILY ACCOUNTING application

## What is it?
It is family financial accounting and bookkeeping application

## Main technologies used in the project:
- Django framework
- SQL database

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
1. Use Django ORM exports to get data from SQLite:
```
python3 family_acc/manage.py dumpdata --natural-foreign --natural-primary --exclude auth.permission --exclude contenttypes > data.json
```
1. Create identical schema on PostgreSQL via Django migrations.
1. Import data:
```
python3 family_acc/manage.py loaddata data.json
```

### Secrets
During development secrets was stored in **secrets.py** in same directory with settings.py, in format:
```
SECRET_K = '...............'
USER = '.....'
PASSWORD = '...........'
```
Proper secret storage (env vars or secret management system) should be used for production.

### Deployment
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
2. DJANGO_EMAIL_HOST_USER - host email for ending password recovery link
3. DJANGO_EMAIL_HOST_PASSWORD - password to the host email, in case of gmail it generates in [App passwords management](myaccount.google.com/apppasswords)

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


### How to
* Translation
in templates:
 {% load i18n %},
{% blocktrans %}text to translate{% endblocktrans %}, {% trans "text to translate" %}
in vievs:
from django.utils.translation import gettext as _
context = {'data': _("text to translate")}

Generate .po files for each specific language:
'''
python3 family_acc/manage.py makemessages -l uk -i venv
'''
edit  .po files, Run the compile command
'''
python3 family_acc/manage.py compilemessages -l uk -i venv
'''

### To-Do

* filter transactions by account
* android app
* reports