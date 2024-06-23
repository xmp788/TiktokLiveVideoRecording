import core,startWay,time,configparser,gevent
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
@runtime
def getConfig():  
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
      logger.debug(f"配置文件路径为：{saveDir}")
      return Path(saveDir)
  RecordDir = Path(readConfigurationFile())
  Obj=dict()
  core.Public_v=dict(
    Splicer=Splicer,
    RecordDir=RecordDir,
    Obj=Obj
  )

  del Splicer,RecordDir
  # 数据初始化
  someb=dict.fromkeys(['Listening','num','notes','nickname','authorURL','Living','isWatch','isRecord','reCorTime','url','watching','recoding','msg'],False)
  # 定义程序执行方式
  sign=['joinAll','gJoin','gLet','apply','async']
  LS=[]
  while True:
    with open(f'{thisPath}/MonitoringAddress.json','r',encoding='utf-8') as f:
      List=f.readlines()
    # 字典推导式  过滤掉需要监听的列表
    somebody={f"{No}.{item.strip().split(':',1)[0]}": item.strip().split(':',1)[1] for No,item in enumerate(List,start=1) if '//'not in item.strip().split(':',1)[0]}
    del List,f
    for key,value in somebody.items():
      Obj.setdefault(key,someb.copy())
      Obj[key].update(
                      num=key.split('.',1)[0],
                      notes=key.split('.',1)[1],
                      url=value
                      )
      startWay.way(key,value,sign[0]) # sign=['joinAll','gJoin','gLet','apply','async']
      # LS.append(gevent.spawn(MonitoringLive,key,value))
    # gevent.joinall(LS)
if __name__ == "__main__":
  getConfig()