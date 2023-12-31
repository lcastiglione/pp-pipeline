﻿"""Módulo con la implementación para hacer peticiones http asincríncas con la librería aiohttp"""

import traceback
from typing import Any, Dict, Optional, Union, AsyncGenerator, Callable
import aiohttp
from pipeline.core.http.exceptions import ResponseHTTPException
from pipeline.core.http.httpclient import AbstractHttpClient


class AiohttpClient(AbstractHttpClient):
    """Implementación de la clase abstracta AbstractHttpClient para la librería aiohttp

    Args:
        AbstractHttpClient (_type_): Clase abstracta que define las funciones a implementar
    """

    def __init__(self):
        self._session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Obtener (o crear) la sesión actual."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _request(self,
                       method: str,
                       url: str,
                       chunk_size: int = 0,
                       **kwargs: Any) -> Union[Dict, str, Callable]:
        response = None
        try:
            session=await self._get_session()
            response = await session.request(method, url, **kwargs)
            response.raise_for_status()

            if chunk_size > 0:
                # Devuelve una función generadora para que el usuario la itere
                return lambda: self._requests_stream(response, chunk_size)
            content_type = response.headers['Content-Type']
            if 'application/json' in content_type:
                result = await response.json()  # Devuelve un objeto JSON
            else:
                result = await response.text()  # Devuelve un string por defecto
            await response.release()
            return result
        except Exception as exc:
            #print(exc)
            #traceback.print_exception(exc)
            if response:
                await response.release()
            raise ResponseHTTPException(str(exc), url, method) from exc

    async def _requests_stream(self, response: aiohttp.ClientResponse, chunk_size: int) -> AsyncGenerator[bytes, None]:
        try:
            async for chunk in response.content.iter_chunked(chunk_size):
                yield chunk
        finally:
            await response.release()

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        return await self._request('GET', url, params=params, **kwargs)

    async def post(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        return await self._request('POST', url, data=data, **kwargs)

    async def put(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        return await self._request('PUT', url, data=data, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Any:
        return await self._request('DELETE', url, **kwargs)

    async def get_session_cookies(self) -> Dict[str, str]:
        """Obtiene las cookies de la sesión actual."""
        session=await self._get_session()
        return {cookie.key: cookie.value for cookie in session.cookie_jar}

    async def close(self) -> None:
        """Cierra la sesión
        """
        if self._session:
            await self._session.close()
            self._session=None
