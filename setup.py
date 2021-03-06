# -*- coding: utf-8 -*-

from io import open
from setuptools import setup, find_packages


setup(
    name='wuffi',
    version='0.0.0',
    description='TBD',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Nikita Grishko',
    author_email='grin.minsk+github@gmail.com',
    url='https://github.com/Gr1N/wuffi',
    download_url='TBD',
    license='MIT',
    packages=find_packages(exclude=(
        'tests.*',
        'tests',
        'example',
    )),
    install_requires=(
        'aiohttp==0.21.5',
        'aiohttp-jinja2==0.7.0',
        'alembic==0.8.6',
        'Cerberus==0.9.2',
        'SQLAlchemy==1.0.12',
    ),
    extras_require={
        'memcached': (
            'aiomcache==0.3.0',
        ),
        'mysql': (
            'aiomysql==0.0.7',
        ),
        'postgresql': (
            'aiopg==0.9.2',
        ),
        'redis': (
            'asyncio-redis==0.14.2',
        ),
        'sentry': (
            'raven==5.13.0',
            'raven-aiohttp==0.2.0',
        ),
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    )
)
