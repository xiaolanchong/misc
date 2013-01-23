import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'wwwapp.settings'
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(ROOT_PATH)
from django.template.loader import render_to_string

def configAsModule():
    from django.conf import settings
    TEMPLATE_DIRS = ("wwwapp/templates",)
    settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS, DEBUG=False,
                       TEMPLATE_DEBUG=False)
    settings._target = None

def renderStartPage(tableData):
	rendered = render_to_string('index.html', { 'tableData': tableData })
	return rendered

def main():
    from django.conf import settings
    TEMPLATE_DIRS = ("templates",)
    settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS, DEBUG=False,
                    TEMPLATE_DEBUG=False)
    res = renderStartPage(None)
    import io
    with io.open('out.html', mode='w', encoding='utf-8') as file:
        file.write(res)

if __name__ == "__main__":
    main()
else:
    configAsModule()