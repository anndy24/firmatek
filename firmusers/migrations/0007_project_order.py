# Generated by Django 4.2 on 2023-06-15 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firmusers', '0006_project_open_alter_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
