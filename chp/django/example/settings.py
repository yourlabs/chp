import os


# FORM_RENDERER = 'chp.django.mdc.renderer.FormRenderer'

SECRET_KEY = os.getenv('SECRET_KEY', 'notsecret')
DEBUG = os.getenv('DEBUG', False)
ROOT_URLCONF = 'chp.django.example.urls'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'chp.django',  # management command
    'chp.django.example.blog',
    # 'chp.django.example.todos',
    # 'crudlfap',
]
ALLOWED_HOSTS = []
if DEBUG:
    ALLOWED_HOSTS = ['*']
    if 'debug_toolbar' in INSTALLED_APPS:
        from .utils import IP_List
        INTERNAL_IPS = IP_List('127.0.0.1', '192.168.1.0/24')

STATIC_URL = '/static/'
BASE_DIR = os.path.dirname(__file__)
STATICFILES_DIRS = [
    BASE_DIR,
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chp.django.threadlocals.ThreadLocalMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },

]
TIME_ZONE = "Europe/London"
