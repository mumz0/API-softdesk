# Generated by Django 5.0.4 on 2024-05-31 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_comment_created_time_comment_modified_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='customproject',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='customproject',
            name='modified_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
