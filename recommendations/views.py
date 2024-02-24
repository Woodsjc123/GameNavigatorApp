from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
import os

class SPAView(View):
    def get(self, request, *args, **kwargs):
        with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as file:
            return HttpResponse(file.read(), content_type='text/html')