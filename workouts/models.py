from django.db import models
from django.urls import reverse


class Session(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("session_detail", kwargs={"pk": self.id})

    def __str__(self):
        return f"{self.date}"


class Exercise(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Workout(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    # Units for weight are kg
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.session}: {self.exercise}, {self.weight}kg"


class Set(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    reps = models.IntegerField()

    def __str__(self):
        return f"{self.reps} {self.workout}"
