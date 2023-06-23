from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Firmuser(AbstractUser):
    professions = models.ForeignKey('Profession', on_delete=models.CASCADE, related_name='professions', null=True, blank=True)
    def __str__(self):
        return self.username

class Profession(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name

class Phone(models.Model):
    user = models.ForeignKey(Firmuser, on_delete=models.CASCADE, related_name='phones')
    name = models.CharField(max_length=11, null=True, blank=True)
    def __str__(self):
        return self.name


class CarNumber(models.Model):
    user = models.ForeignKey(Firmuser, on_delete=models.CASCADE, related_name='car_numbers')
    number = models.CharField(max_length=9, null=True, blank=True)
    def __str__(self):
        return self.number

class Project(models.Model):
    image = models.ImageField(upload_to='images', default='images/default.png')
    title = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    professions = models.ManyToManyField(Profession, related_name='projects', blank=True)
    files = models.FileField(upload_to='files/', null=True, blank=True)
    open = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtask_tasks', null=True)
    name = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    def __str__(self):
        return self.name

