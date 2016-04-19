# -*- coding: utf-8 -*-

from aiomysql.sa import create_engine

__all__ = (
    'connect',
)


async def connect(host='localhost', port=3306, user=None, password=None,
                  database=None, autocommit=True, poolsize=10):
    """
    Creates a new engine instance with embedded connection pool.

    :param host: Address, either host or unix domain socket path
    :type host: str
    :param port: TCP port.
    :type port: int
    :param user: MySQL database user
    :type user: str
    :param password: MySQL database password
    :type password: str
    :param database: MySQL database
    :type database: int
    :param autocommit: Autocommit mode. None means use server default.
    :type autocommit: bool or None
    :param poolsize: The number of parallel connections.
    :type poolsize: int
    """
    return await create_engine(host=host, port=port, user=user,
                               password=password, db=database,
                               autocommit=autocommit,
                               minsize=poolsize, maxsize=poolsize)
