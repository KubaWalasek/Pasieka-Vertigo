#!/usr/bin/env bash
set -euxo pipefail

python manage.py collectstatic --noinput
python manage.py migrate --noinput

echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'admin@example.com', 'kiklop123')" | python manage.py shell



echo "=== PYTHON/UVICORN DIAGNOSTICS START ==="
python - <<'PYCODE'
import os, sys, importlib
print("PYTHON:", sys.version)
print("PORT:", os.environ.get("PORT"))
try:
    importlib.import_module("Vertigo_Bee_Garden.asgi")
    print("ASGI import OK")
except Exception as e:
    print("ASGI import FAILED:", e)
    raise
PYCODE

exec uvicorn Vertigo_Bee_Garden.asgi:application --host 0.0.0.0 --port $PORT --log-level debug --loop asyncio --http h11
