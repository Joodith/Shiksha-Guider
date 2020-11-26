from django import views
from django.views.generic import TemplateView

class HomePage(TemplateView):
    template_name="home.html"
class AfterLogin(TemplateView):
    template_name ="after_login.html"
class Logout(TemplateView):
    template_name ="logout.html"