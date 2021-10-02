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


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
redis = Redis(os.getenv('REDIS_ADDRESS'))
expire = int(os.getenv('EXPIRE'))

app.mount("/static", StaticFiles(directory="static"))


@app.route('/')
async def main(_: Request):
    return FileResponse('index.html')


@app.route('/api/ping/')
async def ping(_: Request):
    return Response('pong')


@app.post('/api/generate/')
async def api_generate(request: Request):
    max_description_length = 16 * 1024

    description = await request.body()

    if not 0 < len(description) <= max_description_length:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    id = uuid.uuid4()

    await Spotiflag.generate(id, description)

    redis.set(str(id), 1, ex=expire)

    return Response(str(id))


@app.get('/api/listen/{id}/')
async def api_listen(id: uuid.UUID, range: str=Header(...)):
    offset = int(re.findall(r'\d+', range)[0])

    if redis.get(str(id)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    data = await Spotiflag.read(id, offset)

    if data is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    new_start = offset
    new_end = offset + len(data)
    new_length = new_end + len(data)

    return Response(
        data,
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        media_type='audio/wav',
        headers={
            'Content-Range': f'bytes {new_start}-{new_end}/{new_length}',
            'Content-Length': f'{len(data)}',
        }
    )


@app.get('/api/list/')
async def api_list():
    return redis.keys('*')
