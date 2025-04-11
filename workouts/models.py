from django.db import models


class Session(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField()

    def __str__(self):
        return self.date


class Exercise(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Workout(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.session}: {self.exercise}"


class Set(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    reps = models.IntegerField()

    def __str__(self):
        return f"{self.weight} {self.reps} {self.workout}"
