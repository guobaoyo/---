#下面的是下载文件，需要输入想要下载的文件名
import requests
import os
from os import walk
def downloadfile(file_name):
    real_url = 'http://localhost:8080/download/'+file_name

    i = 0
    while i < 3:
        try:
            r = requests.get(real_url, stream=True,timeout=(5,10))#设置5秒的连接超时设置，和10秒的读取超时设置，设置读取超时的目的是防止服务器端出现问题后陷入卡死状态。
            #最坏的情况：服务器没有开启服务（端口未开开）：会直接返回给客户端“由于目标计算机积极拒绝，无法连接。”
            #当服务器端口开启，但是没有资源处理TCP连接建立的时候，会等着5s这里面的5s指的是连接等待时间，是指从客户端发出TCP连接建立请求开始，到服务器与客户端建立TCP连接的时间为止。
            #10s指的是从TCP连接建立开始到服务器返回给客户端文件第一个字节所等待的时间
            # print(r)
            if str(r) == "<Response [404]>":#在此处判断在服务器端是否存在目标文件
                print("文件不存在")
                return#return指的是跳出整个文件，底下的就不找了
            break#break指的是仅仅跳出这个while循环
        except requests.exceptions.RequestException as e:
            print(e)
            i += 1

    basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径
    #print(basedir)
    save_dir = basedir + '\\' + 'download'#对文件的路径进行字符串的添加
    if os.path.exists(save_dir) is False:
        os.makedirs(save_dir)#如果不存在这个路径就创建一个这个路径
    f = open("./"+'download'+'\\'+file_name, "wb")

    try:
        for chunk in r.iter_content(chunk_size=512*1024):#创建一个流写入该文件
            if chunk:
                f.write(chunk)
                print(file_name + "下载成功")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    downloadfile(file_name='download.zip')

