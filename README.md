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
python family_acc\manage.py dumpdata --natural-foreign --natural-primary --exclude auth.permission --exclude contenttypes > data.json
```
1. Create identical schema on PostgreSQL via Django migrations.
1. Import data:
```
python family_acc\manage.py loaddata data.json
```

### Secrets
During development secrets was stored in **secrets.py** in same directory with settings.py, in format:
```
SECRET_K = '...............'
USER = '.....'
PASSWORD = '...........'
```
Proper secret storage (env vars or secret management system) should be used for production.