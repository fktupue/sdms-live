# Generated by Django 4.0.2 on 2022-03-24 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SDMS', '0021_trips_management_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='visible',
            field=models.CharField(default='SHOW', max_length=10),
        ),
        migrations.AddField(
            model_name='farm',
            name='visible',
            field=models.CharField(default='SHOW', max_length=10),
        ),
        migrations.AddField(
            model_name='truck',
            name='visible',
            field=models.CharField(default='SHOW', max_length=10),
        ),
        migrations.AddField(
            model_name='user_account',
            name='visible',
            field=models.CharField(default='SHOW', max_length=10),
        ),
        migrations.CreateModel(
            name='Driver_FinancialReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_month', models.IntegerField()),
                ('trip_year', models.IntegerField()),
                ('trip_count', models.IntegerField(default=0)),
                ('bag_count', models.IntegerField(default=0)),
                ('driver_basic', models.IntegerField(default=0)),
                ('driver_additional', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SDMS.user_account')),
            ],
        ),
        migrations.CreateModel(
            name='Client_FinancialReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_inprogress', models.IntegerField(default=0)),
                ('trip_completed', models.IntegerField(default=0)),
                ('bag_count', models.IntegerField(default=0)),
                ('receivables', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SDMS.company')),
            ],
        ),
    ]
