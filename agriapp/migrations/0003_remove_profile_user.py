# Generated by Django 3.2.7 on 2021-11-15 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agriapp', '0002_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]