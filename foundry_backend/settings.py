"""
Django settings for foundry_backend project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dynaconf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, "static")


# For some reason, DRF doesn't seem to like DEFAULT_PAGINATION_CLASS in the YAML
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

settings_location = os.path.join(
    BASE_DIR, "deploy/settings.yaml,deploy/.secrets.yaml"
)

settings = dynaconf.DjangoDynaconf(
    __name__,
    GLOBAL_ENV_FOR_DYNACONF="FOUNDRY",
    ENV_SWITCHER_FOR_DYNACONF="FOUNDRY_ENV",
    SETTINGS_MODULE_FOR_DYNACONF=settings_location,
    INCLUDES_FOR_DYNACONF=['/opt/foundry/'],
    ENVVAR_FOR_DYNACONF="FOUNDRY_SETTINGS",
)
