# Generated by Django 2.2.28 on 2023-03-03 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=512)),
                ('picture', models.ImageField(blank=True, upload_to='')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(null=True)),
                ('date_updated', models.DateField(null=True)),
                ('customer_interaction_rating', models.IntegerField(choices=[(1, '1 stars'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])),
                ('price_rating', models.IntegerField(choices=[(1, '1 stars'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])),
                ('quality_rating', models.IntegerField(choices=[(1, '1 stars'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')])),
                ('comment', models.CharField(blank=True, max_length=512)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(null=True)),
                ('date_updated', models.DateField(null=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, max_length=8192)),
                ('picture', models.ImageField(blank=True, upload_to='shop_images')),
                ('opening_hours', models.CharField(max_length=512)),
                ('location', models.CharField(max_length=128)),
                ('views', models.IntegerField(default=0)),
                ('categories', models.ManyToManyField(to='gsr.Category')),
                ('owners', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(null=True)),
                ('date_updated', models.DateField(null=True)),
                ('comment', models.CharField(max_length=512)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsr.Review')),
            ],
            options={
                'verbose_name_plural': 'Review replies',
            },
        ),
        migrations.AddField(
            model_name='review',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsr.Shop'),
        ),
    ]
