from django import forms

from .models import Session, Workout, Exercise


class SessionCreateForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ()


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = (
            "exercise",
            "weight",
        )
        labels = {"weight": "Weight (kg)"}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["exercise"].queryset = Exercise.objects.filter(user=user.id)