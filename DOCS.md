# Documentación Detallada: Inicializador y Verificador de Proyectos Django

Este documento explica cada parte del proyecto, su arquitectura y los componentes implementados en la aplicación **`init_verificador_django`** para la app **`verificador`**.

---

## 1. Estructura de Carpetas Generada

El proyecto se estructura bajo el esquema estándar de doble carpeta de Django (generado al no usar el parámetro `.` en `django-admin startproject`):

```
init_verificador_django/
├─ venv/                            # Entorno virtual aislado
├─ requirements.txt                 # Dependencias administradas por pip
├─ README.md                        # Guía académica del syllabus
├─ DOCS.md                          # Documentación técnica del proyecto
└─ init_verificador_django/         # Carpeta raíz del proyecto Django
   ├─ manage.py                     # Script administrativo de entrada
   ├─ init_verificador_django/      # Paquete de configuración principal
   │  ├─ __init__.py                # Inicializador de paquete
   │  ├─ settings.py                # Configuración global
   │  ├─ urls.py                    # Enrutamiento principal
   │  ├─ asgi.py                    # Configuración asíncrona
   │  └─ wsgi.py                    # Configuración de despliegue síncrono
   ├─ verificador/                  # Aplicación de control (Módulo)
   │  ├─ __init__.py
   │  ├─ admin.py                   # Registro en admin site
   │  ├─ apps.py                    # Metadatos de la app
   │  ├─ tests.py                   # Pruebas automatizadas (unitarias)
   │  ├─ urls.py                    # Enrutamiento de la app
   │  └─ views.py                   # Lógica de las vistas
   └─ templates/                    # Directorio de plantillas
      └─ verificador/
         └─ home.html               # Plantilla del panel interactivo
```

---

## 2. Entorno Virtual y PIP (`venv`)
* **Creación**: `python -m venv venv`
* **Activación (Windows)**: `venv\Scripts\activate`
* **Mapeo en Backend**: En `views.py` comprobamos si el entorno virtual está activo mediante la instrucción:
  ```python
  is_venv = sys.prefix != sys.base_prefix
  ```
  Esto devuelve un valor booleano indicando al dashboard si el proyecto corre de forma aislada (`True`) o de forma global en el sistema (`False`).

---

## 3. Herramientas Administrativas

### django-admin
Herramienta administrativa del framework a nivel global. Usada únicamente para crear el esqueleto inicial:
```bash
django-admin startproject init_verificador_django
```

### manage.py
Punto de entrada administrativo del proyecto. Vincula automáticamente el módulo de configuración `settings.py`. Sus comandos configurados e interactivos son:
* **`runserver`**: Levanta el servidor local de desarrollo.
* **`startapp`**: Genera el módulo `verificador/`.
* **`createsuperuser`**: Permite dar de alta al administrador del sitio.
* **`migrate`**: Genera el archivo SQLite `db.sqlite3` y aplica las tablas por defecto (sesiones, administración, autenticación).

---

## 4. Archivos de Configuración Principal

### `init_verificador_django/settings.py`
Se configuraron los siguientes parámetros indispensables:
1. **`BASE_DIR`**: Generado dinámicamente mediante `pathlib.Path(__file__).resolve().parent.parent`.
2. **`INSTALLED_APPS`**: Registra la aplicación local `'verificador'` para que Django busque sus plantillas, rutas y configuraciones.
3. **`TEMPLATES`**: Se modificó el parámetro `'DIRS'` para incluir `BASE_DIR / 'templates'`, permitiendo que el motor de plantillas de Django localice la carpeta general en el directorio raíz.
4. **`DATABASES`**: Conexión por defecto a base de datos embebida SQLite3 en la raíz del proyecto.

### `init_verificador_django/urls.py`
Enrutador raíz del proyecto. Delega el tráfico de la ruta raíz `""` a la aplicación mediante:
```python
path('', include('verificador.urls')),
```

---

## 5. Aplicación `verificador`

### Espacios de Nombres (Namespacing)
En `verificador/urls.py` se declara `app_name = "verificador"`. Esto aisla las rutas de la app, permitiendo usar `reverse('verificador:home')` en Python y `{% url 'verificador:home' %}` en plantillas HTML, evitando conflictos en proyectos complejos.

