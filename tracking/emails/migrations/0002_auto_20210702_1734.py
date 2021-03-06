# Generated by Django 3.2 on 2021-07-02 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtracking',
            name='click_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='emailtracking',
            name='destination_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='emailtracking',
            name='first_click_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='emailtracking',
            name='latest_click_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
