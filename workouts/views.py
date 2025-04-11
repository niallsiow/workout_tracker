from django.views.generic import ListView, DetailView

from .models import Session

class SessionListView(ListView):
    model = Session
    template_name = "home.html"


class SessionDetailView(DetailView):
    model = Session
    template_name = "session_detail.html"