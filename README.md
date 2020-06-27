# match4everyone

Open source project for building a platform that can match anyone.

Originally developed as [match4healthcare](https://github.com/match4everyone/match4healthcare) and in [production with ~10000 users](https://match4healthcare.de).


## Quick install
- Copy `backend.prod.env.example` and `database.prod.env.example` to `backend.prod.env` and `database.prod.env` and fill in appropriate values
- Run `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build` (uses Docker) and visit `http://localhost:8000/`

## Environment variables

TODO

## Install by hand
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
Copy `backend.prod.env.example` to `backend.prod.env` and set variables as documented in the example file for Django
Copy `database.prod.env.example` to `database.prod.env` and set variables as documented in the example file for postgres on your host machine.

To run a container in production and in a new environment execute the `deploy.sh` script which builds the containers, runs all configurations and starts the web service.

If you want to deploy manually follow these steps closly:

#### Build the containers
(Run `export CURRENT_UID=$(id -u):$(id -g)` if you want to run the backend as non-root)
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


### Implementation details

#### Logging

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


#### Permissions

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
