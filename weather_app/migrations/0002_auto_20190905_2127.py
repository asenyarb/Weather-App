# Generated by Django 2.2.3 on 2019-09-05 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.DecimalField(decimal_places=0, max_digits=2)),
                ('temp_min', models.DecimalField(decimal_places=0, max_digits=2)),
                ('temp_max', models.DecimalField(decimal_places=0, max_digits=2)),
                ('humidity', models.DecimalField(decimal_places=0, max_digits=3)),
                ('pressure', models.DecimalField(decimal_places=0, max_digits=4)),
                ('description', models.CharField(max_length=20)),
                ('wind_speed', models.FloatField()),
                ('weather', models.CharField(max_length=20)),
                ('icon_id', models.CharField(max_length=20)),
                ('sunrise', models.CharField(max_length=6)),
                ('sunset', models.CharField(max_length=6)),
            ],
            options={
                'verbose_name': 'Weather',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='weather',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city', to='weather_app.Weather'),
        ),
    ]
