from core.liveDataProcessing import LiveProcess
from tkinter import *
from pathlib import Path
import core,os
def clicked(event:Event,args):
    ent=event.widget
    frameList=ent.master._w.replace('!','').split('.')
    frame=ent.master.children
    # 判断点击来自哪个页面
    if frameList[2]=='setting':
      enpath=Path(frame['!entry'].get())
      try:
        enpath.mkdir(parents=True,exist_ok=True)
        os.startfile(enpath)
      except Exception as e:
        print(e)
    elif frameList[2]=="table":
      if len(args):
        thead=args['tableHead']
        tbody=args['tabBody']
      cname=ent._name.split('_')
      note=frame[f'lb_{cname[1]}_2'].get()# 备注
      # dot=frame[f'lb_{cname[1]}_1'].get()# 序号
      somebody=core.Public_v['Obj'][note]
      match cname[0]:
        case 'checkbox': # 监听自动录制
          isCek=tbody[f'LabelFrame_{cname[1]}'][f'isCheckBox_{cname[1]}'].get()
          tbody[f'LabelFrame_{cname[1]}'][f'isCheckBox_{cname[1]}'].set(not isCek) # 设置选择框
          # tbody[f'LabelFrame_{cname[1]}'][f'Radio_{cname[1]}'].set(not isCek) # 设置录制按扭
          somebody['isRecord']=not isCek
          somebody['recoding']=isCek
          return
        case 'isWatch': # 观看直播
          if somebody['Living']:
            somebody['watching']=not somebody['watching'] # 当前状态取反
            if somebody['watching']:
              somebody['isWatch']=True
              LiveProcess(note,1)
            else:
              PID=somebody['watPID']
              stopRecoding(PID,9)
          return
        case 'radio': # 手动录制
          if somebody['Living']:
            isCek=tbody[f'LabelFrame_{cname[1]}'][f'Radio_{cname[1]}'].get()
            tbody[f'LabelFrame_{cname[1]}'][f'Radio_{cname[1]}'].set(not isCek)# 设置录制按扭
            somebody['isRecord']=not isCek #False
            somebody['recoding']= isCek # True
            if isCek:
              try:
                PID=somebody['recPID']
                stopRecoding(PID)
              except KeyError as er:
                print(er,'未录制')
              except Exception as er:
                print(er)          
            else:
              LiveProcess(note,-1)            
          return
      
def stopRecoding(PID,MODE=0):
  """
  结束进程
  PID:要结束进程的PID
  MODE:结束方式,0正常结束,9强制结束
  """
  os.kill(PID,MODE)
  