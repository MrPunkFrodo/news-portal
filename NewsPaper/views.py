from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views import View
from news.tasks import hello

class HomePageView(TemplateView):
    template_name = 'home.html'
