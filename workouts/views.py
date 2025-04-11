from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.urls import reverse

from .forms import SessionForm
from .models import Session


class SessionDetailView(DetailView):
    model = Session
    template_name = "session_detail.html"


class SessionGet(ListView):
    model = Session
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SessionForm()
        return context


class SessionPost(SingleObjectMixin, FormView):
    model = Session
    form_class = SessionForm
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("session_detail", kwargs={"pk": self.object.pk })


class SessionListView(View):
    def get(self, request, *args, **kwargs):
        view = SessionGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = SessionPost.as_view()
        return view(request, *args, **kwargs)