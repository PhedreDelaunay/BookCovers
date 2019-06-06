# Generated by Django 2.2 on 2019-05-31 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookcovers', '0006_artbookindex_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artbookindex',
            name='cover_title',
        ),
        migrations.AddField(
            model_name='artbookindex',
            name='publish_year',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
