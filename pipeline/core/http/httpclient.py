"""Módulo con las clase abtsracta que deifne los métodos que tienen que tener todas las implementaciones que hacen peticiones HTTP"""

import abc
from typing import Any, Dict, Optional
import aiohttp


class AbstractHttpClient(abc.ABC):

    @abc.abstractmethod
    async def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        pass

    @abc.abstractmethod
    async def post(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        pass

    @abc.abstractmethod
    async def put(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
        pass

    @abc.abstractmethod
    async def delete(self, url: str, **kwargs: Any) -> Any:
        pass
