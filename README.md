# Mist - Game store

A django application allowing users to browse and purchase computer games

## Configuration

app.yaml for google cloud delpoyment is untracked as secrets are set as env vairables, the structure of the file looks like so:

```runtime: python311

entrypoint: gunicorn store.wsgi:application


instance_class: F1

automatic_scaling:
  min_instances: 0
  max_instances: 1
  target_cpu_utilization: 0.65

beta_settings:
  cloud_sql_instances: project-<projectId>:europe-west1:mist-db

env_variables:
  DJANGO_SETTINGS_MODULE: "store.settings"
  DJANGO_SECRET_KEY: "CHANGE_ME"  # better set via Secret Manager later
  DJANGO_DEBUG: "False"
  CLOUD_SQL_CONNECTION_NAME:
  DB_USER: 
  DB_PASSWORD: 
  DB_NAME: 
  FIREBASE_CREDENTIALS_JSON: |
    {
      <Firebase Json Credentials>
    }
```
include this for deployment
---

Missing for local development is the .env file strutured like so:

```
FIREBASE_API_KEY = 
FIREBASE_CREDENTIALS_JSON = "<firebase creds as string>"
CLOUD_SQL_CONNECTION_NAME = 
DB_PASSWORD = 
DB_NAME = 
```

## Tests

Test are included in /tests they are pytest based and can be run with ``pytest -q``

11/11 tests are passing