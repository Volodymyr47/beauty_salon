# Generated by Django 2.2.12 on 2023-03-31 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0003_auto_20230331_1232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='booking_time',
            new_name='booking_from',
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_to',
            field=models.DateTimeField(null=True),
        ),
    ]
