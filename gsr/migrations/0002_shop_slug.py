# Generated by Django 2.2.28 on 2023-03-18 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
    ]
