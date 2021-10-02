#!/usr/bin/env python3

import os
import uuid
import struct
import asyncio
import contextlib


SPOTIFLAG_SOCKET = os.getenv('SPOTIFLAG_SOCKET')


class Spotiflag:
    @contextlib.asynccontextmanager
    async def connect_with_id(id: uuid.UUID):
        reader, writer = await asyncio.open_unix_connection(SPOTIFLAG_SOCKET)

        id_data = str(id).encode()
        id_data_length = struct.pack('<Q', len(id_data))

        writer.write(id_data_length)
        writer.write(id_data)
        await writer.drain()

        yield reader, writer

        writer.close()

    @staticmethod
    async def generate(id: uuid.UUID, description: bytes):
        async with Spotiflag.connect_with_id(id) as (reader, writer):
            description_length = struct.pack('<Q', len(description))

            writer.write(b'GENERATE')
            writer.write(description_length)
            writer.write(description)
            await writer.drain()

            await reader.readexactly(8)

    @staticmethod
    async def read(id: uuid.UUID, offset: int):
        async with Spotiflag.connect_with_id(id) as (reader, writer):
            offset_data = struct.pack('<Q', offset)

            writer.write(b'READREAD')
            writer.write(offset_data)
            await writer.drain()

            response = await reader.readexactly(8)

            if response == b'NOTFOUND':
                return None

            size = struct.unpack('<Q', response)[0]

            return await reader.readexactly(size)
