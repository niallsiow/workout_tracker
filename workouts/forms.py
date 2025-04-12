from django import forms

from .models import Session, Workout


class SessionCreateForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ()


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ("exercise", "weight",)