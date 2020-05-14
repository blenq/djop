# djop

Django object permissions

Integrates with the existing Django authorization framework. It provides 
finegrained permissions per Model instance, instead of per Model class.

## Configuration

```Python
INSTALLED_APPS = [
    ...
    "django.contrib.contenttypes",
    "django.contrib.auth",
    ...
    "djop",
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'djop.backend.ObjectPermissionBackend',
]

```

## Usage
```python

    perm = ObjectPermission.objects.create(
            "myapp.view_myobject", obj=my_instance)

    perm.users.add(my_user)
    my_user.has_perm("myapp.view_myobject", my_instance)

    perm.groups.add(my_group)


```
