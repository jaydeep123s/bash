from match4healthcare.utils.imports import import_submodules

STATIC_HACK = False
if STATIC_HACK:
    """
    This code is never executed, but it is needed to trick IDEs and Python linters
    to register the dynamically loaded submodules.
    The actual modules are loaded dynamically during startup
    Inspired by https://github.com/celery/kombu/blob/4644a5e9400beac6668f326c16078286f7d60b64/kombu/__init__.py#L34
    """
    from .email_group import *  # noqa
    from .email_to_hospital import *  # noqa
    from .email_to_student import *  # noqa
    from .hospital import *  # noqa
    from .newsletter import *  # noqa
    from .newsletter_approved_by import *  # noqa
    from .student import *  # noqa
    from .user import *  # noqa

import_submodules(globals(), __name__, __path__)  # noqa: F405
