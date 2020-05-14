""" Context Processor for the object permissions

Based on the Django perm context processor

"""

import django
from django.contrib.auth.context_processors import (
    PermWrapper as DjangoPermWrapper,
    PermLookupDict as DjangoPermLookupDict)
from django.db.models import QuerySet

filter_permitted = None


class Perm:
    """ Permission checker including object permissions """

    def __init__(self, user, app_label, perm_name):
        self.user = user
        self.app_label = app_label
        self.perm_name = perm_name

    def __contains__(self, obj):
        """ Makes it possible to check object permissions in templates

        This can be done with an expression like:
            if <object> in perms.<permission_app>.<permission_name>

        """

        # late import
        global filter_permitted
        if filter_permitted is None:
            from djop.db import filter_permitted

        perm = "%s.%s" % (self.app_label, self.perm_name)
        if isinstance(obj, QuerySet):
            return filter_permitted(self.user, perm, obj).exists()
        return self.user.has_perm(perm, obj)

    def __bool__(self):
        return self.user.has_perm("%s.%s" % (self.app_label, self.perm_name))


class PermLookupDict(DjangoPermLookupDict):
    """ PermLookupDict override to provide object permission checker """

    def __getitem__(self, perm_name):
        return Perm(self.user, self.app_label, perm_name)


class PermWrapper(DjangoPermWrapper):
    """ PermWrapper override to provide object permission checker """

    def __getitem__(self, app_label):
        return PermLookupDict(self.user, app_label)


def auth(request):
    """
    Return context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, use AnonymousUser (from
    django.contrib.auth).
    """
    if hasattr(request, 'user'):
        user = request.user
    else:
        from django.contrib.auth.models import AnonymousUser
        user = AnonymousUser()

    return {
        'user': user,
        'perms': PermWrapper(user),
    }


# monkey patch to avoid admin checks
django.contrib.auth.context_processors.auth = auth
