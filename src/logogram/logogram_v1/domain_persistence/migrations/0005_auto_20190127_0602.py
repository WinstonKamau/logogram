# Generated by Django 2.1.5 on 2019-01-27 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logogram_v1', '0004_auto_20190126_1012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='words',
            old_name='flash_card',
            new_name='flashcard',
        ),
    ]