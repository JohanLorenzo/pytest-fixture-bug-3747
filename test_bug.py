import asyncio
import aiohttp
import pytest

from unittest import mock

class FakeResponse(aiohttp.client_reqrep.ClientResponse):
    def __init__(self, *args, **kwargs):
        pass

    @asyncio.coroutine
    def release(self):
        return


@pytest.mark.asyncio
@pytest.fixture(scope='function')
async def fake_session():
    @asyncio.coroutine
    def _fake_request(method, url, *args, **kwargs):
        resp = FakeResponse(method, url)
        resp._history = (FakeResponse(method, url, status=302),)
        return resp

    session = aiohttp.ClientSession()
    session._request = _fake_request
    yield session
    await session.close()


@pytest.mark.asyncio
async def test_bug(fake_session):
    async with fake_session.put('some_url') as resp:
        pass
