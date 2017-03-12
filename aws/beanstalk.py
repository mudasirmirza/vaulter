
import boto3


class BeanStalk(object):

    """
    Example usage
    boto_profile = ""
    beanstalk_application_name = ""
    beanstalk_environment_name = ""
    return BeanStalk(profile=boto_profile,
                     application=beanstalk_application_name,
                     environment=beanstalk_environment_name).environment_detail()

    Class to fetch data from AWS Beanstalk environment
    Scope of this class if not to create new application
    or environment in any already created application.
    However, we will update environments and to be specific
    just the the environment variables of environments.
    """
    def __init__(self, profile=None,
                 application=None,
                 environment=None):
        self.profile = profile
        self.application = application
        self.environment = environment
        self.session = boto3.Session(profile_name=self.profile)
        try:
            self.client = self.session.client("elasticbeanstalk")
        except Exception, e:
            self.client = None
            print(e)

    def application_detail(self):
        """
        Get details of the given application.
        Most probably we will not use this, but
        just in case if we need this
        :return: app_detail: type dict
        """
        if self.client and self.application:
            try:
                response_beanstalk = self.client.describe_applications()['Applications']
            except Exception, e:
                print(e)
                return {}
            else:
                return response_beanstalk

    def environment_detail(self):
        """
        Get details of the given environment
        Here we do not rely on the application, however
        the environment name you provide should be under
        the application name provided.
        The reason we will not rely on application is because
        the application can have multiple environments
        and each environment can have separate environment
        variables.
        Be very specific when providing environment name
        :return: env_var_dict: type dict
        """
        if self.client and self.application and self.environment:
            env_var_dict = {}
            try:
                env_details = self.client.describe_configuration_settings(
                    ApplicationName=self.application,
                    EnvironmentName=self.environment
                )
            except Exception, e:
                env_var_dict = {}
                print(e)
            else:
                env_vars = [j['Value'].split(",") for i in env_details['ConfigurationSettings'] for j in i['OptionSettings']
                            if j['OptionName'] == 'EnvironmentVariables'][0]
                """
                Got stuck here so asked on stackoverflow
                http://stackoverflow.com/questions/39053490/python-convert-list-to-dict-with-multiple-key-value
                """
                current_key = None
                try:
                    for item in env_vars:
                        if '=' in item:
                            current_key, value = item.split('=')
                            # This puts a string as the value
                            env_var_dict[current_key] = value
                        else:
                            # Check if the value is already a list
                            if not isinstance(env_var_dict[current_key], list):
                                # If value is not a list, create one
                                env_var_dict[current_key] = [env_var_dict[current_key]]
                            env_var_dict[current_key].append(item)
                except IndexError:
                    pass
                else:
                    return env_var_dict
