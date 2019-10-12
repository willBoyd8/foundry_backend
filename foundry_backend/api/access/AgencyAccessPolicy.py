from rest_access_policy import AccessPolicy


class AgencyAccessPolicy(AccessPolicy):
    statements = [
        {  # Allow anyone to list all the Agencies, and allow anyone to retrieve a specific Agency
            'action': ['list', 'retrieve'],
            'principal': '*',
            'effect': 'allow'
        },
        {  # Allow realtors that are part of an agency to manage that agency
            'action': ['update', 'partial_update'],
            'principal': ['group:realtor'],
            'effect': 'allow',
            'condition': 'is_agent_in_agency'
        },
        {  # Forbid realtors from deleting
            'action': ['delete'],
            'principal': ['group:realtor'],
            'effect': 'deny',
        },
        {  # Allow admin users to do anything
            'action': ['*'],
            'principal': ['group:admin'],
            'effect': 'allow'
        }
    ]
