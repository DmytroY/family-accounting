## Family accounting API documentation

API is RESTful JSON-based API. All requests are made to the endpoint beginning .../api/. All requests must be secure, i.e. https, not http.

In the examples below all requests have http://localhost:8000 or http://127.0.0.1:8000 which is related to the test development server. Note that in the production proper host shoud be used.

### 1. Obtaining and regenerating API token
Only requests of authorized users will be processed by API. As first step username and password should be used to obtain user's API token authentication token:

`curl -X POST -d "username=<your_username>&password=<your_password>" "<site_URL>/api/token/"`

for example during local run:
```
curl -X POST -d "username=user1&password=******" http://127.0.0.1:8000/api/token/
```
it returns:
```
{"token":"********************************"}
```

Alternatively build-in Django management tool can be used to obtain token: `python family_acc/manage.py drf_create_token <username>`

Note, that repeating those commands do not recreate token. If you need regenerate token use next API request:

```
curl -X POST -H "Authorization: Token <OLD_TOKEN>" http://localhost:8000/api/token/regenerate/
```

As soon as you have valid token you can use it for authentication of youw API requests.



### 2. Users and Family
User can register itself, in this case new family identity will be created and this user willbe first member of the family:
```
>curl.exe -X POST http://127.0.0.1:8000/members/api/register/ -H "Content-Type: application/json" --data-raw "{\"first_name\":\"API_user_fname\",\"last_name\":\"API_user_lname\",\"email\":\"apiu@u.com\",\"username\":\"api_user\",\"password1\":\"somepass\",\"password2\":\"somepass\"}"

{"success":"user created"}
```

By using existing user authentication we can create oter users assigned to the same family.




```
curl -H "Authorization: Token ************" http://127.0.0.1:8000/members/api/members/

[{"id":2,"username":"user1","email":"u1@u.com"},{"id":3,"username":"user2","email":"user2@u.com"},{"id":4,"username":"user3","email":"u3@u.com"},{"id":5,"username":"user4","email":"jd@u.com"}]
```