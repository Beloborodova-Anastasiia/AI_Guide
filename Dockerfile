FROM python:3.8

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

COPY ai_guide/ /app

WORKDIR /app

# ENTRYPOINT ["bash", "docker-entrypoint.sh"]

CMD ["gunicorn", "ai_guide.wsgi:application", "--bind", "0:8000" ]
