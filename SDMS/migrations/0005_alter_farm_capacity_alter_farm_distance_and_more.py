# Generated by Django 4.0.2 on 2022-02-23 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SDMS', '0004_company_alter_user_account_profile_pic_truck_farm_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='capacity',
            field=models.DecimalField(decimal_places=1, max_digits=6),
        ),
        migrations.AlterField(
            model_name='farm',
            name='distance',
            field=models.DecimalField(decimal_places=1, max_digits=6),
        ),
        migrations.AlterField(
            model_name='farm',
            name='rate_code',
            field=models.IntegerField(default=0),
        ),
    ]
