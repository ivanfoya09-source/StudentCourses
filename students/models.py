from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    phone = models.CharField(max_length=13)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"