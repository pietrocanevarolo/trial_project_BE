FROM python:latest

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev postgresql-contrib

COPY /requirements.in /app/

RUN pip install --upgrade pip && \
    pip install pip-tools

RUN pip-compile requirements.in && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 80

CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:80"]