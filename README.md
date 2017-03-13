# vaulter

Tool to utilize HashiCorp Vault when deploying to AWS ElasticBeanstalk 

TODO: add support for ECS


### Usage (dev only)

Currently we have tested with Github Auth.

- ```vault server -config=vault_server/vault-file.hcl```
- ```vault init -key-threshold=2 -key-shares=10``` (copy the output and keep it somewhere safe for now)
- ```vault unseal``` (keep repeating till we have successfully completed the number of cycles provided in key-threshold)
- ```export VAULT_TOKEN=<root token you got when ran the vault init command>```
- ```vault auth-enable github```
- ```vault write auth/github/config organization=<github organization name>```
- ```vault policy-write dev vault_policies/dev-policy.hcl```
- ```vault policy-write admins vault_policies/admin-policy.hcl```
- ```vault policy-write build vault_policies/build-policy.hcl```
- ```vault write auth/github/map/teams/<admin-team> vaule=admins```
- ```vault write auth/github/map/users/<github username> value=admins```
- ```vault write secret/<staging || production || testing || dev>/<AWS service beanstalk || ecs>/<service name>/<env name>/MYSQL_HOST value="localhost:3306"```


```aidl
In [1]: import vaulter
In [2]: tt = "<GITHUB TOKEN>"
In [3]: aa = vaulter.VaultClient(token=tt, service_name=<service_name>", secret_path="<secret path to env>")
In [4]: ggg = aa.get_env()
In [5]: ggg
Out[5]: {u'MYSQL_HOST': u'localhost:3306'}
In [6]: aa.jsonify_env()
Out[6]: '{"MYSQL_HOST": "localhost:3306"}'
```


### Helpers

Currently we only have a helper for import ENV VARS from beanstalk.

### Usage beanstalk helper

```aidl
In [1]: import aws.beanstalk
In [2]: boto_profile = "boto_profile_name"
In [3]: beanstalk_application_name = <beanstalk application name>
In [4]: beanstalk_environment_name = <beanstalk environment name under the application name provided above>
In [5]: aa = aws.beanstalk.BeanStalk(profile=boto_profile, 
                                     application=beanstalk_application_name, 
                                     environment=beanstalk_environment_name)
In [6]: aa.environment_detail()
Out[6]: 
{'KEY1': 'value1',
 'KEY2': 'value2',
 'KEY3': 'value3',
 'KEY4': 'value4'}

```

Now we can use the output ENV VARS and import them in VAULT 
```
import valuter
tt = "<GITHUB TOKEN>"
aa = vaulter.VaultClient(token=tt, service_name=<service_name>", secret_path="<secret path to env>")
aa.write(**aa.environment_detail())
```
