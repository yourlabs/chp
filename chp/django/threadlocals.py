# coding: utf-8

"""
    Code adapted from django-tools==0.42.4 (to avoid including all tools).

    threadlocals middleware
    ~~~~~~~~~~~~~~~~~~~~~~~

    make the request object everywhere available (e.g. in model instance).

    based on: http://code.djangoproject.com/wiki/CookBookThreadlocalsAndUser

    Put this into your settings:
    --------------------------------------------------------------------------
        MIDDLEWARE_CLASSES = (
            ...
            'django_tools.middlewares.ThreadLocal.ThreadLocalMiddleware',
            ...
        )
    --------------------------------------------------------------------------


    Usage:
    --------------------------------------------------------------------------
    from django_tools.middlewares import ThreadLocal

    # Get the current request object:
    request = ThreadLocal.get_current_request()

    # You can get the current user directly with:
    user = ThreadLocal.get_current_user()
    --------------------------------------------------------------------------

    :copyleft: 2009-2017 by the django-tools team, see AUTHORS for more
        details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
    # LICENSE
    All rights reserved.


    django-tools is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License version 3 or later as
    published by the Free Software Foundation.

    complete GNU General Public License version 3:
        http://www.gnu.org/licenses/gpl-3.0.txt

    German translation:
        http://www.gnu.de/documents/gpl.de.html

    # AUTHORS
    PRIMARY AUTHORS are and/or have been (alphabetic order):

    * Diemer, Jens
      Main Developer since the first code line.
      ohloh.net profile: <http://www.ohloh.net/accounts/4179/>
      Homepage: <http://www.jensdiemer.de/>


    CONTRIBUTORS are and/or have been (alphabetic order):
        - Ben Konrath <https://github.com/benkonrath>
        - Don Naegely <https://github.com/naegelyd>middleware
        - Lucas Wiman <https://github.com/lucaswiman>
"""

from __future__ import absolute_import, division, print_function

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object  # fallback for Django < 1.10


_thread_locals = local()


def get_current_request():
    """ returns the request object for this thread """
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """ returns the current user, if exist, otherwise returns None """
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


class ThreadLocalMiddleware(MiddlewareMixin):
    """ Simple middleware that adds the request object in thread local storage.
    """
    def process_request(self, request):
        _thread_locals.request = request

    def process_response(self, request, response):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        return response

    def process_exception(self, request, exception):
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
