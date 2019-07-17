#!/usr/bin/env python
#-.- coding=utf-8 -.-
'''
__author__ = 'caeser'
__mtime__ = '2019/7/16'
'''

API_HOST = 'api-aiot.horizon.ai'

_config = {
    'default_requet_host': API_HOST,
    'connection_timeout': 30,
    'connection_retries': 3,
    'connection_pool': 10,
}

def get_default(key):
    return _config[key]

def set_default(
        default_requet_host=None, connection_retries=None, connection_pool=None, connection_timeout=None):
    if default_requet_host:
        _config['default_requet_host'] = default_requet_host
    if connection_retries:
        _config['connection_retries'] = connection_retries
    if connection_pool:
        _config['connection_pool'] = connection_pool
    if connection_timeout:
        _config['connection_timeout'] = connection_timeout