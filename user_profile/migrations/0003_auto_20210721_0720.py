# Generated by Django 3.1.1 on 2021-07-21 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_auto_20210407_0904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ('id',), 'verbose_name_plural': 'Profile'},
        ),
    ]