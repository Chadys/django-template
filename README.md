# setup the project

```bash
python3 ./buildrun/setup_project.py $PROJECT_NAME $PROJECT_GITLAB_IMAGE $SITE_NAME
# E.G. python3 ./buildrun/setup_project.py dommarket gitlab.domain.ovh:4567/domain/dev/dommarket/dommarket "DOM MARKET"
```

# Prerequisites
## task
```bash
brew install go-task/tap/go-task
```
## project dependencies
```bash
task install-dependencies
```
## IDE Configuration
### black
[Configure it for your IDE](https://black.readthedocs.io/en/stable/integrations/editors.html)

Please keep your version of black always up-to-date (`pip install black -U` to upgrade)

## Login to gitlab
To be able to push and pull dev image, first you'll need to authenticate
or you'll have an "denied: access forbidden error"
```bash
# use your LDAP credentials when asked for it
docker login gitlab.domain.ovh:4567
```

# How to run
## Preparation
```shell
cd buildrun/docker/#project_name
# If you have access to the credentials,
# this file should be updated with them after being copied
cp secrets_sample.env secrets.env

cd ../docker-compose/dev-env
# only needed on empty project setup
task compile-dep
# init the app with users and data
# Admin user will be created with credentials admin@domain.ovh:<choose_a_pwd>
# This should be called only the first time you run the app or if you want to reset everything
task init-app
```
## App run
```shell
# Run the app after first initialisation (it is advised to set up your IDE to run the app instead)
task up
```
Also setup the IDE's project interpreter to a docker-compose configuration, using [buildrun/docker/docker-compose/dev-env/docker-compose.yml](buildrun/docker/docker-compose/dev-env/docker-compose.yml)
service `web` and name it `#project_name-web DEV`


## Launch dependent services
```shell
task run-ldap
```


## Network configuration
Ports [80, 443, 9090, 5432] must be available on your machine.

### DNS
On a mac, add the following rule to `/etc/hosts`:
```
127.0.0.1	local-#domain_name.domain.ovh
```

### Certificate
To be able to correctly run your website in HTTPS without your browser protesting about an invalid
certificate, you'll need to manually add and trust the Caddy root certificate located [here](buildrun/docker/caddy/.caddy/data/caddy/pki/authorities/local/root.crt)
On a Mac, simply open this file using Keychain Access, then double-click on the certificate
once it has been added to System keychain, and in the Trust settings select "Always Trust".
If your browser still display the certificate as invalid after that, restart your browser.

### Urls
Don't use `localhost` as you'll have errors with the HTTPS configuration.
- #project_name website: https://local-#domain_name.domain.ovh/ (if you get a warning about invalid certificate, see previous section)
- #project_name openAPI interface: https://local-#domain_name.domain.ovh/api/v1/docs
- LDAP Admin: http://local-#domain_name.domain.ovh:9090/ (login DN is "cn=readonly,dc=domain,dc=ovh", pwd in `AUTH_LDAP_BIND_PASSWORD` of [dev.env](buildrun/docker/#project_name/dev.env))

You can connect using the admin user created automatically (username admin@domain.ovh, for password see [DJANGO_SUPERUSER_PASSWORD](buildrun/docker/project_name/dev.env))
or one of the existing ldap user (see [ldap config](buildrun/docker/ldap/custom/00_export.ldif))
using their mail and password "azertyuiop".

# How to add a new Python package requirement

Add you requirement to buildrun/docker/#project_name/requirements/base-requirements.in
(or dev-* / prod-* / test-* if your package is only useful in one context).
Then run:
```shell
cd buildrun/docker/docker-compose/dev-env
task compile-dep
# Don't forget to rebuild the service to include the new dependency
docker-compose up -d --no-recreate --build web
```
**/!\ The compile-dep service also do an upgrade of all package,
remove the `--upgrade` option in the docker-compose file from all the commands called to avoid that**

Don't forget to execute `task push` once you are done
