from django.contrib import admin

from .models import Lecture, Session, Department

admin.site.register(Lecture)
admin.site.register(Department)
admin.site.register(Session)
