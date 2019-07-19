# -*- coding: utf-8 -*-

from base64 import urlsafe_b64encode, urlsafe_b64decode
from datetime import datetime
from .compat import b, s,is_py2,is_py3
import json
import time
import base64


try:
    import zlib
    binascii = zlib
except ImportError:
    zlib = None
    import binascii

def url_encode(str):
    if is_py2:
        import urllib2
        return urllib2.quote(str)
    elif is_py3:
        import urllib.parse
        return urllib.parse.quote(str)

def image_base64_encode(file):
    with open(file, 'rb') as f:  # open（‘这里是图片地址’，‘这个打开模式读’）
        return str(base64.b64encode(f.read()),'utf-8')

def image_base64_decode(image_file,b64str):
    with open(image_file, 'wb') as f:  # open（‘这里是图片地址’，‘这个打开模式读’）
        f.write(base64.b64decode(b64str))
        return image_file


def urlsafe_base64_encode(data):
    """urlsafe的base64编码:
    对提供的数据进行urlsafe的base64编码。规格参考：
    https://developer.qiniu.com/kodo/manual/1231/appendix#1
    Args:
        data: 待编码的数据，一般为字符串
    Returns:
        编码后的字符串
    """
    ret = urlsafe_b64encode(b(data))
    return s(ret)


def urlsafe_base64_decode(data):
    """urlsafe的base64解码:
    对提供的urlsafe的base64编码的数据进行解码
    Args:
        data: 待解码的数据，一般为字符串
    Returns:
        解码后的字符串。
    """
    ret = urlsafe_b64decode(s(data))
    return ret


def rfc_from_timestamp(timestamp):
    """将时间戳转换为HTTP RFC格式
    Args:
        timestamp: 整型Unix时间戳（单位秒）
    """
    last_modified_date = datetime.utcfromtimestamp(timestamp)
    last_modified_str = last_modified_date.strftime(
        '%a, %d %b %Y %H:%M:%S GMT')
    return last_modified_str