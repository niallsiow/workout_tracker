from django.db import models
from django.urls import reverse
from datetime import date


class Session(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def is_today(self):
        return self.date == date.today()


    def get_absolute_url(self):
        return reverse("session_detail", kwargs={"pk": self.id})

    def __str__(self):
        return f"{self.date}"


class Exercise(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def get_latest_working_weight(self):
        last_workout = Workout.objects.filter(exercise=self.id).last()
        if last_workout:
            return last_workout.get_working_weight()
        return "0kg"

    def get_latest_sets(self):
        last_workout = Workout.objects.filter(exercise=self.id).last()
        if last_workout:
            return last_workout.get_sets()
        return "N/A"

    
    def get_latest_workout_choices(self):
        last_workout = Workout.objects.filter(exercise=self.id).last()
        if last_workout:
            return last_workout.get_next_workout_choices()
        return "Goal For Next Workout = N/A"

    def __str__(self):
        return f"{self.name} {self.get_latest_working_weight()}"


class Workout(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    # Units for weight are kg
    working_weight = models.DecimalField(max_digits=6, decimal_places=2)
    # Fields for noting parameters to increase/decrease next workout
    NEXT_WORKOUT_CHOICES = {0: "no change", 1: "increase", 2: "decrease"}
    next_weight = models.IntegerField(choices=NEXT_WORKOUT_CHOICES, default=0)
    next_sets = models.IntegerField(choices=NEXT_WORKOUT_CHOICES, default=0)
    next_reps = models.IntegerField(choices=NEXT_WORKOUT_CHOICES, default=0)

    def get_previous_workout(self):
        previous_workout = (
            Workout.objects.filter(
                session__user=self.session.user, exercise=self.exercise
            )
            .filter(id__lt=self.id)
            .last()
        )
        return previous_workout

    def get_working_weight(self):
        unit = "kg"
        working_weight = (
            str(int(self.working_weight))
            if self.working_weight == int(self.working_weight)
            else str(self.working_weight)
        )
        return f"{working_weight} {unit}"

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
        return sets_string if sets_string else "No Sets Found"

    def get_next_workout_choices(self):
        next_workout_choices = ""
        if self.next_weight != 0:
            next_workout_choices += f"{self.NEXT_WORKOUT_CHOICES[self.next_weight].capitalize()} Weight"
        if self.next_sets != 0:    
            if next_workout_choices == "":
                next_workout_choices += f"{self.NEXT_WORKOUT_CHOICES[self.next_sets].capitalize()} Sets"
            else:
                next_workout_choices += f", {self.NEXT_WORKOUT_CHOICES[self.next_sets].capitalize()} Sets"
        if self.next_reps != 0:
            if next_workout_choices == "":
                next_workout_choices += f"{self.NEXT_WORKOUT_CHOICES[self.next_reps].capitalize()} Reps"
            else:
                next_workout_choices += f", {self.NEXT_WORKOUT_CHOICES[self.next_reps].capitalize()} Reps"
        if next_workout_choices == "":
            return "No Goal For Next Workout"
        return "Goal For Next Workout = " + next_workout_choices

    def __str__(self):
        return f"{self.session}: {self.exercise}, {self.working_weight}kg"


class Set(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    reps = models.IntegerField()

    def __str__(self):
        return f"{self.reps} {self.workout}"
