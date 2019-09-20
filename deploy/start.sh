#!/usr/bin/env bash
# handles startup on the docker container

gunicorn --bind=0.0.0.0 --workers=2 foundry_backend.wsgi:application