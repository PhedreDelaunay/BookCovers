# Generated by Django 2.1.1 on 2018-10-14 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookcovers', '0003_authoraka'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AuthorAka',
            new_name='AuthorAkas',
        ),
    ]