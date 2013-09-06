import os, sys
sys.path.append('/opt/BlackHole/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'blackhole.black_hole.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
