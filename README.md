# Inicializador y Verificador de Proyectos Django (Módulo 6 - L2-D1)

Este proyecto educativo está diseñado para demostrar y verificar a la perfección el cumplimiento del tema:
**"2. Utilizar las herramientas administrativas provistas por el framework para la configuración de un nuevo proyecto web Django"**.

Sirve como una guía de referencia académica y como un dashboard interactivo que valida en tiempo real la correcta inicialización del entorno, dependencias, enrutamiento y arquitectura base.

---

## 📖 Fundamentos Conceptuales del Syllabus

### 1. Gestión de Entornos y PIP (Syllabus 2.1)
* **Entorno Virtual (`venv`)**: Es una herramienta que aísla las dependencias del proyecto. Al crear e instalar paquetes dentro de él, se evita contaminar la instalación global de Python y se previenen conflictos de versiones entre diferentes aplicaciones web.
* **El utilitario `pip`**: Gestor de paquetes oficial de Python. Se utiliza para descargar, instalar, actualizar y desinstalar paquetes y librerías externas (como Django).
* **Verificación de la instalación**:
  * `django-admin --version`: Confirma la presencia del utilitario de comandos de Django.
  * `python -m django --version`: Confirma que el intérprete de Python del entorno puede importar la librería.

### 2. Creación de Proyectos y Herramientas Administrativas (Syllabus 2.2)
* **`django-admin`**: Utilitario administrativo global de Django. Su función principal es realizar tareas que ocurren *antes* de que el proyecto exista, siendo la principal `django-admin startproject <nombre>`.
* **`manage.py`**: Archivo autogenerado al crear el proyecto. Reemplaza a `django-admin` para la administración local del proyecto y vincula automáticamente el archivo de configuración `settings.py` sin necesidad de configurarlo manualmente en la terminal.

#### Comandos Clave de `manage.py`:
* **`runserver`**: Inicia el servidor HTTP de desarrollo integrado para verificar la aplicación localmente.
* **`startapp`** *(referenciado como `startup` en algunos syllabus)*: Crea un nuevo módulo funcional (aplicación) con su correspondiente estructura de MVC/MTV.
* **`createsuperuser`**: Genera un usuario administrador para gestionar los modelos de datos en la interfaz administrativa autogenerada de Django (`/admin/`).
* **`migrate`**: Aplica los esquemas de base de datos pendientes (migraciones) en el motor de base de datos configurado.

### 3. Estructura de Directorios Estándar
Al ejecutar `django-admin startproject init_verificador_django`, se genera una doble carpeta:
1. **Carpeta raíz (externa)**: Contenedor del proyecto, entorno virtual (`venv/`) y requerimientos.
2. **Carpeta del proyecto (interna)**: Contiene `manage.py` y el paquete de configuración:
   * **`__init__.py`**: Archivo vacío que marca el directorio como un paquete Python importable.
   * **`settings.py`**: Parámetros globales del proyecto (Base de Datos, Apps Instaladas, Plantillas, Idioma).
   * **`urls.py`**: Tabla de enrutamiento principal (URLConf) del sitio web.
   * **`wsgi.py` / `asgi.py`**: Puntos de enlace con servidores de despliegue en producción.

### 4. Configuración y Espacios de Nombre (Namespaces)
* **Configuración de Paths (`settings.py`)**: Se utiliza `pathlib.Path` para definir de forma dinámica el directorio raíz `BASE_DIR`, lo que permite configurar rutas relativas portables para bases de datos y archivos estáticos.
* **Configuración de Templates**: Definición de la carpeta `templates` dentro del parámetro `DIRS` para centralizar las plantillas HTML a nivel de proyecto.
* **Manejo de Espacios de Nombres (Namespaces)**: El uso de `app_name = "verificador"` en los archivos `urls.py` de la aplicación permite organizar las rutas por ámbitos aislados. Esto evita colisiones de nombres al redireccionar o generar enlaces en proyectos con múltiples aplicaciones.

