# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-15 07:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hostmanager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='business_id',
            new_name='business',
        ),
    ]