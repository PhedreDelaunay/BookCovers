# Generated by Django 2.1.1 on 2019-01-03 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookcovers', '0008_auto_20190103_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printruns',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='thePrintRuns', related_query_name='thePrintRun', to='bookcovers.Covers'),
        ),
    ]