### Lógica de Vistas (`verificador/views.py`)
Implementa dos endpoints:
1. **`hola` (Respuesta Directa)**: Retorna un objeto `HttpResponse` sin requerir plantillas, ideal para pruebas de respuesta rápida en el navegador.
2. **`home` (Panel Interactivo)**:
   * Recopila información del sistema utilizando módulos estándar (`sys`, `os`, `django`).
   * Evalúa la conexión a base de datos con `django.db.connection` e inspecciona si las migraciones base están aplicadas.
   * Ejecuta un escáner recursivo del directorio del proyecto (excluyendo cachés, git y el venv) y serializa el árbol de archivos a JSON (`folder_tree_json`).
   * Envía toda la metadata a `home.html` para su renderización dinámica.

### Plantilla HTML (`templates/verificador/home.html`)
Diseñada como una interfaz web interactiva con:
* **Estilos CSS Custom**: Diseño premium oscuro ("dark-mode"), tarjetas de cristal translúcido (glassmorphism), y tipografías modernas.
* **Sistema de Pestañas**: Lógica JavaScript pura para alternar entre el Panel de Control, información de PIP/entornos, comandos administrativos, y fundamentos de arquitectura MTV.
* **Explorador de Archivos**: Componente interactivo que analiza el JSON enviado por el servidor y construye un árbol de directorios desplegable.

---

## 6. Pruebas Unitarias (`verificador/tests.py`)
Contiene pruebas automatizadas para garantizar la estabilidad del proyecto:
1. `test_hola_view_status_code`: Verifica que `/hola/` responda 200 y contenga el saludo de prueba.
2. `test_home_view_status_code_and_template`: Verifica que `/` responda 200, renderice `home.html` y contenga el título del panel.
3. `test_url_namespace_resolving`: Verifica que las reversiones de rutas utilizando el namespace `verificador` apunten a los paths correctos.

---

## 7. Arquitectura de Despliegue con Docker

El proyecto incluye soporte para contenedores Docker con el fin de simplificar la configuración inicial, garantizar que la ejecución se realice exactamente sobre el mismo sistema operativo y librerías, y automatizar tareas repetitivas de desarrollo:

### A. Dockerfile (Estrategia de Imagen)
- **Base**: Utiliza la imagen oficial de Python `python:3.11-slim` por su reducido tamaño y alto rendimiento.
- **Variables de Entorno**:
  - `PYTHONDONTWRITEBYTECODE=1`: Evita que Python escriba archivos `.pyc` de caché compilada en el contenedor.
  - `PYTHONUNBUFFERED=1`: Evita que la salida en consola sea retenida por búferes de memoria, permitiendo ver logs en tiempo real.
- **Herramientas**: Se instala `dos2unix` para sanitizar posibles finales de línea de estilo Windows (`CRLF`) en los scripts de shell y asegurar compatibilidad de ejecución en contenedores Linux.

### B. docker-entrypoint.sh (Ciclo de Vida de Arranque)
El contenedor no se limita a ejecutar el servidor de desarrollo, sino que coordina y audita secuencialmente:
1. **Migraciones**: Ejecución de `python manage.py migrate --noinput` para preparar el esquema relacional en SQLite3.
2. **Pruebas**: Ejecución de `python manage.py test verificador` para bloquear la puesta en marcha si el código presenta fallos.
3. **Superusuario**: Creación condicional del administrador por variables de entorno sin detener el script si la cuenta ya existe.
4. **Ejecución**: Lanzamiento del proceso de Django utilizando `exec` para delegar la recepción de señales de sistema (como SIGTERM o SIGKILL) directamente a Python.

### C. docker-compose.yml (Orquestación de Desarrollo)
- **Servicios**: Define el contenedor `web` exponiendo el puerto `8000` de forma bidireccional.
- **Volúmenes**:
  - Monta el directorio local en `/app` para permitir la sincronización en caliente del código (cualquier cambio en la máquina host se refleja inmediatamente en el contenedor).
  - Monta un volumen anónimo `/app/venv` para evitar que el entorno virtual del host interfiera o sobreescriba las librerías del contenedor.
- **Variables de Entorno**: Define `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`, y `DJANGO_SUPERUSER_EMAIL` para el aprovisionamiento automatizado del administrador.

---

## 8. Licencia del Proyecto
El proyecto está licenciado bajo la **Licencia MIT**, lo cual permite el libre uso, copia, modificación y distribución del código con fines educativos o comerciales, siempre que se conserve la declaración de derechos de autor original en el archivo `LICENSE`.

