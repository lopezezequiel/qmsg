# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-20 04:05
from __future__ import unicode_literals

import apirestv1.models
import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.CharField(default=apirestv1.models.get_id, editable=False, max_length=8, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(code='nomatch', message='It has to be a string of 12 hexadecimal characters', regex=re.compile('^[0-9a-f]{8}$'))])),
                ('text', models.CharField(blank=True, max_length=2000)),
            ],
        ),
    ]
