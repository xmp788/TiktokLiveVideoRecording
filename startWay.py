# from gevent import monkey
# monkey.patch_all()
from core.getRoom import MonitoringLive
def way(somebody,url,sign='joinAll'):
  match sign:
    case 'joinAll':
      import gevent
      # 创建协程,并传递参数
      gevent.joinall([gevent.spawn(MonitoringLive,somebody,url)])

    case 'gJoin':
      import gevent
      # 创建协程,并传递参数      
      g=gevent.spawn(MonitoringLive,somebody,url)
      g.join()

    case 'gLet':
      import greenlet
      # 创建协程
      g=greenlet(MonitoringLive)
      # 开始执行协程,并传递参数
      g.switch(somebody,url)

    case 'apply':
      # 同步
      from multiprocessing import Pool
      p1=Pool(3)
      p1.apply(MonitoringLive,args=(somebody,url))

    case 'async':
      # 异步
      from multiprocessing import Pool
      p2=Pool(processes=3)
      p2.apply_async(MonitoringLive,args=(somebody,url)).get()

      p2.close()
      p2.join()