# Generated by Django 5.1.6 on 2025-03-29 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_bookreview_create_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookreview',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
