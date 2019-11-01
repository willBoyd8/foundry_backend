#!/usr/bin/env bash
# handles startup on the docker container. see phusion/baseimage

# Set a suitably random secret key
export FOUNDRY_SECRET_KEY=$(openssl rand -base64 100)
export FOUNDRY_ADMIN_PASSWORD=$(openssl rand -base64 32)

export DJANGO_SETTINGS_MODULE=foundry_backend.settings

# Migrate the database
django-admin makemigrations
django-admin migrate

django-admin collectstatic --noinput

# Start foundry
gunicorn --bind=0.0.0.0 --workers=2 foundry_backend.wsgi:application