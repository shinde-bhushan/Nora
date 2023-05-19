from NoraWallet.Settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# CORS_ALLOWED_ORIGINS = [
#     'https://arunpol.com/',
#     'https://api.arunpol.com/',
#     'https://staging.arunachalpoliceamrit.com/',
#     'https://api.staging.arunachalpoliceamrit.com',
#     'http://localhost:4200',
# ]

# CORS_ORIGIN_ALLOW_ALL = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',                      
        'USER': 'postgres',
        'PASSWORD': 'eUDnTi5NYCSclF0YgXUR',
        'HOST': 'nora-db.cz5c7djabith.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}


# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'Strict'
# SESSION_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = True
# X_FRAME_OPTIONS = 'DENY'