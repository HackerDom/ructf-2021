#!/usr/bin/env python3

import os
import uuid
import typing
import struct
import asyncio
import aiohttp

from gornilo import Checker, Verdict, CheckRequest, PutRequest, GetRequest

from api import Spotiflag, MumbleException
from generator import random_text


checker = Checker()
timeout = 30
chunks_count = 8


def wrap_errors(func: typing.Callable[..., Verdict]) -> typing.Callable[..., Verdict]:
    async def wrapper(request):
        try:
            return await func(request)
        except aiohttp.ClientError:
            return Verdict.DOWN('service is down')
        except MumbleException as mumble:
            return Verdict.MUMBLE(mumble.message)

    wrapper.__name__ = func.__name__
    wrapper.__annotations__ = func.__annotations__

    return wrapper


async def song_generate(description: bytes) -> bytes:
    dir = os.path.dirname(os.path.realpath(__file__))
    exe = 'spotiflag/spotiflag'

    description_length = struct.pack('<Q', len(description))

    io = await asyncio.subprocess.create_subprocess_exec(
        os.path.join(dir, exe),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    io.stdin.write(description_length + description)
    await io.stdin.drain()

    data_length = struct.unpack('<Q', await io.stdout.readexactly(8))[0]

    data = await io.stdout.readexactly(data_length)

    return data


@checker.define_check
@wrap_errors
async def do_check(request: CheckRequest) -> Verdict:
    api = Spotiflag(request.hostname, timeout)

    await api.ping()

    description = random_text(128, 1024).encode()

    id, data_expected = await asyncio.gather(
        api.generate(description),
        song_generate(description),
    )

    if str(id) not in await api.list():
        return Verdict.MUMBLE('/api/list/: can\'t find song')

    data_actual = await api.listen(id, chunks_count)

    if data_actual is None:
        return Verdict.MUMBLE('/api/listen/: can\'t get song')

    if data_expected[:len(data_actual)] != data_actual:
        return Verdict.MUMBLE('invalid song')

    return Verdict.OK()


@checker.define_put(vuln_num=1, vuln_rate=1)
@wrap_errors
async def do_put(request: PutRequest) -> Verdict:
    api = Spotiflag(request.hostname, timeout)

    id = await api.generate(request.flag.encode())

    return Verdict.OK(str(id))


@checker.define_get(vuln_num=1)
@wrap_errors
async def do_get(request: GetRequest) -> Verdict:
    api = Spotiflag(request.hostname, timeout)

    id = uuid.UUID(request.flag_id.strip(), version=4)

    if str(id) not in await api.list():
        return Verdict.CORRUPT('/api/list/: can\'t find flag')

    data_actual, data_expected = await asyncio.gather(
        api.listen(id, chunks_count),
        song_generate(request.flag.encode()),
    )

    if data_actual is None:
        return Verdict.MUMBLE('/api/listen/: can\'t get flag')

    if data_expected[:len(data_actual)] != data_actual:
        return Verdict.CORRUPT('invalid flag')

    return Verdict.OK()


if __name__ == '__main__':
    checker.run()
