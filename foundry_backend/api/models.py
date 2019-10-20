from django.db import models
from multiselectfield import MultiSelectField


class IAMPolicy(models.Model):
    """
    Defines a list of IAM policies
    """
    notes = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'notes': self.notes,
            'statements': [statement.serialize() for statement in self.statements.all()]
        }


class IAMPolicyStatement(models.Model):
    """
    Defines a specific IAM policy statement
    """
    STATEMENT_ACTION_OPTIONS = (
        ('list', 'List all objects (GET)'),
        ('retrieve', 'Retrieve a specific object (GET with PK)'),
        ('create', 'Create a new object (POST)'),
        ('update', 'Update a specific object in it\'s entirety (PUT)'),
        ('update_partial', 'Update a specific object\'s specific elements (PATCH)'),
        ('delete', 'Delete an object (DELETE)'),
        ('all', 'All actions'),
        ('safe', 'Read only actions')
    )

    IAM_EFFECT_OPTIONS = (
        ('allow', 'This rule allows users permission'),
        ('deny', 'This rule denies users permission')
    )

    policy = models.ForeignKey(IAMPolicy, related_name='statements', on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, null=True, blank=True)
    actions = MultiSelectField(choices=STATEMENT_ACTION_OPTIONS)
    effect = models.CharField(max_length=5, choices=IAM_EFFECT_OPTIONS)

    def serialize(self) -> dict:
        final_actions = []

        for action in self.actions:
            if action == 'all':
                final_actions.append('*')
            elif action == 'safe':
                final_actions.append('<safe_methods>')
            else:
                final_actions.append(action)

        return_value = {
            'notes': self.notes,
            'effect': self.effect,
            'action': final_actions,
            'principal': [principal.serialize() for principal in self.principals.all()],
            'condition': [condition.serialize() for condition in self.conditions.all()]
        }

        return return_value


class IAMPolicyStatementPrincipal(models.Model):
    """
    Defines a principal actor for an IAM policy
    """
    statement = models.ForeignKey(IAMPolicyStatement, related_name='principals', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def serialize(self) -> str:
        return self.value


class IAMPolicyStatementConditionItem(models.Model):
    """
    Defines a condition for an IAM policy
    """
    policy = models.ForeignKey(IAMPolicyStatement, related_name='conditions', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
