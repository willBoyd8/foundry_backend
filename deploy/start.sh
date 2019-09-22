#!/usr/bin/env bash
# handles startup on the docker container. see phusion/baseimage

# Set a suitably random secret key
FOUNDRY_SECRET_KEY=$(openssl rand -base64 100)

# Start foundry
gunicorn --bind=0.0.0.0 --workers=2 foundry_backend.wsgi:application