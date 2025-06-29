from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import SessionCreateForm, WorkoutForm
from .models import Session, Workout, Set, Exercise


class SessionListViewGet(ListView):
    model = Session
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SessionCreateForm()

        if not self.request.user.is_anonymous:
            last_session = Session.objects.filter(user=self.request.user).last()
            context["last_session"] = last_session
        else:
            context["last_session"] = "N/A"
        
        return context


class SessionPost(FormView):
    model = Session
    form_class = SessionCreateForm
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.session = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("session_detail", kwargs={"pk": self.session.pk})


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        self.session_id = self.kwargs.get("pk")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.session = Session.objects.get(pk=self.session_id)
        self.workout = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("workout_edit", kwargs={"pk": self.workout.id})


class SessionDetailViewGet(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Session
    template_name = "session_detail.html"

    def test_func(self):
        session = self.get_object()
        return session.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workout_new_form"] = WorkoutForm(user=self.request.user)

        context["exercises"] = Exercise.objects.filter(user=self.request.user)
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


class WorkoutDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Workout
    template_name = "workout_detail.html"

    def test_func(self):
        workout = self.get_object()
        return workout.session.user == self.request.user


class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    template_name = "workout_edit.html"
    fields = ("exercise", "working_weight", "next_weight", "next_sets", "next_reps")

    def test_func(self):
        workout = self.get_object()
        return workout.session.user == self.request.user

    def get_success_url(self):
        workout = self.object
        return reverse("workout_edit", kwargs={"pk": workout.id})


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
        return reverse("workout_edit", kwargs={"pk": workout.id})


class SetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Set
    template_name = "set_edit.html"
    fields = ("reps",)

    def test_func(self):
        set = self.get_object()
        return set.workout.session.user == self.request.user

    def get_success_url(self):
        set = self.object
        workout = set.workout
        return reverse("workout_edit", kwargs={"pk": workout.id})


class SetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Set
    template_name = "set_delete.html"

    def test_func(self):
        set = self.get_object()
        return set.workout.session.user == self.request.user

    def get_success_url(self):
        set = self.object
        workout = set.workout
        return reverse("workout_edit", kwargs={"pk": workout.id})


class ExerciseListView(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = "exercise_list.html"


class ExerciseDetailView(LoginRequiredMixin, DetailView):
    model = Exercise
    template_name = "exercise_detail.html"


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    template_name = "exercise_new.html"
    fields = ("name",)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("exercise_list")


class ExerciseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Exercise
    template_name = "exercise_edit.html"
    fields = ("name",)

    def test_func(self):
        exercise = self.get_object()
        return exercise.user == self.request.user

    def get_success_url(self):
        return reverse("exercise_list")


class ExerciseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Exercise
    template_name = "exercise_delete.html"

    def test_func(self):
        exercise = self.get_object()
        return exercise.user == self.request.user

    def get_success_url(self):
        return reverse("exercise_list")
