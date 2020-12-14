from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# User Credentials
class User(AbstractUser,models.Model):
    pass
# Course Model
class Course(models.Model):
    name=models.CharField(max_length=50)
    code=models.UUIDField(primary_key=True,default=uuid.uuid4) #Reminder: add editable=False later.
    instructor=models.ForeignKey(User, on_delete=models.CASCADE,related_name="courses")
    students=models.ManyToManyField(User,related_name="students",blank=True)

    def __str__(self):
        return f"{self.name}: {self.code}"
    
# Student Model 
class Student(models.Model):
    credentials=models.ForeignKey(User, on_delete=models.CASCADE)
    courses=models.ManyToManyField(Course)
    # Write all students data rows here
    def __str__(self):
        return f"{self.credentials.username}"
# Instructor Model
class Instructor(models.Model):
    credentials=models.ForeignKey(User, on_delete=models.CASCADE)
    # Write all instructor data rows here
    def __str__(self):
        return f"{self.credentials.username}"