# Generated by Django 5.1.2 on 2025-02-15 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_manager_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database_manager_app.column')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database_manager_app.table')),
            ],
        ),
    ]
