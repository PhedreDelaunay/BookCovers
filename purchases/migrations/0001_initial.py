# Generated by Django 3.0.1 on 2020-02-09 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookcovers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owned',
            fields=[
                ('owned_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchase_date', models.CharField(blank=True, max_length=10, null=True)),
                ('title', models.CharField(max_length=100)),
                ('author_name', models.CharField(max_length=255)),
                ('artist_name', models.CharField(blank=True, max_length=255, null=True)),
                ('publisher_year', models.CharField(blank=True, max_length=100, null=True)),
                ('print_run', models.CharField(blank=True, max_length=25, null=True)),
                ('series', models.CharField(blank=True, max_length=255, null=True)),
                ('imprint', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.CharField(blank=True, max_length=25, null=True)),
                ('isfdb', models.CharField(blank=True, max_length=50, null=True)),
                ('cost', models.CharField(blank=True, max_length=25, null=True)),
                ('total_cost', models.CharField(blank=True, max_length=50, null=True)),
                ('purchased_from', models.CharField(blank=True, max_length=50, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
                ('artist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Artist')),
                ('artwork', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Artwork')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Author')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Book')),
                ('book_series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.BookSeries')),
                ('cover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Cover')),
                ('edition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Edition')),
                ('set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bookcovers.Set')),
            ],
            options={
                'db_table': 'purchases_owned',
            },
        ),
    ]
