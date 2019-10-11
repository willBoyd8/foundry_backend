from rest_access_policy import AccessPolicy
from foundry_backend.database.models import MLSNumber


class MLSNumberAccessPolicy(AccessPolicy):
    statements = [
        {  # Allow Admin to do anything
            'action': ['*'],
            'principal': 'group:admin',
            'effect': 'allow'
        },
        {  # Allow anyone to list and retrieve
            'action': ['list', 'retrieve'],
            'principal': '*',
            'effect': 'allow'
        }
    ]