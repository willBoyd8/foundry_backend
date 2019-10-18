from django.db import models
from multiselectfield import MultiSelectField


class IAMPolicy(models.Model):
    """
    Defines a list of IAM policies
    """
    notes = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)


class IAMPolicyRule(models.Model):
    """
    Defines a specific IAM policy
    """
    IAM_ACTION_OPTIONS = (
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

    policy = models.ForeignKey(IAMPolicy, related_name='rules', on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, null=True, blank=True)
    actions = MultiSelectField(choices=IAM_ACTION_OPTIONS)
    effect = models.CharField(max_length=5, choices=IAM_EFFECT_OPTIONS)


class IAMPrincipalItem(models.Model):
    """
    Defines a principal actor for an IAM policy
    """
    policy = models.ForeignKey(IAMPolicyRule, related_name='principals', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)


class IAMConditionItem(models.Model):
    """
    Defines a condition for an IAM policy
    """
    policy = models.ForeignKey(IAMPolicyRule, related_name='conditions', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
