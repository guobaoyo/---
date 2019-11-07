#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf-8 -*-
import urllib.parse, http.client
import hashlib
import os
import datetime
from os import walk

httpClient = None
def post_filename_MD5():
    try:
        params = urllib.parse.urlencode(name_md5)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        httpClient = http.client.HTTPConnection('localhost', 8080, timeout=10)
        httpClient.request('POST', '/compare/', params, headers)
        response = httpClient.getresponse()
        print (response.status)
        print (response.reason)
        #print (response.getheaders())#�����õ�
    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()

name_md5 = dict()
def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
if __name__ == '__main__':
    mypath = 'C:\\Users\\�ɹ�\\Desktop\\�½��ļ���'
    f = []
    list2 = list()
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        filename_list = filenames
        MD5_list = [None] * len(filename_list)  # ע����������Ҫ��ʼ��list1��С�Ŀ��б�,����������Ҫ�����ͱ��������ڳ����б�Χ�Ĵ�
        break
    for i in range(len(filename_list)):  # ��iѭ�������ļ���д���б���
        # print(filename_list[i]+'�ļ���MD5ֵ��')#�����õ�
        filepath = 'C:\\Users\\�ɹ�\\Desktop\\�½��ļ���\\' + filename_list[i]
        # print(GetFileMd5(filepath))#�����õ�
        MD5_list[i] = GetFileMd5(filepath)
        name_md5.update(zip(filename_list,
                            MD5_list))  # ע�������治��ֻ��update������������������update(��=ֵ)�����ᱨ�����дfilename_list[i],MD5_list[i]�ᱨ���������Ĵ�Ŀǰ��֪����ֻ����zip����
        # print(name_md5)#�����õ�
    print(name_md5)
    post_filename_MD5()






    # i=0
    # while i < 3:
    #     try:
    #         r = requests.get(real_url, stream=True,timeout=(5, 10))#����5������ӳ�ʱ���ã���10��Ķ�ȡ��ʱ���ã����ö�ȡ��ʱ��Ŀ���Ƿ�ֹ�������˳�����������뿨��״̬��
    #         print(r)
    #         return
    #     except requests.exceptions.RequestException as e:
    #         print(e)
    #         i += 1