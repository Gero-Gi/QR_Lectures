# Generated by Django 3.1.7 on 2021-04-05 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0005_auto_20210403_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='allow_all_connections',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='ip_address',
        ),
    ]