### 5. Arquitectura MTV (Model-Template-View)
Django implementa una variante del patrón de diseño clásico MVC (Modelo-Vista-Controlador):
* **Modelo (Model)**: La representación de los datos y las reglas de negocio (Base de Datos).
* **Plantilla (Template)**: La capa de presentación (HTML dinámico) que ve el usuario.
* **Vista (View)**: La lógica que une el modelo con la plantilla. Equivale al *Controlador* clásico, recibiendo una petición HTTP y entregando una respuesta HTTP.

---

## 🛠️ Guía Paso a Paso: Recreación e Instalación

### 1. Inicializar el Entorno
Crea la carpeta raíz del proyecto, activa tu entorno e instala Django utilizando `pip`:
```bash
# Crear directorio y entrar
mkdir init_verificador_django
cd init_verificador_django

# Crear entorno virtual
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/macOS
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Generar el Proyecto y la Aplicación
```bash
# Crear proyecto (estructura base)
django-admin startproject init_verificador_django

# Entrar a la carpeta del proyecto (donde está manage.py)
cd init_verificador_django

# Crear aplicación independiente
python manage.py startapp verificador
```

### 3. Configurar Settings y URLs
Registra la aplicación y define la ruta de las plantillas en `init_verificador_django/settings.py`:
```python
# Registrar app
INSTALLED_APPS = [
    ...
    'verificador',
]

# Configurar ruta de plantillas
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    },
]
```

Enlaza las rutas de la aplicación en `init_verificador_django/urls.py`:
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('verificador.urls')),
]
```

### 4. Ejecutar e Iniciar Servidor
```bash
# Ejecutar migraciones iniciales para crear tablas SQLite
python manage.py migrate

# Crear superusuario administrador
python manage.py createsuperuser

# Iniciar servidor de desarrollo
python manage.py runserver
```

---

## 🧪 Pruebas y Verificación del Proyecto

El proyecto incluye pruebas automatizadas para comprobar el enrutamiento y las respuestas. Puedes ejecutarlas localmente con:
```bash
python manage.py test verificador
```

---

## 🐳 Despliegue Automatizado con Docker

Para facilitar el despliegue y la replicabilidad exacta del entorno sin necesidad de instalar Python o dependencias de forma manual, el proyecto cuenta con soporte completo para **Docker** y **Docker Compose**.

### Prerrequisitos
- Tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/) (que incluye Docker Compose).

### Instrucciones de Despliegue:

1. **Construir e Iniciar los contenedores**:
   Ejecuta el siguiente comando en la raíz del proyecto (donde se ubica `docker-compose.yml`):
   ```bash
   docker compose up --build
   ```
   *Este comando compilará la imagen de Docker, creará el contenedor, ejecutará las migraciones de la base de datos, correrá el set de pruebas unitarias de forma automatizada y levantará el servidor web.*

2. **Acceder a la aplicación**:
   Abre tu navegador y entra en:
   - Sitio Web y Panel de Control: [http://localhost:8000/](http://localhost:8000/)
   - Saludo rápido (HttpResponse): [http://localhost:8000/hola/](http://localhost:8000/hola/)
   - Sitio Administrativo: [http://localhost:8000/admin/](http://localhost:8000/admin/)

3. **Credenciales del Administrador Autogeneradas**:
   El entrypoint del contenedor auto-proveerá un superusuario administrador si inicias mediante Docker Compose con las siguientes credenciales por defecto (modificables en `docker-compose.yml`):
   - **Usuario**: `admin`
   - **Contraseña**: `adminpassword123`
   - **Email**: `admin@verificador.cl`

4. **Detener el contenedor**:
   ```bash
   docker compose down
   ```

---

## ⚖️ Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Para más detalles, consulta el archivo [LICENSE](file:///c:/Users/BlandskronNotebook/Documents/updatesGitHubs/Django/M6/M6-L2-D1-InitVerificadorDjango/LICENSE) en el directorio raíz.

