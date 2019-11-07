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
        #print (response.getheaders())#测试用的
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
    mypath = 'C:\\Users\\成功\\Desktop\\新建文件夹'
    f = []
    list2 = list()
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        filename_list = filenames
        MD5_list = [None] * len(filename_list)  # 注意这里面需要初始化list1大小的空列表,必须这样，要不它就报错，报关于超出列表范围的错
        break
    for i in range(len(filename_list)):  # 用i循环，将文件名写入列表里
        # print(filename_list[i]+'文件的MD5值是')#测试用的
        filepath = 'C:\\Users\\成功\\Desktop\\新建文件夹\\' + filename_list[i]
        # print(GetFileMd5(filepath))#测试用的
        MD5_list[i] = GetFileMd5(filepath)
        name_md5.update(zip(filename_list,
                            MD5_list))  # 注意这里面不能只用update函数，不能用类似于update(键=值)这样会报错，如果写filename_list[i],MD5_list[i]会报参数个数的错。目前我知道的只能用zip函数
        # print(name_md5)#测试用的
    print(name_md5)
    post_filename_MD5()






    # i=0
    # while i < 3:
    #     try:
    #         r = requests.get(real_url, stream=True,timeout=(5, 10))#设置5秒的连接超时设置，和10秒的读取超时设置，设置读取超时的目的是防止服务器端出现问题后陷入卡死状态。
    #         print(r)
    #         return
    #     except requests.exceptions.RequestException as e:
    #         print(e)
    #         i += 1