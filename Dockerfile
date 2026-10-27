FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBUG=0 \
    SERVE_STATIC=1 \
    SQLITE_PATH=/data/db.sqlite3 \
    PRIVATE_DIR=/data/private

WORKDIR /app
COPY requirements.txt requirements-docker.txt ./
RUN pip install --no-cache-dir -r requirements-docker.txt \
    && groupadd --system --gid 10001 fcd \
    && useradd --system --uid 10001 --gid fcd --home-dir /app fcd \
    && mkdir -p /data/private /app/staticfiles \
    && chown -R fcd:fcd /data /app/staticfiles

COPY --chown=fcd:fcd . .
RUN sed -i 's/\r$//' /app/docker/entrypoint.sh \
    && chmod 755 /app/docker/entrypoint.sh

USER fcd
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/cuentas/login/', timeout=4)" || exit 1
ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]
