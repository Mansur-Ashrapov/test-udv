import sys
from pathlib import Path

import aioredis

file = Path(__file__).resolve()  
package_root_directory = file.parents[1]  
sys.path.append(str(package_root_directory))  


from typing import Any
from unittest import mock

import pytest
from multidict import MultiDict
from yarl import URL

import aiohttp
from aiohttp import Fingerprint, ServerFingerprintMismatch, hdrs, web
from aiohttp.abc import AbstractResolver
from aiohttp.client_exceptions import TooManyRedirects
from aiohttp.test_utils import unused_port

from app.routes.update_db_routes import update_db


async def test_post_new_valutes_succes_with_zero_merge(aiohttp_client: Any) -> None:
    app = web.Application()
    app['db'] = aioredis.from_url(
        'redis://redis_db', 
        password='password',
        decode_responses=True
    )
    app.route.add_route('POST', '/database', update_db)

    connector = aiohttp.TCPConnector(limit=1)
    client = await aiohttp_client(app, connector=connector)

    resp = client.post('/databa')


async def test_keepalive_two_requests_success(aiohttp_client: Any) -> None:
    async def handler(request):
        body = await request.read()
        assert b"" == body
        return web.Response(body=b"OK")

    app = web.Application()
    app.router.add_route("GET", "/", handler)

    connector = aiohttp.TCPConnector(limit=1)
    client = await aiohttp_client(app, connector=connector)

    resp1 = await client.get("/")
    await resp1.read()
    resp2 = await client.get("/")
    await resp2.read()

    assert 1 == len(client._session.connector._conns)
