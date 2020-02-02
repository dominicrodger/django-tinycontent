DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tinycontent',
)

ROOT_URLCONF = 'tests.urls'
SECRET_KEY = 'thisbagismadefromrecycledmaterial'

MEDIA_ROOT = 'tests/testmedia'
MEDIA_URL = 'http://media.example.com/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]
