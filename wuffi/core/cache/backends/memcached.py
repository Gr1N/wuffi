# -*- coding: utf-8 -*-

import aiomcache

__all__ = (
    'connect',
)


async def connect(host='localhost', port=11211, poolsize=1):
    """
    Create a new connection pool instance.

    :param host: Address, either host or unix domain socket path
    :type host: str
    :param port: TCP port.
    :type port: int
    :param poolsize: The number of parallel connections.
    :type poolsize: int
    """
    return aiomcache.Client(host, port=port, pool_size=poolsize)
