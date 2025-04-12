from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .forms import SessionCreateForm, WorkoutForm
from .models import Session, Workout


class SessionListViewGet(ListView):
    model = Session
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SessionCreateForm()
        return context


class SessionPost(FormView):
    model = Session
    form_class = SessionCreateForm
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
        view = SessionListViewGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = SessionPost.as_view()
        return view(request, *args, **kwargs)


class SessionUpdateView(UpdateView):
    model = Session
    template_name = "session_edit.html"
    fields = ("notes",)
    

class WorkoutPost(SingleObjectMixin, FormView):
    model = Workout
    form_class = WorkoutForm
    template_name = "session_detail.html"

    def post(self, request, *args, **kwargs):
        self.session = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.session = Session.objects.get(pk=self.session.id)
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("session_detail", kwargs={"pk": self.session.pk})


class SessionDetailViewGet(DetailView):
    model = Session
    template_name = "session_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = get_object_or_404(Session, pk=self.kwargs['pk'])
        context["session_edit_form"] = SessionUpdateForm(instance=session)
        context["workout_new_form"] = WorkoutForm()
        return context


class SessionDetailView(View):
    def get(self, request, *args, **kwargs):
        view = SessionDetailViewGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = WorkoutPost.as_view()
        return view(request, *args, **kwargs)