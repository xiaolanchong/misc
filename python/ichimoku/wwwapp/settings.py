from django.conf import settings
TEMPLATE_DIRS = ("templates",)
settings.configure(TEMPLATE_DIRS=TEMPLATE_DIRS, DEBUG=False,
                   TEMPLATE_DEBUG=False)