"""
WSGI config for unrce_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

# Add the subdirectories as needed
sys.path.append(os.path.join(root_path, 'unrce_project'))
sys.path.append(os.path.join(root_path, 'unrce_project', 'unrce'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unrce_project.unrce_project.settings")

application = get_wsgi_application()
