# Family accounting API documentation

API is RESTful JSON-based API. All requests are made to the endpoint containing .../api/. All requests must be secure, i.e. https, not http.

In the examples below all requests have http://localhost:8000 or http://127.0.0.1:8000 which is related to the test development server. Note that in the production proper host shoud be used.

## 1. Obtaining and regenerating API token
Only requests of authorized users will be processed by API. As first step username and password should be used to obtain user's API token authentication token:

`curl -X POST -d "username=<your_username>&password=<your_password>" "<site_URL>/api/token/"`

for example during local run:
```
curl -X POST -d "username=api_user&password=somepass" http://127.0.0.1:8000/api/token/
```
it returns:
```
{"token":"df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6"}
```

Alternatively build-in Django management tool can be used to obtain token: `python family_acc/manage.py drf_create_token <username>`

Note, that repeating those commands do not recreate token. If you need regenerate token use next API request:

```
curl -X POST -H "Authorization: Token <OLD_TOKEN>" http://localhost:8000/api/token/regenerate/
```

As soon as you have valid token you can use it for authentication of API requests.



## 2. Users and Family

### 2.1. Self registration
User can register itself, in this case new family identity will be created and this user will be first member of the family (Powershell sintax):
```
>curl.exe -X POST http://127.0.0.1:8000/members/api/register/ -H "Content-Type: application/json" --data-raw "{\"first_name\":\"API_user_fname\",\"last_name\":\"API_user_lname\",\"email\":\"apiu@u.com\",\"username\":\"api_user\",\"password1\":\"somepass\",\"password2\":\"somepass\"}"

{"success":"user created"}
```

let's get authentication token of this user:
```
> curl -X POST -d "username=api_user&password=somepass" http://127.0.0.1:8000/api/token/

{"token":"df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6"}
```
### 2.2. Adding new member of to the family
We can use existing user token for create oter users in the same family(Powershell sintax):
```
curl.exe -X POST -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/members/api/create/ -H "Content-Type: application/json" --data-raw "{\"first_name\":\"API_user_fname2\",\"last_name\":\"API_user_lname2\",\"email\":\"apiu2@u.com\",\"username\":\"api_user2\",\"password1\":\"somepass2\",\"password2\":\"somepass2\"}"

{"success":"user created"}
```

### 2.3. List of users in the family
Using next endpoint with authorisation token of one of member of the family will returns list of users in this family:

```
curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/members/api/members/

[{"id":22,"username":"api_user","email":"apiu@u.com"},{"id":23,"username":"api_user2","email":"apiu2@u.com"}]
```

## 3. Financial transactions
Star-scheme used for keeping data. Fact table and corresponding Django models class **Transaction** contains historical financial  records complemented by dimension tables/Django models classes:
- **User**, user profile includes family field which allows separate different families bookkeeping
- **Currency** i.e. USD, EUR, other.
- **Account** i.e. Cash, Credit card, Deposit...
- **Category**, can be income category like "Salary" or expence category like "Entertaiment" or both like "Transfer between accounts"

Because external keys dependensies, please keep attention to data creation order. Firstly create **Currency** then **Account** (Account uses currency atribute). Create **Category** of income or/and expenses. After this financial **Transaction** record can be created.

### 3.1. Currency

Let's creat first currency(Powershell syntax):
```
>curl.exe -X POST -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/transactions/api/currency_create/  -H "Content-Type: application/json" --data-raw "{\"code\":\"EUR\",\"description\":\"Euro\"}"

{"success":"currency created"}
```

Creating one more currency (bash sintax):
```
$ curl -X POST \
  -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" \
  -H "Content-Type: application/json" \
  -d '{"code":"USD","description":"US dollar"}' \
  http://127.0.0.1:8000/transactions/api/currency_create/

{"success":"currency created"}
```

list of currencies:
```
curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/transactions/api/currency/

[{"code":"EUR","description":"Euro"},{"code":"USD","description":"US dollar"}]
```

### 3.2. Accounts
Currency should be created before Account creating.
Creating account example:
```
curl -X POST \
  -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" \
  -H "Content-Type: application/json" \
  -d '{"name":"cash", "currency":"USD", "balance":0}' \
  http://127.0.0.1:8000/transactions/api/account_create/

  {success":"account created"}
  ```

Last of accounts:
```
curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/transactions/api/accounts/

[{"name":"cash","balance":"0.00","currency":"USD"}]
```

### 3.3. Category
Creating income category:
```
curl -X POST \
  -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" \
  -H "Content-Type: application/json" \
  -d '{"name":"api_test_income_categ", "income_flag":1, "expense_flag":0}' \
  http://127.0.0.1:8000/transactions/api/category_create/

  {"success":"category created"}
```
Creating expence category:
```
curl -X POST \
  -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" \
  -H "Content-Type: application/json" \
  -d '{"name":"api_test_income_categ", "income_flag":1, "expense_flag":0}' \
  http://127.0.0.1:8000/transactions/api/category_create/

  {"success":"category created"}
```

list of categories:
```
curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/transactions/api/category/

[{"name":"api_test_income_categ","income_flag":true,"expense_flag":false},{"name":"api_test_income_categ","income_flag":true,"expense_flag":false}]
```