import core,time,subprocess,threading
from datetime import datetime
from loguru import logger
from pathlib import Path
thisFileP=Path(__file__).parent.parent
def commonSeting():  
  # 定义时间水印
  timeWatermark=":".join(["drawtext=text='%{localtime}'",
        f"fontfile={thisFileP}/ffmpeg/FreeSerif.ttf",
        "fontsize=35",
        "fontcolor=red",
        "x=main_w-text_w-25",
        "y=25"])
  return timeWatermark

def RecordingFunc(datas,msg):# 备注，昵称，直播流
  """录制函数""" 
  # 文件标题
  def titleFilter(liveFileName: str):
    """转为Windows合法文件名"""
    # 非法字符
    lst = ['\r', '\n', '\\', '/', ':', '*', '?', '"', '<', '>', '|']
    # 非法字符处理方式1
    # for key in lst:
    #     liveFileName = liveFileName.replace(key, '&')
    # 非法字符处理方式2
    table = str.maketrans(dict.fromkeys(''.join(lst),'&'))
    liveFileName = liveFileName.translate(table)
    # 文件名+路径长度最大255，汉字*2，取60
    if len(liveFileName) > 60:
        liveFileName = liveFileName[:60]
    return liveFileName.strip()
  def Rec_ing(urls,fileFullname,vf):
    """录制命令"""    
    cmd = [str(f'{thisFileP}/ffmpeg/ffmpeg.exe'),"-re","-y",
            "-v","verbose", 
            "-timeout","2000",
            "-loglevel","error",
            "-hide_banner",
            "-user_agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "-analyzeduration","2147483647",
            "-probesize","2147483647",
            "-i",urls,
            "-vf",vf,
            '-bufsize','5000k',
            "-map","0",
            "-sn","-dn",
            '-max_muxing_queue_size','64',
            str(fileFullname)]
    print(f'{msg}开始录制视频……')
    logger.info(f'{msg}开始录制视频……')
    subprocess.Popen(cmd).wait()# 录制
    obj[datas[0]]['rec_etime'],obj[datas[0]]['recoding']=datetime.now(),False
    logger.info(f"{msg}直播结束!停止录制！！！{msg}已成功录制:{obj[datas[0]]['rec_etime']-obj[datas[0]]['rec_stime']}")
  
  fileN=f'{time.strftime("%Y-%m-%d_%H-%M-%S")}.mp4'
  # fileDirName=titleFilter(datas[0].split('.')[1])#保存文件名       
  fileDirName=titleFilter(datas[1])#保存文件名
  makedir = core.Public_v['RecordDir']/fileDirName#dir 前面读取配置文件获得
  makedir.mkdir(parents=True,exist_ok=True) # 创建文件夹
  path = makedir/fileN # 文件保存路径
  try:
    # 记录录制时间,标记正在录制状态
    obj[datas[0]]['recoding'],obj[datas[0]]['rec_stime']=True,datetime.now()
    Rec_ing(datas[2],path,commonSeting())# 创建录制视频线程
    
  except Exception as e:
    sr='='
    msg=f'{datas[1]}{sr*20}>>录制异常:'
    print(f'{msg}{e}') 
    logger.error(f'{msg}{e}') 

def  watching(datas):
  from screeninfo import get_monitors
  wid,hei=get_monitors()[0].width,get_monitors()[0].height  # 获取屏幕尺寸
  x=0
  ffplayCMD=[f'{thisFileP}/ffmpeg/ffplay.exe',
              '-volume',str(2),# 设置直播初始音量
              '-x',f'{x}',# 设置直播画面大小
              '-left',f'{wid-x}',# 位置
              '-vf',commonSeting(),# 过滤器(水印)
              '-autoexit',# 播放结束后自动退出
              '-window_title',datas[1],# 设置标题
              # '-vn',# 无视频
              # '-nodisp',# 无输出画面
              # '-hide_banner',
              '-noborder',# 设置为无边框
              '-i',datas[2]]# 输入源
  obj[datas[0]]['watching']=False
  # 创建子进程,使用ffpaly播放开播提醒音
  # subprocess.Popen(f'{thisFileP}/ffmpeg/ffplay.exe -nodisp -volume 100 -autoexit -i {thisFileP}/sound/notify_message.mp3')
  subprocess.Popen(ffplayCMD).wait()
  obj[datas[0]]['isWatch']=False
def LiveProcess(datas):
  global obj
  obj=core.Public_v['Obj']
  msg=f'{datas[1]} {core.Public_v["Splicer"]}'
  if obj[datas[0]]['isRecord']:# 录制
    threading.Thread(target=RecordingFunc,args=(datas,msg)).start() if not obj[datas[0]]['recoding'] else print(f"{msg}已录制:{datetime.now()-obj[datas[0]]['rec_stime']}")    
  if obj[datas[0]]['isWatch']:# 观看    
    threading.Thread(target=watching,args=(datas,)).start() if obj[datas[0]]['watching'] else print('正在观看')
