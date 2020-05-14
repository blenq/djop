from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext


def validate_perm(model_or_instance, perm):
    content_type = ContentType.objects.get_for_model(model_or_instance)
    if "." in perm:
        # app_label is present in both object and permission. These
        # must match.
        app_label, codename = perm.split(".", 1)
        if content_type.app_label != app_label:
            raise ValueError(gettext("App label mismatch"))
    else:
        codename = perm

    return content_type, codename
