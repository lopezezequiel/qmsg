# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import uuid

from django.core.validators import RegexValidator
from django.db import models


def get_id():
    return str(uuid.uuid1()).split('-')[0]


class Message(models.Model):
    """Representa un mensaje que tiene un id de 8 digitos hexadecimales
    y un texto de hasta 2000 caracteres
    """

    id = models.CharField(
        primary_key=True, default=get_id,
        editable=False, validators=[RegexValidator(
            regex=re.compile('^[0-9a-f]{8}$'),
            message='It has to be a string of 12 hexadecimal characters',
            code='nomatch')], max_length=8)
    text = models.CharField(max_length=2000, blank=True)
