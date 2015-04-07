DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tinycontent',
)

ROOT_URLCONF = 'tests.urls'
SECRET_KEY = 'thisbagismadefromrecycledmaterial'