#!/bin/sh

# Salir inmediatamente si algún comando falla
set -e

echo "=== [1/4] Ejecutando migraciones de Base de Datos ==="
python manage.py migrate --noinput

echo "=== [2/4] Ejecutando pruebas unitarias automatizadas ==="
python manage.py test verificador

# Auto-crear superusuario si se pasan las variables correspondientes
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "=== [3/4] Creando superusuario administrador de forma automática ==="
    # Capturar error si el usuario ya existe para no detener el despliegue
    python manage.py createsuperuser --noinput || echo "El superusuario ya existe o no pudo crearse."
else
    echo "=== [3/4] Saltando auto-creación de superusuario (Variables no definidas) ==="
fi

echo "=== [4/4] Levantando servidor de desarrollo Django ==="
# Usamos exec para que el proceso de python reciba señales del sistema (como SIGTERM) correctamente
exec python manage.py runserver 0.0.0.0:8000
