# Generated by Django 5.0.6 on 2024-05-31 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='food name')),
                ('calories', models.FloatField(default=0)),
                ('protein', models.FloatField(default=0)),
                ('carbohydrates', models.FloatField(default=0)),
                ('fat', models.FloatField(default=0)),
            ],
        ),
    ]