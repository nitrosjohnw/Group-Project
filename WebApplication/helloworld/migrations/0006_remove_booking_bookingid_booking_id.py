# Generated by Django 5.0.4 on 2024-04-26 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helloworld', '0005_alter_booking_bookingid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='bookingID',
        ),
        migrations.AddField(
            model_name='booking',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]