# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-03 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieApp', '0004_auto_20170903_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreview',
            name='episode_review',
            field=models.ManyToManyField(related_name='m_review_user', to='movieApp.EpisodeReview'),
        ),
        migrations.AddField(
            model_name='userreview',
            name='movie_review',
            field=models.ManyToManyField(related_name='m_review_user', to='movieApp.MovieReview'),
        ),
        migrations.AddField(
            model_name='userreview',
            name='tv_review',
            field=models.ManyToManyField(related_name='m_review_user', to='movieApp.TVReview'),
        ),
    ]
