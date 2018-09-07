import os

from oauthenticator.generic import (
    GenericOAuthenticator,
)
from ecs_spawner import (
    EcsSpawner,
)

class AuthenticatorRemovedAtSymbol(GenericOAuthenticator):
    # It looks like the @ symbol in usernames causes lots of strange issues
    # with the notebooks
    async def authenticate(self, handler, data=None):
        auth = await super().authenticate(handler, data)
        return {
            **auth,
            'name': auth['name'].replace('@', '.'),
        }
c.JupyterHub.authenticator_class = AuthenticatorRemovedAtSymbol

c.JupyterHub.db_url = os.environ.get('DB_URL', 'sqlite:///jupyterhub.sqlite')
c.JupyterHub.log_level = 'DEBUG'

c.Authenticator.auto_login = True
c.Authenticator.enable_auth_state = True
c.Authenticator.admin_users = set([os.environ['ADMIN_USERS']])

c.JupyterHub.spawner_class = EcsSpawner
c.EcsSpawner.endpoint = {
    'cluster_name': os.environ['ECS_SPAWNER__CUSTER_NAME'],
    'task_definition_arn': os.environ['ECS_SPAWNER__TASK_DEFINITION_ARN'],
    'securityGroup': os.environ['ECS_SPAWNER__SECURITY_GROUP'],
    'subnet': os.environ['ECS_SPAWNER__SUBNET'],
    'region': os.environ['ECS_SPAWNER__REGION'],
    'host': os.environ['ECS_SPAWNER__HOST'],
    'access_key_id': os.environ['ECS_SPAWNER__ACCESS_KEY_ID'],
    'secret_access_key': os.environ['ECS_SPAWNER__SECRET_ACCESS_KEY'],
    'port': 8888,
}
c.EcsSpawner.debug = True
c.EcsSpawner.start_timeout = 600
c.Spawner.env_keep = ['PATH', 'DATABASE_URL']
