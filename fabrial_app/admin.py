from django.contrib import admin
from fabrial_app.models import ToDoItem, ToDoList

admin.site.register(ToDoItem)
admin.site.register(ToDoList)