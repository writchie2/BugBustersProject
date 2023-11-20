from django.contrib import admin
from .models import Course, MyUser, Section
admin.site.register(MyUser)
admin.site.register(Course)
admin.site.register(Section)