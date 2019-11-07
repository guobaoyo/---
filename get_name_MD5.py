import http.client
import hashlib
import os
import downloadfile
import time
httpClient = None
local_name_MD5_dict = dict()
server_name_MD5_dict = dict()
from os import walk

def Get_server_name_MD5():
    try:
        httpClient = http.client.HTTPConnection('localhost', 8080, timeout=10)
        httpClient.request('GET', '/getfileinfo/')

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        # print(response.status)
        # print (response.reason)
        # return response.read()
        # server_name_MD5 = response.read()
        #print("**********************")
        #print(server_name_MD5)
        server_name_md5_temp = response.read()
        server_name_md5_temp_string = str(server_name_md5_temp, 'utf-8')  # 必须将bytes转为str的形式才能用正则表达式
        server_name_MD5_dict = eval(server_name_md5_temp_string)  # 将字符串的形式转为字典形式
        return server_name_MD5_dict
    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()

def Get_Local_single_FileMd5(filename):#返回单个文件的MD5值
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()#定义myhash为本地的md5加密值
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
def Get_Local_name_MD5(localfilepath):#返回这个文件夹下的文件名，并且挨着调用Get_Local_single_FileMd5(filename)
    filename_list = []
    list2 = list()
    for (dirpath, dirnames, file__names) in walk(localfilepath):
        filename_list.extend(file__names)
        MD5_list = [None] * len(file__names)  # 注意这里面需要初始化list1大小的空列表,必须这样，要不它就报错，报关于超出列表范围的错
        filename_list = file__names#在for之后写这句，这样可以得到
        break
    for i in range(len(filename_list)):  # 用i循环，将文件名写入列表里
        filepath = localfilepath+'\\' + filename_list[i]
        MD5_list[i] = Get_Local_single_FileMd5(filepath)
        local_name_MD5_dict.update(zip(filename_list,MD5_list))  # 注意这里面不能只用update函数，不能用类似于update(键=值)这样会报错，如果写filename_list[i],MD5_list[i]会报参数个数的错。目前我知道的只能用zip函数
        # print(name_md5)#测试用的
    return local_name_MD5_dict

def Delete_download_list(dict1,dict2):
    local_name_list = list(dict1.keys())#传入dict1的键为local_name_list这个列表
    server_name_list = list(dict2.keys())
    print("本地文件名列表为")
    print(local_name_list)#输出验证
    print("服务器端文件名列表为")
    print(server_name_list)
    delete_list = []
    download_list = []#首先把服务器字典的每个键拿出来跟客户端进行比较：
    for i in server_name_list:
        if i not in local_name_list:
            download_list.append(i)#    如果服务器有客户端不存在的键，记录这部分键。
    for i in local_name_list:
        if i not in server_name_list:
            delete_list.append(i)#    如果客户端有服务器端不存在的键，直接删掉。
            local_name_list.remove(i)
    for i in local_name_list:
        for j in server_name_list:
            if (i == j and local_name_MD5_dict[i] != server_name_MD5_dict[j]):
                download_list.append(i)#返回一个[文件名1，文件名2...]的列表
    return download_list,delete_list#返回两个列表

def downloading(download_list_temp):
    for i in download_list_temp:
        downloadfile.downloadfile(file_name=i)
    print("下载完毕")

def deleting(delete_list_temp):
    for i in delete_list_temp:
        delete_path = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径
        delete_path = delete_path+'\\'+'download\\'+i#将文件名加到路径底下
        os.remove(delete_path)#删除这部分文件
    print("删除完毕")

if __name__ == '__main__':
    start_time = time.time()
    localfilepath_temp = os.path.abspath(os.path.dirname(__file__))#返回绝对路径
    localfilepath_real = localfilepath_temp+'\\download'
    print(localfilepath_real)
    print("本地文件的文件名及MD5值是")
    local_name_MD5_dict = Get_Local_name_MD5(localfilepath_real)#输出本地文件的文件名和MD5值
    print(local_name_MD5_dict)
    print("服务器端的文件名及MD5值为")
    server_name_MD5_dict = Get_server_name_MD5()#输出服务器端文件的文件名和MD5值
    print(server_name_MD5_dict)
    download_list, delete_list = Delete_download_list(local_name_MD5_dict,server_name_MD5_dict)
    print("下载的文件列表为")
    print(download_list)
    print("删除的文件列表为")
    print(delete_list)
    if delete_list:
        deleting(delete_list)#调用删除列表
    if download_list:
        downloading(download_list)#反复调用下载函数
    end_time = time.time()
    print("同步完毕,共耗时"+str(end_time-start_time)+"s")

