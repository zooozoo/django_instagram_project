# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 12:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20171023_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='like_post',
            new_name='like_posts',
        ),
    ]