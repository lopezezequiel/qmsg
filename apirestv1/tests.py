# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import IntegrityError
from django.test import Client
from django.test import TestCase

from models import Message


class MessageTestCase(TestCase):

    def setUp(self):
        self.root = '/api-rest/v1/messages'

    def test_message_params(self):
        """Prueba aceptación de parámetros correctos
        """
        Message().save()
        Message(id="0000ffff").save()
        Message(text="").save()
        Message(text="lorep ipsum").save()
        Message(id="ffff0000", text="lorep ipsum").save()
        Message(text='x' * 2000).save()

    def test_unique_constraint(self):
        """Prueba que no permita crear mensajes con ids duplicados
        """
        with self.assertRaises(IntegrityError):
            Message.objects.create(id="0000ffff")
            Message.objects.create(id="0000ffff")

    def test_id(self):
        """Valida que se genere un id válido cuando se crea un mensaje.
        formato válido: 8 caracteres hexadecimales.
        regexp: ^[0-9a-f]{8}$
        """

        message = Message(text="lorep ipsum")
        self.assertRegex(message.id, r'^[0-9a-f]{8}$')

    def test_collisions(self):
        """Valida que no haya colisiones entre ids autogenerados de
        mensajes que se crean en un corto periodo de tiempo
        """

        q = 10000
        ids = set([Message().id for i in range(q)])

        self.assertEqual(len(ids), q)

    def test_rest(self):
        """Prueba la api rest para Message
        """

        client = Client()
        data = {'text': 'hola'}
        json_data = json.dumps(data)
        # '{"text":"hola"}'

        response = client.post(
            self.root, data=json_data,
            content_type='application/json',
            HTTP_USER_AGENT='Mozilla/5.0',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        # '{"id":"b613e080","text":"hola"}'
        content = response.content

        # /api-rest/v1/messages/b613e080
        uri = '{0}/{1}'.format(self.root, response.json()['id'])

        response = client.get(uri)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, content)

        response = client.get(uri)
        self.assertEqual(response.status_code, 404)

    def test_bad_request(self):
        """Prueba que devuelva un http 400 si se envían datos inválidos
        """

        client = Client()
        data = {'text': 'x' * 2001}
        json_data = json.dumps(data)

        response = client.post(
            self.root, data=json_data,
            content_type='application/json',
            HTTP_USER_AGENT='Mozilla/5.0',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)

    def test_MITM(self):
        """Prueba que no se pueda setear el id de un mensaje a traves de
        la api rest
        """

        client = Client()

        message_id = 'FFFFFFFF'
        data = {'id': message_id, 'text': 'hola'}

        json_data = json.dumps(data)

        response = client.post(
            self.root, data=json_data,
            content_type='application/json',
            HTTP_USER_AGENT='Mozilla/5.0',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertNotEqual(response.json()['id'], message_id)
