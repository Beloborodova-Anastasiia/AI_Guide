FROM python:3.8

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ai_guide/ /app

WORKDIR /app

CMD ["gunicorn", "ai_guide.wsgi:application", "--bind", "0:8000" ]
# CMD ["python3", "manage.py", "runserver", "0:8000"] 
