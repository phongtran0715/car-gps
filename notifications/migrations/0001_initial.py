# Generated by Django 3.1.1 on 2021-02-02 12:09

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('body', models.CharField(max_length=250)),
                ('image', models.ImageField(blank=True, default='null', upload_to='')),
                ('url', models.CharField(blank=True, max_length=1024)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notifications',
                'ordering': ['created_at'],
            },
        ),
    ]
