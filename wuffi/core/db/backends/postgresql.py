# -*- coding: utf-8 -*-

from aiopg.sa import create_engine

__all__ = (
    'connect',
)


async def connect(host='localhost', port=5432, user=None, password=None,
                  database=None, poolsize=10):
    """
    Creates a new engine instance with embedded connection pool.

    :param host: Address, either host or unix domain socket path
    :type host: str
    :param port: TCP port.
    :type port: int
    :param user: PostgreSQL database user
    :type user: str
    :param password: PostgreSQL database password
    :type password: str
    :param database: PostgreSQL database
    :type database: int
    :param poolsize: The number of parallel connections.
    :type poolsize: int
    """
    return await create_engine(host=host, port=port, user=user,
                               password=password, database=database,
                               minsize=poolsize, maxsize=poolsize)
