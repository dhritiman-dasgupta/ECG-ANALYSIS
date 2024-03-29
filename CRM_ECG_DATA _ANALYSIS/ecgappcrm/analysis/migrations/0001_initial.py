# Generated by Django 4.1.13 on 2024-01-18 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('device_id', models.CharField(max_length=50, unique=True)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ecgdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=50)),
                ('scan_data', models.JSONField()),
                ('EventProcessedUtcTime', models.DateTimeField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=50, unique=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.patient')),
            ],
        ),
    ]
