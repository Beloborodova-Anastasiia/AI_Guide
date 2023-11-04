# AI Audio Guide
![Workflow status](https://github.com/Beloborodova-Anastasiia/AI_Guide/actions/workflows/merge_master.yaml/badge.svg)

This is a backend service for an mobile application telling customer stories about nearby attractions like a touristic guide. The stories are generated and sounded by AI.

### Backend service
- receives an attraction name from the mobile app;

- asks Chat GPT (gpt-3.5-turbo) to make a text narrative about the requested attraction on behalf of touristic guide;

- transforms the narrative into an audio file using AWS Polly (boto3) service (work in progress);

- returns this file as a response to the mobile app.

### Next steps

- receive user location from the mobile app;

- receive a list of the  nearest attractions using a map service;

- send the user the list of attractions.


### Technologies

Python 3.10

Django 24.2

Django REST Framework 3.14

Docker 20.10.17

### Local project run:

Clone a repository and navigate to it on the command line:

```
git clone https://github.com/Beloborodova-Anastasiia/AI_Guide.git
```

```
cd ai_guide
```

Create env-file by template:

```
OPEN_AI_API_KEY=YOUR_OPEN_AI_API_KEY
DJANGO_SECRET_KEY=YOUR_DJANGO_SECRET_KEY
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123
HOST=db
DB_PORT=5432
DEBUG=False
```

Run build docker-container:

```
for Windows and Mac:
docker-compose up -d --build
```
```
for Linux:
sudo docker-compose up -d --build
```

### API request examples

Get attraction:

```
POST: http://localhost/get_guide/
```
```
Request body:
{
 "query": "string"
}
```
Response:
```
{
  "id": int,
  "object_name": "string",
  "location": "string",
  "content": "string",
}
```


### Author

Anastasiia Beloborodova 

anastasiia.beloborodova@gmail.com