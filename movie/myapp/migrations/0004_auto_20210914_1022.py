# Generated by Django 3.2.6 on 2021-09-14 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_movie_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewermovie',
            name='review',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='viewermovie',
            name='rtime',
            field=models.DateTimeField(null=True),
        ),
    ]