#!/usr/bin/env python3
"""
WSGI config for nobly project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""
import sys
import os


sys.path.append('/usr/local/apache2/htdocs/push/nobly/')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nobly.settings")

os.environ["DJANGO_SETTINGS_MODULE"] = "nobly.settings"


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
