# Generated by Django 2.2 on 2019-05-04 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0002_auto_20190504_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owned',
            name='edition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Edition'),
        ),
    ]
