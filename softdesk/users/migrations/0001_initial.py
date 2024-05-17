# Generated by Django 5.0.4 on 2024-04-26 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='Username')),
                ('age', models.PositiveIntegerField(verbose_name='Age')),
                ('can_be_contacted', models.BooleanField(default=False, verbose_name='Can Be Contacted')),
                ('can_data_be_shared', models.BooleanField(default=False, verbose_name='Can Data Be Shared')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
