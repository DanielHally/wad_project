# Generated by Django 2.2.28 on 2023-03-19 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsr', '0003_auto_20230318_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date_added',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_updated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='reviewreply',
            name='date_added',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='reviewreply',
            name='date_updated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='date_added',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='date_updated',
            field=models.DateTimeField(null=True),
        ),
    ]
