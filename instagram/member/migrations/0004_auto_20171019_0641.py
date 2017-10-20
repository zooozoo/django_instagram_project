# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 06:41
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations
import member.models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_user_age'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('onjects', member.models.UserManager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
