from django.contrib import admin

from users.models import Appointments, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Appointments)