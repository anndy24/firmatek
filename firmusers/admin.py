from django.contrib import admin
from .models import Firmuser, Project, Task, Subtask, CarNumber, Profession, Phone 

# Register your models here.
admin.site.register(Firmuser)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(CarNumber)
admin.site.register(Profession)
admin.site.register(Phone)