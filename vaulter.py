
import json

import hvac


class vauleclient(object):
    """
    This class interacts with Vault API using HVAC library
    """

    def __init__(self, token, service_name, vault_addr="http://127.0.0.1:8200"):
        """
        Initialize the class and set self.token as token
        """
        self.token = token if token else False
        self.service_name = service_name
        self.vault_addr = vault_addr
        self.env_var_dict = {}
        self.vault_client = None

    def is_auth(self):
        if self.vault_client:
            return self.vault_client.is_authenticated()
        else:
            return False

    def auth_vault(self):
        """
        Authenticates with Vault against the Token provided
        by the user
        Updates self.client with HVAC client object

        v0.0.1:
            We only support github auth_backend

        Todo:
            v0.0.2:
                Add AWS-EC2 backend for having ECS / Beanstalk
                instances directly communicate with Vault to
                fetch required variables
        """
        if not self.is_auth():
            self.vault_client = hvac.Client(url=self.vault_addr)
            self.vault_client.auth_github(self.token)
        else:
            return self.vault_client

    def _read_vault(self):
        """
        Private method that interacts with Vault
        Reads the path relavent to the service name
        provided for the process
        Todo:
            v0.0.2:
                Make service_name as method argument not class argument
            v0.0.3:
                Verify based on lease id when did we last fethced the env
                for a given service. If over a certain time, notify
                team to update / rotate credentials
        """
        if self.is_auth() and self.service_name:
            try:
                vault_response = self.vault_client.read("secret/%s/env" % self.service_name)
            except Exception, e:
                return e
            else:
                return vault_response

    def _write_vault(self):
        """
        This version will be implement in version 0.0.2
        Writes to the path relavent to the service name
        provided for processing
        """
        pass

    def get_env(self):
        """
        Wrapper around our _read_vault method
        """
        return self._read_vault()

    def jsonify_env(self):
        """
        Created a valid json from the env data
        we fetch from vault

        In case of ECS, this helps in adding the JSON
        in the task definition

        In case of EBS, this will be called / passed to
        ebizzle / ebzl to update / create environment
        vairbales on the fly during the build pipeline
        """
        env_data = self.get_env()
        return json.dumps(env_data)

