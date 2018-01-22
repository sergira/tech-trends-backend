# Generated by Django 2.0.1 on 2018-01-22 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0003_auto_20180122_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='company',
            field=models.ForeignKey(default='UNDEFINED', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='news_articles', to='db_api.Company'),
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='tag',
            field=models.ManyToManyField(related_name='news_articles', to='db_api.Tag'),
        ),
    ]
