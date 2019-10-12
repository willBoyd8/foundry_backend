from rest_access_policy import AccessPolicy


class HomeAlarmAccessPolicy(AccessPolicy):
    statements = [
        {  # Allow realtors to list and retrieve Nearby Attractions
            'action': ['list', 'retrieve'],
            'principal': 'group:realtor',
            'effect': 'allow'
        },
        {  # Allow admin users to do anything
            'action': ['*'],
            'principal': ['group:admin'],
            'effect': 'allow'
        },
        {  # Allow realtors to create, update, and delete,
           # if they are member to the agency that owns this
           # thing
            'action': ['create', 'update', 'partial_update', 'delete'],
            'principal': ['group:realtor'],
            'effect': 'allow',
            'condition': 'property_belongs_to_agency'
        }
    ]
