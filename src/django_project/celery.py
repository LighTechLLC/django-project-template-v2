import os
import importlib
import pkgutil
from pathlib import Path

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


def discover_celery_tasks():
    """
    Custom function to discover and import all task modules from services.celery_tasks
    This replaces the autodiscover_tasks approach for custom folder structures.
    """
    try:
        # Import the celery_tasks package
        celery_tasks_package = importlib.import_module('services.celery_tasks')
        
        # Get the package path
        package_path = Path(celery_tasks_package.__file__).parent
        
        # Discover all Python modules in the package
        for _, module_name, is_pkg in pkgutil.iter_modules([str(package_path)]):
            if not is_pkg and module_name != '__init__':
                # Import each module to register tasks
                importlib.import_module(f'services.celery_tasks.{module_name}')
                print(f"✓ Discovered tasks from: services.celery_tasks.{module_name}")
                
    except ImportError as e:
        print(f"Warning: Could not import services.celery_tasks package: {e}")
    except Exception as e:
        print(f"Error during task discovery: {e}")


# Discover custom tasks from celery_tasks folder
discover_celery_tasks()
