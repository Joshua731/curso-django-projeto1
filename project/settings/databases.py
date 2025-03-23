from .environment import BASE_DIR
import os
if os.environ.get('DEBUG') == 1:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.environ.get('DATABASE_NAME', 'nome_do_banco'),
            'USER': os.environ.get('DATABASE_USER', 'usuario'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'senha'),
            'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
            'PORT': os.environ.get('DATABASE_PORT', '5432'),
        } 
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }