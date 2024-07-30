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

def RecordingFunc(somebody,nickname,flv_rtmp,msg):# 备注，昵称，直播流
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
  def Rec_ing(urls,fileFullname,vf,msg):
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
    # print(f'{msg}开始录制视频……')
    try:
      subprocess.Popen(f'{thisFileP}/ffmpeg/ffplay.exe -nodisp -volume 6 -autoexit -i {thisFileP}/sound/notify_message.mp3')
      # 标记正在录制状态,记录录制时间
      obj[somebody]['recoding'],obj[somebody]['rec_stime']=True,datetime.now()
      sub=subprocess.Popen(cmd)
      obj[somebody]['recPID']=sub.pid
      logger.info(f"\n{msg}开始录制视频……")
      sub.wait()# 录制
      logger.info(f"\n{msg}直播结束!停止录制！！！已成功录制:{datetime.now()-obj[somebody]['rec_stime']}")
    except Exception as e:
      sr='='
      msg=f'{nickname}{sr*20}>>录制异常:'
      print(f'{msg}{e}') 
      logger.error(f'{msg}{e}')
    finally:
      obj[somebody]['recoding'],obj[somebody]['rec_stime']=False,''  
  fileN=f'{time.strftime("%Y-%m-%d_%H-%M-%S")}.mp4'
  # fileDirName=titleFilter(sb.split('.')[1])#保存文件名       
  fileDirName=titleFilter(nickname)#保存文件名
  makedir = core.Public_v['RecordDir']/fileDirName#dir 前面读取配置文件获得
  makedir.mkdir(parents=True,exist_ok=True) # 创建文件夹
  path = makedir/fileN # 文件保存路径
  # 创建录制视频线程
  threading.Thread(target=Rec_ing,args=(flv_rtmp,path,commonSeting(),msg)).start()

def  watching(somebody,nickname,flv_rtmp):
  scrWidth,scrHeight=core.Public_v['scrWidth'],core.Public_v['scrHeight']  # 取出屏幕尺寸
  x=36
  ffplayCMD=[f'{thisFileP}/ffmpeg/ffplay.exe',
              '-volume',str(2),# 设置直播初始音量
              '-x',f'{x}',# 设置直播画面大小
              '-left',f'{scrWidth-x}',# 位置
              '-vf',commonSeting(),# 过滤器(水印)
              '-autoexit',# 播放结束后自动退出
              '-window_title',nickname,# 设置标题
              # '-vn',# 无视频
              # '-nodisp',# 无输出画面
              # '-hide_banner',
              '-noborder',# 设置为无边框
              '-i',flv_rtmp]# 输入源
  # obj[sb]['watching']=False
  # 创建子进程,使用ffpaly播放开播提醒音
  # subprocess.Popen(f'{thisFileP}/ffmpeg/ffplay.exe -nodisp -volume 100 -autoexit -i {thisFileP}/sound/notify_message.mp3')
  sub=subprocess.Popen(ffplayCMD)
  obj[somebody]['watPID']=sub.pid
  sub.wait()
  obj[somebody]['isWatch']=False
def LiveProcess(*datas):
  global obj
  obj=core.Public_v['Obj']
  sb,flag=datas
  nickname,flv_rtmp=obj[sb]["nickname"],obj[sb]['flv_rtmp']
  msg=f'{nickname} {core.Public_v["Splicer"]}'
  if obj[sb]['isRecord'] and flag==-1:# 录制
    if obj[sb]['recoding']:
      print(f"{msg}已录制:{datetime.now()-obj[sb]['rec_stime']}")
    else:
      RecordingFunc(sb,nickname,flv_rtmp,msg)
  if obj[sb]['isWatch'] and flag==1:# 观看    
    threading.Thread(target=watching,args=(sb,nickname,flv_rtmp)).start() if obj[sb]['watching'] else print('正在观看')
