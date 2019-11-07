#下面的上传文件函数，需要输入文件名
from urllib3 import encode_multipart_formdata
import os
import requests
def uploadfile(file_name):
    basedir = os.path.abspath(os.path.dirname(__file__))#获取当前文件的绝对路径
    #print(basedir)#D:\tensorboard-shishi\test 输出文件的绝对路径，测试用
    upload_url = 'http://localhost:8080/upload/'#需要上传的url值，在这里upload后面必须有/,如果没有会报错，就是发不出去包，其body显示为空none
    #header={"Content-Type":"multipart/form-data"}#http的header用默认配置就好
    save_dir = basedir+'\\'+'upload'
    if os.path.exists(save_dir) is False:#这里是判断这个路径是否存在，如果不存在就传建这个路径
        os.makedirs(save_dir)
    file_path = save_dir+'\\'+file_name#需要加上\\用来隔开filename和basedir
    #print(filte_path)输出文件路径，测试用
    files = {'askfile':open(file_path,'rb')}#此处是重点！我们操作文件上传的时候，把目标文件以open打开，然后存储到变量file里面存到一个字典里面

    i = 0
    while i < 3:
        try:
            upload_res=requests.post(upload_url,files=files,timeout = (5, 10))##此处是重点！我们操作文件上传的时候，接口请求参数直接存到upload_data变量里面，在请求的时候，直接作为数据传递过去
            print(upload_res)
            print(file_name+"上传成功")
            break
        except requests.exceptions.RequestException as e:
            print(e)#输出错误
            i += 1

if __name__ == '__main__':
    uploadfile(file_name='re.png')