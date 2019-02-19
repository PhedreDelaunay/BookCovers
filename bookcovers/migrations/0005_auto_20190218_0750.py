# Generated by Django 2.1.1 on 2019-02-18 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookcovers', '0004_booksseries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booksseries',
            name='book_id',
        ),
        migrations.RemoveField(
            model_name='booksseries',
            name='series_id',
        ),
        migrations.AddField(
            model_name='booksseries',
            name='book',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theBooksSeries', related_query_name='theBooksSeries', to='bookcovers.Books'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booksseries',
            name='series',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.DO_NOTHING, related_name='theBooksSeries', related_query_name='theBooksSeries', to='bookcovers.Series'),
            preserve_default=False,
        ),
    ]