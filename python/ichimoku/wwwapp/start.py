
from django.conf import settings
from django.template.loader import get_template, render_to_string

TEMPLATE_DIRS = ("templates",)

settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS, DEBUG=False,
                   TEMPLATE_DEBUG=False)

#tmpl = loader.get_template('index.html')
def renderStartPage(tableData):
	rendered = render_to_string('index.html', { 'tableData': tableData })
	return rendered