# Generated by Django 3.2 on 2022-09-27 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oddam_app', '0003_alter_donation_is_taken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
    ]