# -*- coding: utf-8 -*-

import asyncio_redis

__all__ = (
    'connect',
)


async def connect(host='localhost', port=6379, password=None, db=0,
                  poolsize=1, auto_reconnect=True):
    """
    Create a new connection pool instance.

    :param host: Address, either host or unix domain socket path
    :type host: str
    :param port: TCP port. If port is 0 then host assumed to be unix socket path
    :type port: int
    :param password: Redis database password
    :type password: bytes
    :param db: Redis database
    :type db: int
    :param poolsize: The number of parallel connections.
    :type poolsize: int
    :param auto_reconnect: Enable auto reconnect
    :type auto_reconnect: bool
    """
    return await asyncio_redis.Pool.create(host=host, port=port,
                                           password=password, db=db,
                                           poolsize=poolsize,
                                           auto_reconnect=auto_reconnect)