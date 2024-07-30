import core,startWay,time,configparser,gevent
from queue import Queue
Q=Queue(10)
from threading import Thread
from core.getRoom import MonitoringLive
from loguru import logger
from pathlib import Path

def runtime(fun):
  def callFun():
    startTime=time.time()
    fun()
    endTime=time.time()
    print(f'程序运行结束,耗费时长:{(endTime-startTime):.9f}秒')
  return callFun
# @runtime
def getConfig(data):  
  fileName=lambda name:thisPath/name 
  thisPath=Path(__file__).parent#当前文件所在位置
  Splicer=f'{"":{"一"}{">"}{10}}' # 对象拼接符
  logger.remove(handler_id=None) # 取消控制台打印
  logger.add(fileName('douyin_log.log'))
  
  def readConfigurationFile():
      """读取配置文件"""
      config = configparser.ConfigParser()
      config.read(fileName('config.ini'),encoding='utf8')
      saveDir = config.get('DouYin','downloadPath')
      return Path(saveDir)
  try:
    RecordDir=data.pth
  except Exception:
    RecordDir = Path(readConfigurationFile())  
  logger.debug(f"配置文件路径为：{RecordDir}")
  Obj=dict()# 创建数据数据模型
  core.Public_v=dict(
    Splicer=Splicer,
    RecordDir=RecordDir,
    Obj=Obj
  )

  del Splicer,RecordDir
  # 数据初始化
  someb=dict.fromkeys(['num','Listening','notes','nickname','authorURL','Living','isWatch','isRecord','reCorTime','url','watching','recoding','msg'],False)
  # 定义程序执行方式
  sign=['joinAll','gJoin','gLet','apply','async']
  # flag=True
  Thread(target=startWay.way2,args=(Q,)).start()
  # LS=[]
  urlist=set()
  while True:
    # if not List:
    #   with open(f'{thisPath}/MonitoringAddress.json','r',encoding='utf-8') as f:
    #     List=f.readlines()
    sr=data.getData()
    if len(sr)==0:continue
    List=sr.strip().split('\n')
    List=[_ for _ in List if not _.startswith('//')] # 剔除不需要的监听
    # 字典推导式  过滤掉需要监听的列表
    # somebody={f"{No}.{item.strip().split(':',1)[0]}": item.strip().split(':',1)[1] for No,item in enumerate(List,start=1) if '//'not in item.strip().split(':',1)[0]}
    somebody={f"{item.strip().split(':',1)[0]}": item.strip().split(':',1)[1] for item in List if '//'not in item.strip().split(':',1)[0]}
    del List
    newSet=set(somebody.keys())
    if len(urlist) and urlist!=newSet:
      """利用集合找出变动过的数据"""
      subtract=urlist.difference(newSet)# 减少的(删除的)
      # increase=urlist.symmetric_difference(newSet)# 新增的
      for i in subtract:
        Obj.pop(i) # 从模型中删除减少的数据。新增的不用处理，后面会自动添加
    
    urlist=newSet
    for key,value in somebody.items():
      Obj.setdefault(key,someb.copy())
      Obj[key].update(
                      # num=key.split('.',1)[0],
                      # notes=key.split('.',1)[1],
                      notes=key,
                      url=value
                      )
      Q.put([key,value],block=True)
      
      # startWay.way(key,value,sign[0]) # sign=['joinAll','gJoin','gLet','apply','async']
      # LS.append(gevent.spawn(MonitoringLive,key,value))
    # gevent.joinall(Q.get(block=True)) 
    # gevent.joinall(LS) 
    
# if __name__ == "__main__":
#   getConfig()