# match4everyone

Open source project for building a platform that can match anyone.

Originally developed as [match4healthcare](https://github.com/match4everyone/match4healthcare) and in [production with ~10000 users](https://match4healthcare.de).


## Quick install
- Copy `backend.prod.env.example` and `database.prod.env.example` to `backend.prod.env` and `database.prod.env` and fill in appropriate values
- Run `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build` (uses Docker) and visit `http://localhost:8000/`

## Environment variables

TODO

## Manual Install
### Development
- Build images and run containers
`docker-compose up --build`
- Start previously built containers in background
`docker-compose start`
- Load test data (file needs to exist inside backend folder):
`docker-compose exec backend django-admin loaddata fixture.json`

File changes in python files trigger an auto-reload of the server.
Migrations are automatically executed when the container starts.

After changes to the Docker configuration, you have to restart and build the containers with `docker-compose up --build`.

### Production

#### Reverse Proxy

We recommend running the gunicorn server behind a reverse proxy to provide ssl and possibly run multiple services on one server.
The default configuration will make the docker container reachable on port 8000 only on 127.0.0.1.

A sample nginx configuration can be found at ./tools/nginx-sample-site.

#### Setup
Copy `backend.prod.env.example` to `backend.prod.env` and set variables as documented in the example file for Django
Copy `database.prod.env.example` to `database.prod.env` and set variables as documented in the example file for postgres on your host machine.

To run a container in production and in a new environment execute the `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build` script which builds the containers, runs all configurations and starts the web service.

If you want to deploy manually follow these steps closly:

#### Build the containers
(Copy `.env.example` to `.env` and adjust variables if you want to run the backend as non-root)
`docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build`

Building containers will run a number of django tasks automatically:
- make messages (`django-admin makemessages --no-location`)
- compile messages (`django-admin compilemessages`)
- collect static files (`django-admin collectstatic --no-input`)

Starting the containers will run the following django tasks on every backend startup:
- Perform migrations (`django-admin migrate`)
- Perform system check (`django-admin check`)


## Helpful management commands

- create fake users:
`python3 manage.py createfakeusers --add-a 50 --add-b 50`

- dump current database into fixture file (override fixture file):
`python3 manage.py dumpdata > fixture.json`

- load test data:
`python3 manage.py loaddata fixture.json`

- create superuser (to access staff page)
`python3 manage.py createsuperuser`


## Contributing

### Pre-commit checks
In order to run pre-commit checks every time, please run `pre-commit install` once in the repository. Pay attention when using `git commit -a`, because then the automatic code formatting will be added irreversably to your changes. The recommended workflow would be to use `git add` first, resulting in staged changes and unstaged codeformatting that you can double-check if you wish. You can of course always run `pre-commit run` to manually check all staged files before attempting a commit.

### Managing migrations
- create migration after model change:
`python3 manage.py makemigrations`

- migrate to current version:
`python3 manage.py migrate`

### Translation
- The project code language is English
- Additionally, we currently maintain German as a possible language.
- Add translatable strings in python with `_("Welcome to my site.")` and import `from django.utils.translation import gettext as _` ([Documentation](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#internationalization-in-python-code))
- Add translatable strings in templates with `{% blocktrans %}This string will have {{ value }} inside.{% endblocktrans %}` or alternatively with the `trans` block and include `{% load i18n %}` at the top ([Documentation](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#internationalization-in-template-code))
- Update the translation file
`django-admin makemessages -l de --no-location` (line numbers omitted to allow nicer merges)
- Edit translations in `backend/locale/de/LC_MESSAGES/django.po`

### Testing

For executing the tests use `python3 manage.py test`.

In case you add more required environment variables for productions, please check for their existance in `backend/apps/checks.py`.


## Implementation details

### Logging

Logging should always use the following pattern if possible:

```
import logging
logger = logging.getLogger(__name__)
logger.info('message',extra={ 'request': request })
```

If the request is not logged as an extra parameter, the log entry will **NOT** be messaged to slack!

Adding the request as extra parameter will automatically extract logged on user information as well as POST variables and take care of removing sensitive information from
the logs, respecting the @method_decorator(sensitive_post_parameters()). For example in user sign in, this will prevent logging of passwords.

**Warning:** Special care must be taken to avoid errors from circular references. The extra parameters are written to the log file and serialized as JSON. Circular references will cause
logging failure. One example would be adding the student to the extra dict:

Student has an attribute for the user, user has an attribute for the student, ...

These circular references will prevent the log entry from being written.
Including request is always safe, because the logging formatter contains dedicated code for request logging.

### Javascript & CSS

This project uses webpack to create javascript bundles. Custom Javascript is only added to pages when it is needed to enhance default Django functionality or to create user experience improvements.

Notable examples are
- Map Views
- User Profile to hide unneeded blocks

#### Develop JavaScript code using Docker (recommended)

Javascript sources are located in frontend/src folder and are aggregated to bundles loaded by the django application using webpack.
For Javascript development a docker container that runs the necessary build environment can be used. Use `docker-compose up --build` to start the frontend and backend dev containers,
it will automatically watch for changes in the src folder and rebuild the affected bundles. (Every file directly in src/ creates one bundle with the same name). If you add new files
you need to restart the container as the bundles to build are determined only once on start-up.

This is the recommended way to start building the js code. Alternatively you can also run just the backend container `docker-compose up --build backend` and use the following commands to
setup all required files for creating javascript bundles without the use of docker.

#### Alternative way to create JS bundles locally

To build locally node needs to be installed, for example using [Node Version Manager](https://github.com/nvm-sh/nvm) to install node.
Dependencies can then be installed using `cd frontend && npm install`

All commands need to be executed in `./frontend`.
- Build javascript bundles: `npm run build`
- Build javascript bundles in devMode and rebuilt when changes are made: `npm run dev`

#### Loading bundles in Python

To load a bundle in a django template add the following tags:
```
{% load render_bundle from webpack_loader %}
{% render_bundle 'student' %}
```

Django will then use the webpack-stats.json to determine which file from dist folder to include.
The dist folder has been added to the STATICFILES_DIRS so it will be found automatically

#### Adding new bundles

When creating new bundles simply create a new *.js file, this will automatically create an equally named bundle (examples main, map, student).
New bundles should be created as needed in the src directory, and load their modules from the sub-directories.

A Django-template should only load one bundle. The base template will always automatically take care of loading the main bundle. (Bootstrap and CSS)

### Permissions

We use a data migration to add groups and permissions to the database. Groups have permissions assigned and should be used as roles/tags for users, never give permissions directly to users. Permissions can be checked for with the `@permission_required('matching.can_view_access_stats')`. This includes inherited permissions from groups. We currently have the following groups with similarly named permissions:
```python
group_list = [
            "is_a",
            "is_b",
            "perm_user_stats",
            "perm_access_stats",
            "perm_approve_a",
            "perm_approve_b",
]
```
Note that django autogenerates lots of permissions, which might fit your requirements, for example `auth.permission.can_change_permission` or `matching.participanta.can_change_participanta`. Have a look in the admin panel if you want to easily check out the generated structure.


## Forks
Thanks for forking our repository. Pay attention that Travis CI doesn't test your code with sendgrid.
If you want to use sendgrid for your tests, add your repository name to the list in the if statement for NOT_FORK in `backend/match4everyone/settings/production.py` and specify the `SENDGRID_API_KEY` environment variable in the Travis run settings.
