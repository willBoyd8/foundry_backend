#!/usr/bin/env bash
# handles startup on the docker container. see phusion/baseimage

# Set a suitably random secret key
FOUNDRY_SECRET_KEY=$(openssl rand -base64 100)

export DJANGO_SETTINGS_MODULE=foundry_backend.settings

# Migrate the database
django-admin makemigrations
django-admin migrate

django-admin collectstatic --noinput

# Start foundry
gunicorn --bind=127.0.0.1 --workers=2 foundry_backend.wsgi:application