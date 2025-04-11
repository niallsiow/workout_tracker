from django.contrib import admin

from .models import Session, Workout, Exercise, Set

admin.site.register(Session)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Set)