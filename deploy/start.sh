#!/usr/bin/env bash
# handles startup on the docker container. see phusion/baseimage

gunicorn --bind=0.0.0.0 --workers=2 foundry_backend.wsgi:application