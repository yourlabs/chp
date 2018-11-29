from django.middleware.csrf import get_token

from ..components import Input
from ..pyreact import cp


def Csrf(props=[], children=[]):
    """Return the CSRF token.

    Need to store the request in threading.local() as we don't have a access
    to template context processor variables.
    django-threadlocals is only updated to Django <1.10 on PyPI.
    django-tools has many features that are not needed.
    Adapted django-tools CSRF middleware feature in chp.django.threadlocals.
    """
    from .threadlocals import get_current_request

    request = get_current_request()
    if request is None:  # avoid fails in unittests
        csrf_token = "REQUESTnotAVAILABLEinCONTEXT"
    else:
        csrf_token = get_token(request)

    props.extend([
        cp("type", "hidden"),
        cp("name", "csrfmiddlewaretoken"),
        cp("value", csrf_token),
        ])
    return Input(props, children)
