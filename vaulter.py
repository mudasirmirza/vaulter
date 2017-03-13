
import json

import hvac


class VaultClient(object):
    """
    This class interacts with Vault API using HVAC library
    """

    def __init__(self, token,
                 service_name=None,
                 vault_addr="http://127.0.0.1:8200",
                 secret_path=None):
        """
        Initialize the class and set self.token as token
        :param service_name: This will mainly depend on how the env is setup
        :param vault_addr: Address of your vault server
        :param secret_path: This is the path from where you will fetch ENV variables
                            from vault server.
        """
        self.token = token if token else False
        self.service_name = service_name
        self.vault_addr = vault_addr
        self.env_var_dict = {}
        self.vault_client = None
        self.secret_path = secret_path
        self.auth_vault()

    def is_auth(self):
        """
        This to verify is we have already authenticated
        with vault or not
        """
        if self.vault_client:
            return self.vault_client.is_authenticated()
        else:
            return False

    def auth_vault(self):
        """
        Authenticates with Vault against the Token provided
        by the user
        Updates self.client with HVAC client object
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
        """
        if self.is_auth() and self.service_name and self.secret_path:
            env_dict = {}
            try:
                vault_response = self.vault_client.list(self.secret_path)
            except Exception, e:
                vault_response = {}
                print(e)

            if vault_response:
                for e in vault_response['data']['keys']:
                    env_dict[e] = self.vault_client.read("%s/%s" % (self.secret_path, e))['data']['value']
            return env_dict
        else:
            print("Invalid auth / service_name / service_path")
            return False

    def _write_vault(self, **kwargs):
        """
        This is very basic implementation of write functionality, we will
        improve this over time
        """
        if self.is_auth() and self.service_name and self.secret_path:
            if isinstance(kwargs, dict):
                vault_response = {}
                for k, v in kwargs.iteritems():
                    srvc_path = "%s/%s" % (self.secret_path, k)
                    try:
                        vault_response = self.vault_client.write(srvc_path, value=v)
                    except Exception, e:
                        vault_response = {}
                        print(e)
                    else:
                        # TODO: return required response by using vault_response
                        print("Successfully set %s in vault at %s" % (k, srvc_path))
                return vault_response
            else:
                print("Please make sure you provide a dict")
                return False
        else:
            print("Invalid auth / service_name / service_path")
            return False

    def write(self, **kwargs):
        """
        Wrapper around _write_vault method
        :param kwargs:
        :return:
        """
        return self._write_vault(**kwargs)

    def get_env(self):
        """
        Wrapper around our _read_vault method
        """
        return self._read_vault()

    def jsonify_env(self):
        """
        Created a valid json from the env data
        we fetch from vault
        """
        env_data = self.get_env()
        return json.dumps(env_data)
