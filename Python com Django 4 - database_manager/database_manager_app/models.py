from django.db import models
from django.contrib.auth.models import User

class Database(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Table(models.Model):
    name = models.CharField(max_length=100)
    database = models.ForeignKey(Database, on_delete=models.CASCADE)

class Column(models.Model):
    name = models.CharField(max_length=100)
    column_type = models.CharField(max_length=100)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

class DataItem(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)