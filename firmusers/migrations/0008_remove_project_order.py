# Generated by Django 4.2 on 2023-06-15 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firmusers', '0007_project_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='order',
        ),
    ]
