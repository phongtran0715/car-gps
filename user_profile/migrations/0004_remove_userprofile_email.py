# Generated by Django 3.1.1 on 2020-10-22 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_userprofile_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
