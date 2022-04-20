from django.contrib import admin
from django.contrib import auth
from .models import *

admin.site.register(User)
admin.site.register(Project)
admin.site.register(File)
admin.site.register(Version)
admin.site.register(Action)