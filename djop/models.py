""" Object permissions model """

from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext


class ObjectPermissionManager(models.Manager):
    """ Object Permission manager """

    def create(self, perm_name=None, permission=None, object_id=None,
               obj=None, **kwargs):
        """ Creates an object permission """

        if perm_name is not None and permission is not None:
            raise ValueError(
                gettext("perm_name and permission can not be set both"))
        if object_id is not None and obj is not None:
            raise ValueError(
                gettext("object_id and obj can not be set both"))
        if perm_name is not None:
            app_label, codename = perm_name.split(".")
            permission = Permission.objects.get(
                content_type__app_label=app_label, codename=codename)
        if obj:
            object_id = obj.pk
            if (ContentType.objects.get_for_model(obj) !=
                    permission.content_type):
                raise ValueError(gettext("Content type mismatch"))

        return super().create(permission=permission, object_id=object_id,
                              **kwargs)


class ObjectPermission(models.Model):
    """ Object Permission model """

    permission = models.ForeignKey(
        Permission, verbose_name=_("permission"),
        on_delete=models.CASCADE)
    object_id = models.TextField(_("object id"))

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("users"),
        related_name="object_permissions")
    groups = models.ManyToManyField(Group, verbose_name=_("groups"),
                                    related_name="object_permissions")

    objects = ObjectPermissionManager()

    def __str__(self):
        perm = self.permission
        return perm.__str__() if perm else super().__str__()

    class Meta:
        unique_together = [('permission', 'object_id')]
