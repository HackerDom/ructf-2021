#!/usr/bin/env python3

import uuid
import typing
import aiohttp

from aiohttp import web_exceptions


class MumbleException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


def ApiSession(timeout: int) -> typing.AsyncContextManager[aiohttp.ClientSession]:
    skip_headers = ['User-Agent']
    client_timeout = aiohttp.ClientTimeout(total=timeout)

    return aiohttp.ClientSession(timeout=client_timeout, skip_auto_headers=skip_headers)


class Spotiflag:
    PORT = 17171

    def __init__(self, hostname: str, timeout: int):
        self.url = f'http://{hostname}:{self.PORT}'
        self.timeout = timeout

    async def ping(self, answer: str='pong') -> None:
        url = f'{self.url}/api/ping/'

        async with ApiSession(self.timeout) as session:
            async with session.get(url) as response:
                if response.status != web_exceptions.HTTPOk.status_code:
                    raise MumbleException(f'/api/ping/: returns {response.status}')

                try:
                    data = await response.text()
                except Exception:
                    raise MumbleException(f'/api/ping/: can\'t get text')

        if data != answer:
            raise MumbleException(f'/api/ping/: incorrect answer')

    async def list(self) -> typing.List[str]:
        url = f'{self.url}/api/list/'

        async with ApiSession(self.timeout) as session:
            async with session.get(url) as response:
                if response.status != web_exceptions.HTTPOk.status_code:
                    raise MumbleException(f'/api/list/: returns {response.status}')

                try:
                    data = await response.json()
                except Exception:
                    raise MumbleException(f'/api/list/: can\'t get json')

        if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
            raise MumbleException(f'/api/list/: invalid json structure')

        return data

    async def generate(self, description: bytes) -> uuid.UUID:
        url = f'{self.url}/api/generate/'

        async with ApiSession(self.timeout) as session:
            async with session.post(url, data=description) as response:
                if response.status != web_exceptions.HTTPOk.status_code:
                    raise MumbleException(f'/api/generate/: returns {response.status}')

                try:
                    data = await response.text()
                except Exception:
                    raise MumbleException(f'/api/generate/: can\'t get id')

        try:
            id = uuid.UUID(data.strip(), version=4)
        except Exception:
            raise MumbleException(f'/api/generate/: invalid id format')

        return id

    async def listen(
            self,
            id: uuid.UUID,
            chunks_count: int,
            expected_chunk_size: int=64 * 1024
    ) -> typing.Optional[bytes]:
        url = f'{self.url}/api/listen/{id}/'
        chunks = []

        async with ApiSession(self.timeout) as session:
            offset = 0

            for i in range(chunks_count):
                session.headers.update({
                    'Range': f'bytes={offset}-'
                })

                async with session.get(url) as response:
                    if response.status == web_exceptions.HTTPNotFound.status_code:
                        return None

                    if response.status != web_exceptions.HTTPPartialContent.status_code:
                        raise MumbleException(f'/api/listen/: returns {response.status}')

                    try:
                        chunk = await response.read()
                    except Exception:
                        raise MumbleException(f'/api/listen/: can\'t get content')

                if len(chunk) != expected_chunk_size:
                    raise MumbleException(f'/api/listen/: incorrect content size')

                chunks.append(chunk)
                offset += len(chunk)

        return b''.join(chunks)
