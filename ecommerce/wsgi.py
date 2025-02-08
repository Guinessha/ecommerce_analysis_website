"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Path proyek Django di PythonAnywhere
project_home = '/home/guinessha/yourproject'
if project_home not in sys.path:
    sys.path.append(project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourproject.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
