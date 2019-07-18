# -*- coding: utf-8 -*-

from base64 import urlsafe_b64encode, urlsafe_b64decode
from datetime import datetime
from .compat import b, s,is_py2,is_py3
import json
import time


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

class InfoRecode(object):
    def __init__(self,path=None,tag=None,file='record.log'):
        file_name = '{0}_{1}'.format(tag,file) if tag else file
        self.file = '{0}/{1}'.format(path,file_name) if path else file_name

    def add_record(self, op,info):
        re_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        line = {
            'timestamp':re_time,
            'op':op,
            'info':info
        }
        with open(self.file, 'a+', encoding='utf-8', newline='') as f:
            #print(json.dumps(line))
            f.write(json.dumps(line,indent=4) + '\n')

class HorizionTestBase(object):
    def __init__(self,log_path=None,log_tag=None,log_file=None):
        self.log = log_path
        self.note = InfoRecode(log_path,log_tag,log_file)

    @classmethod
    def __writelog(self,re,op):
        for i in re:
            print(i)
        self.note.add_record(op,re[0]) if re[0] else self.note.add_record(op,re[1].error)


    def test_fdb_build(self,fdb):
        name = 'office-3'
        discription = 'test office facesets'
        op = 'test facesets build'
        re = fdb.build(name,discription)

        self.__writelog(re,op)

    def test_fdb_delete(self,fdb):
        facesets_id = '5d303c19f67f1000085b1f27'
        op = 'test facesets build'
        re = fdb.delete(facesets_id)

        self.__writelog(re,op)
    def test_fdb_update(self,fdb):
        facesets_id = '5d3029a7a21c33000804b8e4'
        name = 'update-ttt'
        op = 'test facesets info update'
        re = fdb.update(facesets_id,name=name)

        self.__writelog(re, op)

    def test_fdb_search(self,fdb):
        facesets_id = '5d3029a7a21c33000804b8e4'
        op = 'test facesets search by facesets_id'
        re = fdb.search(facesets_id)

        self.__writelog(re,op)

    def test_fdb_list(self, fdb):
        op = 'test facesets list'
        re = fdb.list()

        self.__writelog(re,op)