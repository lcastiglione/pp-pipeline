"""Módulo con los tests unitarios de la implementación http aiohttp"""

import unittest
import io
from unittest.mock import AsyncMock
from aioresponses import aioresponses
from pipeline import AiohttpClient, http_exceptions


class TestAiohttpClient(unittest.IsolatedAsyncioTestCase):
    """_summary_
    """

    def __init__(self, methodName="runTest"):
        '''Inicializador de la clase TestAiohttpClient.
        '''
        super().__init__(methodName=methodName)
        self.client = None

    async def asyncSetUp(self):
        """Prepara el entorno para cada test asincrónico."""
        self.client = AiohttpClient()

    async def asyncTearDown(self):
        """Limpia el entorno después de cada test asincrónico."""
        await self.client.close()

    @aioresponses()
    async def test_get(self, mock):
        """Prueba el método GET de la clase AiohttpClient."""
        url = 'http://test.com'
        mock.get(url, status=200, payload={'success': True})

        response = await self.client.get(url)
        self.assertEqual(response, {'success': True})

    @aioresponses()
    async def test_post(self, mock):
        """Prueba el método POST de la clase AiohttpClient."""
        url = 'http://test.com'
        mock.post(url, status=200, payload={'success': True})

        response = await self.client.post(url, data={'test': 'data'})
        self.assertEqual(response, {'success': True})

    @aioresponses()
    async def test_put(self, mock):
        """Prueba el método PUT de la clase AiohttpClient."""
        url = 'http://test.com'
        mock.put(url, status=200, payload={'success': True})

        response = await self.client.put(url, data={'test': 'data'})
        self.assertEqual(response, {'success': True})

    @aioresponses()
    async def test_delete(self, mock):
        """Prueba el método DELETE de la clase AiohttpClient."""
        url = 'http://test.com'
        mock.delete(url, status=200, payload={'success': True})

        response = await self.client.delete(url)
        self.assertEqual(response, {'success': True})

    async def test_close(self):
        """Prueba el método close de la clase AiohttpClient."""
        client = AiohttpClient()
        original_close = client._session.close  # pylint: disable=W0212
        client._session.close = AsyncMock()  # pylint: disable=W0212
        await client.close()
        client._session.close.assert_called_once()  # pylint: disable=W0212
        client._session.close = original_close  # pylint: disable=W0212
        await client.close()

    @aioresponses()
    async def test_get_json(self, mock):
        """Prueba el método GET de la clase AiohttpClient para obtener una respuesta JSON."""
        url = 'http://test.com/json'
        mock.get(url, status=200, payload={'success': True}, headers={'Content-Type': 'application/json'})

        response = await self.client.get(url)
        self.assertEqual(response, {'success': True})

    @aioresponses()
    async def test_get_text(self, mock):
        """Prueba el método GET de la clase AiohttpClient para obtener una respuesta de texto."""
        url = 'http://test.com/text'
        mock.get(url, status=200, body='Hello, world!', headers={'Content-Type': 'text/plain'})

        response = await self.client.get(url)
        self.assertEqual(response, 'Hello, world!')

    @aioresponses()
    async def test_get_file(self, mock):
        '''Prueba el método GET de la clase AiohttpClient para obtener un archivo.'''
        url = 'http://test.com/file'
        # Para simular un archivo, usaremos un objeto BytesIO
        file_content = io.BytesIO(b'Some binary data')
        mock.get(url, status=200, body=file_content.read(), headers={'Content-Type': 'application/octet-stream'})
        # Hacemos la solicitud con chunk_size=1 para obtener un generador de contenido binario
        gen = await self.client.get(url, chunk_size=1)
        # Como gen es una función generadora, la llamamos para obtener el generador real
        response = b''.join([chunk async for chunk in gen()])
        self.assertEqual(response, b'Some binary data')

    @aioresponses()
    async def test_response_http_exception(self, mock):
        """Prueba que se lance la excepción ResponseHTTPException."""
        url = 'http://test.com'
        mock.get(url, status=404)

        with self.assertRaises(http_exceptions.ResponseHTTPException):
            await self.client.get(url)
