# Generated by Django 3.1.1 on 2020-10-08 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_info', '0003_auto_20201006_0910'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartrackinginfo',
            options={'ordering': ['-id']},
        ),
    ]