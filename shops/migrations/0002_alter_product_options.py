# Generated by Django 5.0.2 on 2024-07-08 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_time']},
        ),
    ]
