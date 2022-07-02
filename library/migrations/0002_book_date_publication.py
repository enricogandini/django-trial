# Generated by Django 4.0.4 on 2022-07-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='date_publication',
            field=models.DateField(blank=True, help_text='The publication date of a book. If only the year is available, by default use the 1st of January of that year.', null=True),
        ),
    ]
