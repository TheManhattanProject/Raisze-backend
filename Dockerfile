# Pull base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
# COPY Pipfile Pipfile.lock /code/
# RUN pip install pipenv && pipenv install --system

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./raisze_backend/celery_start_scripts/worker /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./raisze_backend/celery_start_scripts/beat /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chmod a+rwx /etc
# Copy project
COPY . /code/