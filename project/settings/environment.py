from pathlib import Path
from utils.environment import get_env_variable, parse_comma_sep_str_to_list
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS: list[str] = parse_comma_sep_str_to_list(get_env_variable('ALLOWED_HOSTS'))
CSRF_TRUSTED_ORIGINS: list[str] = parse_comma_sep_str_to_list(get_env_variable('CSRF_TRUSTED_ORIGINS'))

ROOT_URLCONF = 'project.urls'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#     'PAGE_SIZE': 10
# }