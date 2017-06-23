# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializador/Deserialiador de mensajes
    El campo id es de solo lectura
    """

    class Meta:
        model = Message 
        fields = (u'id', u'text')
        extra_kwargs = {
            u'id': {u'read_only': True}
        }
