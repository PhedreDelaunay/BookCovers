# Generated by Django 2.1.1 on 2019-01-03 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookcovers', '0007_auto_20181202_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintRuns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('print_run_id', models.IntegerField()),
                ('order', models.IntegerField()),
                ('print', models.CharField(blank=True, max_length=255, null=True)),
                ('cover_price', models.CharField(blank=True, max_length=255, null=True)),
                ('num_pages', models.IntegerField(blank=True, null=True)),
                ('print_year', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'print_runs',
            },
        ),
        migrations.AlterField(
            model_name='artistakas',
            name='artist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theArtist_akas', related_query_name='theArtist_aka', to='bookcovers.Artists'),
        ),
        migrations.AlterField(
            model_name='artworks',
            name='artist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theArtworks', related_query_name='theArtwork', to='bookcovers.Artists'),
        ),
        migrations.AlterField(
            model_name='artworks',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theArtworks', related_query_name='theArtwork', to='bookcovers.Books'),
        ),
        migrations.AlterField(
            model_name='authorakas',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theAuthor_akas', related_query_name='theAuthor_aka', to='bookcovers.Authors'),
        ),
        migrations.AlterField(
            model_name='books',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theBooks', related_query_name='theBook', to='bookcovers.Authors'),
        ),
        migrations.AlterField(
            model_name='covers',
            name='artwork',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theCovers', related_query_name='theCover', to='bookcovers.Artworks'),
        ),
        migrations.AlterField(
            model_name='covers',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theCovers', related_query_name='theCover', to='bookcovers.Books'),
        ),
        migrations.AlterField(
            model_name='covers',
            name='edition',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theCover', related_query_name='theCover', to='bookcovers.Editions'),
        ),
        migrations.AlterField(
            model_name='editions',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theEditions', related_query_name='theEdition', to='bookcovers.Books'),
        ),
        migrations.AlterField(
            model_name='editions',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='theEditions', related_query_name='theEdition', to='bookcovers.Countries'),
        ),
        migrations.AddField(
            model_name='printruns',
            name='cover',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='thePrintRun', related_query_name='thePrintRun', to='bookcovers.Covers'),
        ),
        migrations.AddField(
            model_name='printruns',
            name='edition',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='thePrintRun', related_query_name='thePrintRun', to='bookcovers.Editions'),
        ),
        migrations.AlterUniqueTogether(
            name='printruns',
            unique_together={('print_run_id', 'order')},
        ),
    ]