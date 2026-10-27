#!/bin/sh
set -eu
umask 077
mkdir -p "${PRIVATE_DIR:-/data/private}"
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
