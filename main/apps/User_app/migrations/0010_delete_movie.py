# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-31 20:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeApp', '0003_auto_20170831_2038'),
        ('User_app', '0009_auto_20170827_0113'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Movie',
        ),
    ]