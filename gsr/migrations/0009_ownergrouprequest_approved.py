# Generated by Django 2.2.28 on 2023-03-23 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsr', '0008_ownergrouprequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownergrouprequest',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
