from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'foundry_backend.api'

    def ready(self):
        """
        After the API has been instantiated, we need to populate
        it with the correct IAM models. For some reason, this is
        an error that will only show in the docker container, not
        as a run locally.
        """
        from . import autoload
        autoload.run()
