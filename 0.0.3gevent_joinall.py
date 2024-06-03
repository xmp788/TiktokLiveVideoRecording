# from gevent import monkey
# monkey.patch_all()
import gevent,core,time,configparser
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

  core.mode=mode
  core.Splicer=Splicer
  core.fileName=fileName
  core.thisPath=thisPath
  core.RecordDir=RecordDir
  core.Obj=Obj   

  # core.public_V=dict(
  #   mode=mode,
  #   Splicer=Splicer,
  #   fileName=fileName,
  #   thisPath=thisPath,
  #   RecordDir=RecordDir,
  #   Obj=Obj
  # )

  someb=dict.fromkeys(['num','isRecord','notes','nickname','authorURL','url','recoding'],'')
  while True:
    with open(f'{thisPath}/MonitoringAddress.json','r',encoding='utf-8') as f:
      List=f.readlines()
    # 字典推导式  过滤掉需要监听的列表
    somebody={f"{No}.{item.strip().split(':',1)[0]}": item.strip().split(':',1)[1] for No,item in enumerate(List,start=1) if '//'not in item.strip().split(':',1)[0]}
    del Splicer,RecordDir,List,f
    for key,value in somebody.items():
      Obj.setdefault(key,someb.copy())
      Obj[key].update(num=key.split('.',1)[0],
                      notes=key.split('.',1)[1],
                      url=value)
 
      # 创建协程,并传递参数
      gevent.joinall([gevent.spawn(MonitoringLive,key,value)])
      # MonitoringLive(key,value)
      if not mode['ScanList']:
         break
    if not mode['MonirtingLive']:# 是否监视所有列表直播状态
      break
    # else:
    #   time.sleep(10)

if __name__ == "__main__":
  # 程序执行方式
  mode={
    'ScanList':1, # 是否监视所有地址，1：开启，0：关闭（调试程序用）
    'MonirtingLive':0, # 是否循环监视所有地址
    'RecordVideo':1 # 是否开启录制模式，1：开启，0：关闭，即只监视状态不录制视频
  }
  core.rec_somebody_lis=['依依','一颗心','我乐意','小和','喜喜'] # 需要录制视频的主播，不需要录制无需添加（地址文件对应的备注）
  getConfig()
