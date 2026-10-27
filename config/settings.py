import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# Minimal .env loader; environment takes precedence.
if (BASE_DIR / '.env').exists():
    for line in (BASE_DIR / '.env').read_text(encoding='utf-8').splitlines():
        if line.strip() and not line.startswith('#') and '=' in line:
            k,v = line.split('=',1); os.environ.setdefault(k.strip(),v.strip())
DEBUG = os.environ.get('DEBUG','1') == '1'
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured('Configure SECRET_KEY para ejecutar con DEBUG=0.')
    SECRET_KEY = 'local-only-' + str(BASE_DIR)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost,127.0.0.1,testserver').split(',')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.environ.get('CSRF_TRUSTED_ORIGINS','').split(',') if origin.strip()]
# The production site is served behind Cloudflare Tunnel, which forwards this
# header with the original request scheme.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','audits']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME': os.environ.get('SQLITE_PATH',BASE_DIR/'db.sqlite3'),'OPTIONS':{'timeout':20}}}
if os.environ.get('DB_ENGINE') == 'postgresql':
    DATABASES = {'default': {'ENGINE':'django.db.backends.postgresql','NAME':os.environ['DB_NAME'],'USER':os.environ['DB_USER'],'PASSWORD':os.environ['DB_PASSWORD'],'HOST':os.environ.get('DB_HOST','localhost'),'PORT':os.environ.get('DB_PORT','5432')}}
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = os.environ.get('PLANT_TIME_ZONE','America/Mexico_City')
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR/'staticfiles'
PRIVATE_DIR = os.environ.get('PRIVATE_DIR')
if os.environ.get('SERVE_STATIC','0') == '1':
    MIDDLEWARE.insert(1,'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_DIRS = [BASE_DIR/'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/cuentas/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = LOGIN_URL
MAX_EXCEL_BYTES = int(os.environ.get('MAX_EXCEL_BYTES',10485760))
MAX_EXCEL_ROWS = int(os.environ.get('MAX_EXCEL_ROWS',50000))
MAX_EXCEL_UNCOMPRESSED = int(os.environ.get('MAX_EXCEL_UNCOMPRESSED',104857600))
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_EXCEL_BYTES + 1048576
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_EXCEL_BYTES
SESSION_COOKIE_HTTPONLY = True
AUTH_PASSWORD_VALIDATORS = [{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'}]

# Development templates must reflect file edits without retaining an older HTML layout.
if DEBUG:
    TEMPLATES[0]['APP_DIRS']=False
    TEMPLATES[0]['OPTIONS']['loaders']=[
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]
