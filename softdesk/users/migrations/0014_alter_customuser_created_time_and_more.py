# Generated by Django 5.0.4 on 2024-05-31 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_customuser_created_time_customuser_modified_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
