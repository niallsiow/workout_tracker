from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import SessionCreateForm, WorkoutForm
from .models import Session, Workout, Set, Exercise


class SessionListViewGet(LoginRequiredMixin, ListView):
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
        return reverse("session_detail", kwargs={"pk": self.object.pk})


class SessionListView(View):
    def get(self, request, *args, **kwargs):
        view = SessionListViewGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SessionPost.as_view()
        return view(request, *args, **kwargs)


class WorkoutPost(FormView):
    model = Workout
    form_class = WorkoutForm
    template_name = "session_detail.html"

    def post(self, request, *args, **kwargs):
        self.session_id = self.kwargs.get("pk")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.session = Session.objects.get(pk=self.session_id)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("session_detail", kwargs={"pk": self.session_id})


class SessionDetailViewGet(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Session
    template_name = "session_detail.html"

    def test_func(self):
        session = self.get_object()
        return session.user == self.request.user

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


class SessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Session
    template_name = "session_edit.html"
    fields = ("notes",)

    def test_func(self):
        session = self.get_object()
        return session.user == self.request.user


class SessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Session
    template_name = "session_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        session = self.get_object()
        return session.user == self.request.user


class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    template_name = "workout_edit.html"
    fields = ("exercise", "weight")

    def test_func(self):
        workout = self.get_object()
        return workout.session.user == self.request.user

    def get_success_url(self):
        workout = self.object
        session = workout.session
        return reverse("session_detail", kwargs={"pk": session.id})


class WorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Workout
    template_name = "workout_delete.html"

    def test_func(self):
        workout = self.get_object()
        return workout.session.user == self.request.user

    def get_success_url(self):
        workout = self.object
        session = workout.session
        return reverse("session_detail", kwargs={"pk": session.id})


class SetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Set
    template_name = "set_new.html"
    fields = ("reps",)

    def test_func(self):
        workout_id = self.kwargs.get("workout_id")
        workout = get_object_or_404(Workout, pk=self.kwargs["workout_id"])
        return workout.session.user == self.request.user

    def form_valid(self, form):
        form.instance.workout = get_object_or_404(Workout, pk=self.kwargs["workout_id"])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        set = self.object
        workout = set.workout
        return reverse("session_detail", kwargs={"pk": workout.session.id})


class SetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Set
    template_name = "set_edit.html"
    fields = ("reps",)

    def test_func(self):
        set = self.get_object()
        return set.workout.session.user == self.request.user

    def get_success_url(self):
        set = self.object
        session = set.workout.session
        return reverse("session_detail", kwargs={"pk": session.id})


class SetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Set
    template_name = "set_delete.html"

    def test_func(self):
        set = self.get_object()
        return set.workout.session.user == self.request.user

    def get_success_url(self):
        set = self.object
        session = set.workout.session
        return reverse("session_detail", kwargs={"pk": session.id})


class ExerciseCreateView(CreateView):
    model = Exercise
    template_name = "exercise_new.html"
    fields = ("name",)

    def get_success_url(self):
        return reverse("home")
