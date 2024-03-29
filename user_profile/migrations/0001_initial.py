# Generated by Django 3.1.1 on 2021-02-02 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to='auth.user')),
                ('car_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('imei', models.CharField(max_length=50, null=True)),
                ('plate_number', models.CharField(max_length=50, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, max_length=1024, upload_to='')),
            ],
            options={
                'db_table': 'user_profile',
                'ordering': ('id',),
            },
        ),
    ]
