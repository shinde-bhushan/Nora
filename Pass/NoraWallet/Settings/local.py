from NoraWallet.Settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost:8000', '127.0.0.1:8000']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'nora-wallet-db',
       'USER': 'root',
       'PASSWORD': 'root',
       'HOST': '127.0.0.1',
       'PORT': '5432',
   }
}