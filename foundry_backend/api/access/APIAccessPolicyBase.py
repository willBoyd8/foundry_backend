import abc
import json
import logging
from typing import List

from rest_access_policy import AccessPolicy
from .. import models


class APIAccessPolicyBase(AccessPolicy):
    """
    Defines a generic access policy for API Objects
    """
    @property
    @abc.abstractmethod
    def id(self):
        pass

    def get_policy_statements(self, request, view) -> List[dict]:
        default_policy_query = models.IAMPolicy.objects.filter(name='default')

        if not default_policy_query.exists():
            raise Exception('The default API Access Policy was not found')

        model_policy_query = models.IAMPolicy.objects.filter(name=self.id)

        if not model_policy_query.exists():
            policy_data = default_policy_query.get().serialize().get('statements')
            print('Attempted to get access policy for model \'{}\', failed.'.format(self.id))
            print('Using default access policy instead: \'{}\''.format(json.dumps(policy_data)))
            return policy_data
        else:
            policy_data = model_policy_query.get().serialize().get('statements')
            print('Attempted to get access policy for model \'{}\', success!.'.format(self.id))
            print('Using access policy: {}'.format(json.dumps(json.dumps(policy_data, indent=2))))
            return policy_data
