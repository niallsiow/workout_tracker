from django.views.generic import ListView

from .models import Session

class SessionListView(ListView):
    model = Session
    template_name = "home.html"