# Generated by Django 2.2 on 2019-05-21 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookcovers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artbookindex',
            old_name='book_author',
            new_name='book_author_name',
        ),
        migrations.RenameField(
            model_name='artbookindex',
            old_name='cover',
            new_name='cover_title',
        ),
    ]
