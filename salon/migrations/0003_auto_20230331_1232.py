# Generated by Django 2.2.12 on 2023-03-31 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0002_auto_20230324_0837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='time',
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_time',
            field=models.DateTimeField(null=True),
        ),
    ]