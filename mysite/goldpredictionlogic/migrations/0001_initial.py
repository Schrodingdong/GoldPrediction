# Generated by Django 4.0.6 on 2022-07-13 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoldPricePredictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open', models.DecimalField(decimal_places=4, max_digits=15)),
                ('high', models.DecimalField(decimal_places=4, max_digits=15)),
                ('low', models.DecimalField(decimal_places=4, max_digits=15)),
                ('close', models.DecimalField(decimal_places=4, max_digits=15)),
                ('volume', models.IntegerField()),
                ('currency', models.CharField(max_length=6)),
            ],
        ),
    ]
