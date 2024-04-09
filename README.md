# OPA implementation on python app

## Requirement

This opa implementation need opa server to be set up. See https://github.com/mhseptiadi/opa

## Installation

### Install minikube 

Please refer to https://minikube.sigs.k8s.io/docs/start/

---

### Build docker

#### Set to use docker on minikube:

For linux & mac:
```angular2html
eval $(minikube docker-env)
```

For windows using powershell:
```angular2html
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

#### Build the dockerfile
```angular2html
docker build -f Dockerfile -t opa-py:latest .
```

---

### Deploy to minikube

#### Deploy the yaml
```angular2html
kubectl apply -f deploy.yaml
```

#### Open url for testing
```angular2html
minikube service opa-py --url
```

---

### Api test

The return of minikube url will be something like `{host}:{port}`, for example http://127.0.0.1:55738
. Then we can use this for our testing.

There are 3 users for this testing:
```angular2html
[
    {
        "email": "user@user.com",
        "name": "user",
        "password": "admin",
        "roles": [
            "user"
        ]
    },
    {
        "email": "admin@admin.com",
        "name": "admin",
        "password": "admin",
        "roles": [
            "admin"
        ]
    },
    {
        "email": "other@other.com",
        "name": "other",
        "password": "other",
        "roles": [
        ]
    }
]
```

There are 3 api endpoints for this testing:

- Login API
- Get Users (admin and user role)
- Create Users (only admin role)


#### First, Use Login API
```angular2html
curl --location 'http://127.0.0.1:55738/api/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@admin.com",
    "password": "admin"
}'
```


#### Get Users api
From the login api above you will get authorization bearer. Copy the bearer and use it on get users api.

```angular2html
curl --location 'http://127.0.0.1:55738/api/users' \
--header 'Authorization: {{bearer}}'
```

Both `admin` and `user` can access this endpoint because they have role admin and user. The last user `other` cannot access this endpoint because he doesn't have access.


#### Create User api

The same like before, copy the bearer from login and use it in this api.

```angular2html
curl --location 'http://127.0.0.1:55738/api/users' \
--header 'Authorization: {{bearer}}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "user2@user2.com",
    "name": "user2",
    "password": "user2",
    "roles": [
        "user2"
    ]
}'
```

In this create user api, only `admin` can have access.
