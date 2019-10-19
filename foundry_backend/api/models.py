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
            'statements': [statement.serialize() for statement in self.statements]
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
        e = self.effect

        if e == 'all':
            e = '*'
        elif e == 'safe':
            e = '<safe_methods>'

        return {
            'notes': self.notes,
            'effect': e,
            'principal': [principal.serialize() for principal in self.principals],
            'condition': [condition.serialize() for condition in self.conditions]
        }


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
