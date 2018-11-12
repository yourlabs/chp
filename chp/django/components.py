from django.middleware.csrf import get_token

from ..components import Input
from ..pyreact import ce, cp, get_prop


def Csrf(props=[], children=[]):
    """Return the CSRF token.

    Not possible as the request is not available at this point.
    """
    props.extend([
        cp("type", "hidden"),
        cp("name", "csrfmiddlewaretoken"),
        cp("value", "REQUEST NOT AVAILABLE IN CONTEXT"),
        # cp("value", get_token(request)),
        ])
    return Input(props, children)
