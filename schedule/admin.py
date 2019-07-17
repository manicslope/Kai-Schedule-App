from django.contrib import admin

# Register your models here.
from .models import Schedule, Group

admin.site.register(Schedule)
admin.site.register(Group)
