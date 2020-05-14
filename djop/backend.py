""" Authentication backend to provide object permission checking """

from django.db.models import Q

from djop.models import ObjectPermission
from djop.utils import validate_perm


def _has_perm(user, perm, obj):
    content_type, codename = validate_perm(obj, perm)
    if user.is_superuser:
        return True

    try:
        perm_cache = user._djop_perm_cache
    except AttributeError:
        user._djop_perm_cache = perm_cache = {}
    cache_key = f"{content_type.pk}_{obj.pk}"
    try:
        perms = perm_cache[cache_key]
    except KeyError:
        # get all permissions for this object
        perm_cache[cache_key] = perms = set(ObjectPermission.objects.filter(
            Q(groups__user=user) | Q(users=user),
            object_id=str(obj.pk),
            permission__content_type=content_type,
        ).values_list('permission__codename', flat=True))

    return codename in perms


class ObjectPermissionBackend:
    """ Backend to provide object permission checking """

    # pylint: disable=no-self-use

    def authenticate(self):
        """ This backend does not authenticate, only authorize """
        return None

    def has_perm(self, user, perm, obj=None):
        """ Checks for object permissions """
        if obj is None:
            return False
        return user.is_active and _has_perm(user, perm, obj)
