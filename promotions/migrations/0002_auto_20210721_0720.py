# Generated by Django 3.1.1 on 2021-07-21 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promotions',
            options={'ordering': ['updated_at'], 'verbose_name_plural': 'Promotions'},
        ),
    ]