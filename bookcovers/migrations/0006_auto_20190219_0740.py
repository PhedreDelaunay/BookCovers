# Generated by Django 2.1.1 on 2019-02-19 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookcovers', '0005_auto_20190218_0750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setexceptions',
            name='cover_id',
        ),
        migrations.RemoveField(
            model_name='setexceptions',
            name='set_id',
        ),
        migrations.AddField(
            model_name='setexceptions',
            name='cover',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.DO_NOTHING, related_name='theSetExceptions', related_query_name='theSetException', to='bookcovers.Covers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='setexceptions',
            name='set',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.DO_NOTHING, related_name='theSetExceptions', related_query_name='theSetException', to='bookcovers.Sets'),
            preserve_default=False,
        ),
    ]
