# Generated by Django 2.2.3 on 2019-09-06 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190906_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.SlugField(primary_key=True, serialize=False),
        ),
    ]
