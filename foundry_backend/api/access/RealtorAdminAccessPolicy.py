from rest_access_policy import AccessPolicy


class RealtorAdminAccessPolicy(AccessPolicy):
    statements = [
        {  # Allow anyone to list and retrieve Nearby Attractions
            'action': ['list', 'retrieve'],
            'principal': '*',
            'effect': 'allow'
        },
        {  # Allow admin users to do anything
            'action': ['*'],
            'principal': ['group:admin'],
            'effect': 'allow'
        },
        {  # Allow realtors to create, update, and delete
            'action': ['create', 'update', 'delete'],
            'principal': ['group:realtor'],
            'effect': 'allow',
        },
    ]
