# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from models import Message
from serializers import MessageSerializer


def index(request):
    """Renderiza la página princial
    """
    return render(request, 'apirestv1/index.html') 


@api_view(['POST'])
def post_message(request):
    """Recibe un mensaje codificado en json, lo guarda en base de datos
    y lo retorna con el id seteado
    """

    serializer = MessageSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    message = Message.objects.create(**serializer.validated_data)
    message.save()

    serializer = MessageSerializer(message)

    return Response(serializer.data)


@api_view(['GET'])
def get_message(request, id):
    """Devuelve un mensaje y lo elimina de base de datos
    """

    try:
        message = Message.objects.get(pk=id)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    response = MessageSerializer(message).data

    message.delete()

    return Response(response)
