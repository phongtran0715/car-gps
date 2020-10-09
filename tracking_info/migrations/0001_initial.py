# Generated by Django 3.1.1 on 2020-10-06 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarTrackingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('gas', models.FloatField(blank=True, null=True)),
                ('gas_status', models.BooleanField(blank=True, default=False)),
                ('speed', models.FloatField(blank=True, null=True)),
                ('odometer', models.FloatField(blank=True, null=True)),
                ('timestamp', models.TimeField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'car_tracking',
            },
        ),
    ]