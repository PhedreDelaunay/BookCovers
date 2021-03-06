# Generated by Django 3.0.1 on 2020-07-05 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookcovers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artbook',
            options={'ordering': ('title',)},
        ),
        migrations.AlterModelOptions(
            name='artbookindex',
            options={'ordering': ('artbook__title', 'page')},
        ),
        migrations.AlterModelOptions(
            name='artwork',
            options={'ordering': ('name',)},
        ),
        migrations.RemoveField(
            model_name='edition',
            name='format_id',
        ),
        migrations.RemoveField(
            model_name='edition',
            name='genre_id',
        ),
        migrations.AddField(
            model_name='edition',
            name='format',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Format'),
        ),
        migrations.AddField(
            model_name='edition',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Genre'),
        ),
    ]
