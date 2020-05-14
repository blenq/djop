from django.db import models
from django.db.models.functions import Cast

from djop.models import ObjectPermission
from djop.utils import validate_perm


def filter_permitted(user, perm, qs):

    content_type, codename = validate_perm(qs.model, perm)

    if not user.is_active:
        # you get nothing
        return qs.none()

    if user.is_superuser:
        # you get all
        return qs

    # get the filter queryset with allowed primary keys from the object
    # permissions
    obj_perm_qs = ObjectPermission.objects.filter(
        models.Q(groups__user=user) |
        models.Q(users=user),
        permission__codename=codename,
        permission__content_type=content_type,
    ).values(_id=Cast('object_id', qs.model._meta.pk))

    # apply the filter
    return qs.filter(pk__in=obj_perm_qs)
