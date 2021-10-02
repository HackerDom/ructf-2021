#!/usr/bin/env python3

import os
import re
import uuid

from redis import Redis
from fastapi import FastAPI, Header, status
from fastapi.requests import Request
from fastapi.responses import Response, FileResponse
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles

from spotiflag import Spotiflag


PREFIX = 'spotiflag_'

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
redis = Redis(os.getenv('REDIS_ADDRESS'))
expire = int(os.getenv('EXPIRE'))

app.mount("/static", StaticFiles(directory="static"))


@app.route('/')
async def main(_: Request):
    return FileResponse('index.html')


@app.post('/api/generate/')
async def api_generate(request: Request):
    max_description_length = 16 * 1024

    description = await request.body()

    if not 0 < len(description) <= max_description_length:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    id = uuid.uuid4()

    await Spotiflag.generate(id, description)

    redis.set(f'{PREFIX}{id}', 1, ex=expire)

    return Response(str(id))


@app.get('/api/listen/{id}/')
async def api_listen(id: uuid.UUID, range: str=Header(...)):
    offset = int(re.search(r'\d+', range).group(0))

    if redis.get(f'{PREFIX}{id}') is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    data = await Spotiflag.read(id, offset)

    if data is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    new_range = f'bytes {offset}-{offset + len(data)}/{offset + 2 * len(data)}'

    return Response(
        data,
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        media_type='audio/wav',
        headers={
            'Content-Range': new_range,
        }
    )


@app.get('/api/list/')
async def api_list():
    keys = redis.keys(f'{PREFIX}*')

    return [key.decode().removeprefix(PREFIX) for key in keys]
