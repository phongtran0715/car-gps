# Generated by Django 3.1.1 on 2020-09-17 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlackListedToken',
        ),
    ]
