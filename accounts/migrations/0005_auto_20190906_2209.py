# Generated by Django 2.2.3 on 2019-09-06 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190906_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='token',
            field=models.CharField(max_length=30, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=30),
        ),
    ]
