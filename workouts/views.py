from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from .forms import SessionCreateForm, WorkoutForm
from .models import Session, Workout, Set


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
        context["workout_new_form"] = WorkoutForm()
        return context


class SessionDetailView(View):
    def get(self, request, *args, **kwargs):
        view = SessionDetailViewGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = WorkoutPost.as_view()
        return view(request, *args, **kwargs)


class SessionDeleteView(DeleteView):
    model = Session
    template_name = "session_delete.html"
    success_url = reverse_lazy("home")


class WorkoutUpdateView(UpdateView):
    model = Workout
    template_name = "workout_edit.html"
    fields = ("exercise", "weight")

    def get_success_url(self):
        workout = get_object_or_404(Workout, pk=self.kwargs["pk"])
        session = workout.session
        return reverse("session_detail", kwargs={"pk": session.id})


class WorkoutDeleteView(DeleteView):
    model = Workout
    template_name = "workout_delete.html"

    def get_success_url(self):
        workout = get_object_or_404(Workout, pk=self.kwargs["pk"])
        session = workout.session
        return reverse("session_detail", kwargs={"pk": session.id})

    
class SetCreateView(CreateView):
    model = Set
    template_name = "set_new.html"
    fields = ("reps",)

    def form_valid(self, form):
        form.instance.workout = get_object_or_404(Workout, pk=self.kwargs["workout_id"])
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        workout = get_object_or_404(Workout, pk=self.kwargs["workout_id"])
        return reverse("session_detail", kwargs={"pk": workout.session.id})
