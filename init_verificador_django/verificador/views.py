import os
import sys
import django
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.db import connection

def get_directory_structure(path, max_depth=3, current_depth=0):
    """
    Genera recursivamente la estructura del directorio del proyecto Django
    excluyendo carpetas innecesarias para mostrarla en la UI interactiva.
    """
    if current_depth > max_depth:
        return None
        
    try:
        name = os.path.basename(path)
    except Exception:
        name = path
        
    # Carpetas y archivos a ignorar
    ignore_list = ['.git', '__pycache__', 'venv', '.gemini', '.github', 'db.sqlite3', '.gitignore', '.idea', '.vscode']
    if name in ignore_list:
        return None
        
    is_dir = os.path.isdir(path)
    node = {
        'name': name,
        'is_dir': is_dir,
        'children': []
    }
    
    if is_dir:
        try:
            for item in sorted(os.listdir(path)):
                child_path = os.path.join(path, item)
                child_node = get_directory_structure(child_path, max_depth, current_depth + 1)
                if child_node:
                    node['children'].append(child_node)
        except PermissionError:
            pass
            
    return node

def hola(request: HttpRequest) -> HttpResponse:
    """
    Saludo mínimo sin templates: respuesta directa rápida.
    Cumple el punto del syllabus sobre respuesta HTTP directa y pruebas de conexión rápida.
    """
    return HttpResponse("Hola mundo (sin HTML/template). Proyecto OK ✅")

def home(request: HttpRequest) -> HttpResponse:
    """
    Vista del panel interactivo premium.
    Inspecciona y compila toda la información de la configuración del proyecto
    para verificar visualmente el cumplimiento del syllabus de Django.
    """
    # 1. Información del Sistema y Entorno
    is_venv = sys.prefix != sys.base_prefix
    python_version = sys.version.split()[0]
    django_version = django.get_version()
    
    # 2. Información del Proyecto y Rutas
    base_dir_str = str(settings.BASE_DIR)
    installed_apps = list(settings.INSTALLED_APPS)
    root_urlconf = settings.ROOT_URLCONF
    
    # 3. Configuración de Plantillas y Rutas de Archivos Estáticos
    templates_dirs = [str(d) for d in settings.TEMPLATES[0].get('DIRS', [])]
    templates_app_dirs = settings.TEMPLATES[0].get('APP_DIRS', False)
    static_url = settings.STATIC_URL
    
    # 4. Estado de la Base de Datos e Hilos de Migraciones
    db_engine = settings.DATABASES['default']['ENGINE']
    db_name = settings.DATABASES['default']['NAME']
    if hasattr(db_name, 'name'):  # Para objetos Path
        db_name_str = str(db_name)
    else:
        db_name_str = str(db_name)
        
    try:
        tables = connection.introspection.table_names()
        migrations_applied = len(tables) > 0
        tables_count = len(tables)
    except Exception:
        migrations_applied = False
        tables_count = 0
        tables = []
        
    # 5. Generar estructura de carpetas y serializar a JSON
    folder_tree = get_directory_structure(base_dir_str)
    import json
    folder_tree_json = json.dumps(folder_tree)

    context = {
        "mensaje": "Proyecto Django Inicializado y Verificado",
        "ruta": request.path,
        "metodo": request.method,
        "is_venv": is_venv,
        "python_version": python_version,
        "django_version": django_version,
        "base_dir": base_dir_str,
        "installed_apps": installed_apps,
        "root_urlconf": root_urlconf,
        "templates_dirs": templates_dirs,
        "templates_app_dirs": templates_app_dirs,
        "static_url": static_url,
        "db_engine": db_engine,
        "db_name": db_name_str,
        "migrations_applied": migrations_applied,
        "tables_count": tables_count,
        "tables_list": sorted(tables),
        "folder_tree_json": folder_tree_json,
    }
    
    return render(request, "verificador/home.html", context)


