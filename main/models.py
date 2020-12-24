from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# User Credentials
class User(AbstractUser,models.Model):
    status_choices=[
        ("s","s"),
        ("i","i")
    ]
    status=models.CharField(max_length=5,choices=status_choices,default="s")

class Assignment(models.Model):
    name=models.CharField(max_length=64)
    dueDate=models.DateField()
    score=models.FloatField()
    intructor=models.CharField(max_length=64,null=True) # Remove Null= True later
    def __str__(self):
        return f"{self.name}: {self.dueDate}"
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
    courses=models.ForeignKey(Course,on_delete=models.CASCADE)
    major=models.CharField(max_length=64,default="Not mentioned")
    assignments=models.ManyToManyField(Assignment)
    # Write all students data rows here
    def __str__(self):
        return f"{self.credentials.username}"
# Instructor Model
class Instructor(models.Model):
    credentials=models.ForeignKey(User, on_delete=models.CASCADE)
    assignments=models.ManyToManyField(Assignment)
    major=models.CharField(max_length=64,default="Not mentioned")
    # Write all instructor data rows here
    def __str__(self):
        return f"{self.credentials.username}"
