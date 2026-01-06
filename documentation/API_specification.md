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
- **Category**, can be income category like "Salary" or expense category like "Entertaiment" or both like "Transfer between accounts"

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

[{"id":1,"code":"USD","description":"US dollar"},{"id":2,"code":"EUR","description":"Euro"},]
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

[{"id":9,"name":"cash","balance":"0.00","currency":"USD"}]
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
Creating expense category:
```
curl -X POST \
  -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" \
  -H "Content-Type: application/json" \
  -d '{"name":"api_test_expense_categ", "income_flag":0, "expense_flag":1}' \
  http://127.0.0.1:8000/transactions/api/category_create/

  {"success":"category created"}
```

list of categories:
```
curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/transactions/api/category/

[{"id":1,"name":"api_test_income_categ","income_flag":true,"expense_flag":false},{"id":2,"name":"api_test_expense_categ","income_flag":false,"expense_flag":true}]

```

### 3.4. Transactions

#### 3.4.1. Income transaction creating

Below is API request for creating income transaction. Doesn't matter if you use positive or negative amount in this API request - it will be saved as positive in any case because it is an income. Note that you should use account id, not account name, reason is account.name is not unique, combination account.name + account.currency is unique. By providing account id you unambiguously identify account and currency.
```
curl -X POST \
  -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" \
  -H "Content-Type: application/json" \
  -d '{"date":"2025-12-23",
	"account": 9,
	"amount":23.12,
	"category":"api_test_income_categ",
	"remark":"some remark to income transaction"
   }'\
  http://127.0.0.1:8000/transactions/api/income_create/

{"success":"income created"}
```

#### 3.4.2. Expense transaction creating
Doesn't matter if you use positive or negative amount in this API request, because it is expense it always will be saved as negative amount. Same as in creating income  you should use account id, not account name here.
```
curl -X POST \
  -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" \
  -H "Content-Type: application/json" \
  -d '{"date":"2025-12-23",
	"account": 9,
	"amount":12.01,
	"category":"api_test_expense_categ",
	"remark":"some remark to income transaction"
   }'\
  http://127.0.0.1:8000/transactions/api/expense_create/
```

#### 3.4.3. List of transactions
To get list of all transactions:
```
curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/transactions/api/transactions/

[{"id":7,"date":"2025-12-23","account":"cash","amount":"23.12","currency":"USD","category":"api_test_income_categ","remark":"some remark to income transaction","created_by":"api_user"},{"id":8,"date":"2025-12-23","account":"cash","amount":"-12.01","currency":"USD","category":"api_test_expense_categ","remark":"some remark to income transaction","created_by":"api_user"}]

```

To filter transactions next parameters could be applied:
- **from** - report period start date(inclusive)
- **to** - report period end date(inclusive)
- **account** - name of income or expence account, note that there can be several accounts with same name but different currencies.
- **currency** - 3-letter code of currency
- **account_id** - account id. See more about account_id in [3.2. Accounts](###3.2.-accounts). Note, that by using account_id filtered reults will be limited only to account connected to relevant currency. The result will be same as when you use **account** & **currency** filters.
- **category** - name of income or expence category
- **count** - N last transactions


Examples:
```
curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" "http://127.0.0.1:8000/transactions/api/transactions/?from=2025-12-01&to=2025-12-31"

curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/transactions/api/transactions/?account=9

curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" "http://127.0.0.1:8000/transactions/api/transactions/?account=Card&currency=USD"

curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" http://127.0.0.1:8000/transactions/api/transactions/?category=api_test_expense_categ

curl -H "Authorization: Token df78ee9cfa687bc27008d9eb20a22fb07dd9c7b6" "http://127.0.0.1:8000/transactions/api/transactions/?count=5"
```
