from django.contrib import admin
from .models import User,Course,Student,Instructor
# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Instructor)