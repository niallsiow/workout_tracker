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

    def get_previous_workout(self):
        previous_workout = (
            Workout.objects.filter(
                session__user=self.session.user, exercise=self.exercise
            )
            .filter(id__lt=self.id)
            .last()
        )
        print(previous_workout)
        return previous_workout

    def get_weight(self):
        unit = "kg"
        weight = (
            str(int(self.weight))
            if self.weight == int(self.weight)
            else str(self.weight)
        )
        return f"{weight} {unit}"

    def get_sets(self):
        set_objects = Set.objects.filter(workout=self.id)

        set_count = {}
        for set in set_objects:
            reps = set.reps
            if reps in set_count:
                set_count[reps] += 1
            else:
                set_count[reps] = 1

        sets_string = ""
        for reps, sets in set_count.items():
            sets_string += f"{sets}x{reps} "
        return sets_string

    def __str__(self):
        return f"{self.session}: {self.exercise}, {self.weight}kg"


class Set(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    reps = models.IntegerField()

    def __str__(self):
        return f"{self.reps} {self.workout}"
