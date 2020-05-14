SECRET_KEY = 'test-key'
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "djop",
    "tests",
]

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',
                           'djop.backend.ObjectPermissionBackend']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'djop.db',
    }
}


