from django.contrib import admin
from .models import Database, Table, Column

admin.site.register(Database)
admin.site.register(Table)
admin.site.register(Column)