# Generated by Django 4.0.2 on 2022-03-15 05:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SDMS', '0018_trips_last_edit_by_alter_trips_farm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trips',
            name='create_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
