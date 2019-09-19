#!/usr/bin/env bash

gunicorn --bind=0.0.0.0 --workers=2 foundry_backend.wsgi:application