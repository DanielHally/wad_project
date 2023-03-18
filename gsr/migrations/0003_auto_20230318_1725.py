# Generated by Django 2.2.28 on 2023-03-18 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsr', '0002_shop_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(max_length=512),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='reviewreply',
            name='comment',
            field=models.TextField(max_length=512),
        ),
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(blank=True, max_length=8192),
        ),
        migrations.AlterField(
            model_name='shop',
            name='location',
            field=models.TextField(max_length=128),
        ),
        migrations.AlterField(
            model_name='shop',
            name='opening_hours',
            field=models.TextField(max_length=512),
        ),
    ]