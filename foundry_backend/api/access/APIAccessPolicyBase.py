import json
from typing import List
from rest_access_policy import AccessPolicy
from .. import models


class APIAccessPolicyBase(AccessPolicy):
    """
    Defines a generic access policy for API Objects
    """

    _model_name = 'default'
    @property
    def model_name(self):
        return self._model_name

    def get_policy_statements(self, request, view) -> List[dict]:
        default_policy_query = models.IAMPolicy.objects.filter(name='default')

        if not default_policy_query.exists():
            raise Exception('The default API Access Policy was not found')

        model_policy_query = models.IAMPolicy.objects.filter(name=self.model_name)

        if not model_policy_query.exists():
            policy_data = default_policy_query.get().serialize().get('statements')
            print('Attempted to get access policy for model \'{}\', failed.'.format(self.model_name))
            print('Using default access policy instead: \'{}\''.format(json.dumps(policy_data)))
            return policy_data
        else:
            policy_data = model_policy_query.get().serialize().get('statements')
            print('Attempted to get access policy for model \'{}\', success!.'.format(self.model_name))
            print('Using access policy: {}'.format(json.dumps(json.dumps(policy_data, indent=2))))
            return policy_data


def make_access_policy(formatting_name: str, model_name: str) -> type(APIAccessPolicyBase):
    generated = type('{}AccessPolicy'.format(formatting_name), (APIAccessPolicyBase,),
                     {'__doc__': 'IAM model tied to the \'{}\' model'.format(model_name), '_model_name': model_name})

    return generated
