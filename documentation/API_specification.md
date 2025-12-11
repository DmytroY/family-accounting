## Family accounting API documentation
### 1. Overview
API is RESTful JSON-based API. All requests are made to the endpoint beginning .../api/. All requests must be secure, i.e. https, not http.

In the examples below all requests have Host: http://127.0.0.1:8000 which is related to the test development server. Note that in the production proper host shoud be used.

### 2. Obtaining API token
use next format of request for obtaining authentication token:

`curl -X POST -d "username=<your_username>&password=<your_password>" "<site_URL>/api/token/"`

for example during local run:
```
curl -X POST -d "username=user1&password=******" http://127.0.0.1:8000/api/token/
```
returns:
```
{"token":"********************************"}
```

after this you can use the token for you API requests authentication:
```
curl -H "Authorization: Token ************" http://127.0.0.1:8000/members/api/members/

[{"id":2,"username":"user1","email":"u1@u.com"},{"id":3,"username":"user2","email":"user2@u.com"},{"id":4,"username":"user3","email":"u3@u.com"},{"id":5,"username":"user4","email":"jd@u.com"}]
```