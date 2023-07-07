FROM python:3.11.0-bullseye as base-image


ENV PYTHONUNBUFFERED 1

RUN apt-get update &&\
  apt-get install -y --no-install-recommends\
     # python-ldap dependencies
     build-essential=12.9 libldap2-dev=2.4.57+dfsg-3+deb11u1 libsasl2-dev=2.1.27+dfsg-2.1+deb11u1 &&\
  apt-get clean && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man

RUN pip install --no-cache-dir pip-tools==6.9.0


# -----

FROM base-image as production-image

# creates a system user (-r), with no password, no home directory set, and no shell
RUN groupadd -r default-group && useradd -r -s /bin/false -g default-group default-user

WORKDIR /code
RUN chown -R default-user:default-group /code
COPY --chown=default-user:default-group ./src /code/
COPY --chown=default-user:default-group ./buildrun/docker/#project_name/requirements/prod-requirements.txt /code/requirements.txt
RUN pip-sync requirements.txt --pip-args '--no-cache-dir --no-deps'
USER default-user


# -----

FROM base-image as base-test-image

WORKDIR /code
COPY  ./buildrun/docker/#project_name/requirements/test-requirements.txt /code/requirements.txt
RUN pip-sync requirements.txt --pip-args '--no-cache-dir --no-deps'


# -----

FROM base-image as dev-image

WORKDIR /code
COPY ./buildrun/docker/#project_name/requirements/dev-requirements.txt /code/requirements.txt
RUN pip-sync requirements.txt --pip-args '--no-cache-dir --no-deps'


# -----

FROM base-test-image as test-image

COPY ./src /code/
ENV SECRET_KEY=not-secret
ENV DATABASE_URL=postgresql://test_user:test_pwd@db:5432/test_db
ENV ENV_MODE=TEST
ENV DJANGO_SETTINGS_MODULE=configurations.test-settings


CMD ["sh","-c","python manage.py collectstatic --noinput && python manage.py makemigrations --check && python manage.py migrate && pytest"]
# -----
