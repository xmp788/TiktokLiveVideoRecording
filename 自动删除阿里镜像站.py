import os
import shutil
lis=['[global]\n','timeout = 10000\n','index-url = http://mirrors.aliyun.com/pypi/simple/\n','trusted-host = mirrors.aliyun.com']
usrname=os.getlogin()   #获取当前用户名
# print(usrname)
Path=fr'C:\Users\{usrname}\AppData\Roaming\pip'
if not os.path.exists(Path):
    os.makedirs(Path)
    with open(Path+'\pip.ini','w') as wr:
        wr.writelines(lis)
    print('镜像站增加成功!')
else:
    shutil.rmtree(Path)
    print('镜像站删除成功!')