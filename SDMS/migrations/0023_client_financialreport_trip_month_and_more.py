# Generated by Django 4.0.2 on 2022-03-24 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SDMS', '0022_company_visible_farm_visible_truck_visible_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client_financialreport',
            name='trip_month',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='client_financialreport',
            name='trip_year',
            field=models.IntegerField(default=0),
        ),
    ]
