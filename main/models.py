from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# User Credentials
class User(AbstractUser,models.Model):
    """ status_choices=[
        ("i","Instructor"),
        ("s","Student")
    ]
    status=models.CharField(max_length=10,choices=status_choices,default="s") """
    pass
# Course Model
class Course(models.Model):
    name=models.CharField(max_length=50)
    code=models.UUIDField(primary_key=True,default=uuid.uuid4) #Reminder: add editable=False later.
    instructor=models.ForeignKey(User, on_delete=models.CASCADE)
    students=models.ManyToManyField(User,related_name="students")

    def __str__(self):
        return f" Course Name: {self.name}, Course Code: {self.code}"
    
# Student Model 
class Student(models.Model):
    credentials=models.ForeignKey(User, on_delete=models.CASCADE)
    courses= models.ManyToManyField(Course)
    # Write all students data rows here
    def __str__(self):
        return f" Student Name: {self.name}"
# Instructor Model
class Instructor(models.Model):
    credentials=models.ForeignKey(User, on_delete=models.CASCADE)
    # Write all instructor data rows here
    def __str__(self):
        return f" Instructor Name: {self.name}"