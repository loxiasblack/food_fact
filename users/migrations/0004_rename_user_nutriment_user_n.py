# Generated by Django 5.0.6 on 2024-06-04 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_user_id_nutriment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nutriment',
            old_name='user',
            new_name='user_n',
        ),
    ]
