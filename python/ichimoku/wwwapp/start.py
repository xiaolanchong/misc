import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(ROOT_PATH)

#print (os.environ['SERVER_SOFTWARE'])
try:
    from django.conf import settings
    TEMPLATE_DIRS = ("templates",)
    settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS, DEBUG=False,
                   TEMPLATE_DEBUG=False)
except ImportError:
    pass
	
from django.conf import settings

settings._target = None

from django.template.loader import get_template, render_to_string





#tmpl = loader.get_template('index.html')
def renderStartPage(tableData):
	rendered = render_to_string('index.html', { 'tableData': tableData })
	return rendered