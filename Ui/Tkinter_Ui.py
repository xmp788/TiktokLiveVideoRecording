from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import Notebook
from Ui.processClicke import clicked
from datetime import datetime
from pathlib import Path
from loguru import logger
import core,pickle,configparser

class Ui_MainWindow(Tk):
  def __init__(self):
    super().__init__()
    
  def _win(self,win_width,win_height,xy:str):
    self.title('抖音直播监听')
    # 获取屏幕大小 
    scrWidth,scrHeight=self.winfo_screenwidth(),self.winfo_screenheight()
    # sizePosition=f'{int(win_width*scrWidth)}x{int(win_height*scrHeight)}{xy}'
    sizePosition=f'{int(520)}x{int(260)}{xy}'
    self.geometry(sizePosition)    

  def _tabs(self,kw:dict):
    """创建选择卡"""   
    Tabs=Notebook(self)
    for tab in kw.items():
      frame=Frame(Tabs,name=tab[0],bg='pink')
      Tabs.add(frame,text=tab[1])
    Tabs.pack(fill='both',expand=1)
    Tabs.select(0)# 设置默认选择
    return Tabs

class SetPage():
 
  def __init__(self,parent:Frame,**kw) -> None:
    self.parentPath=Path(__file__).parent.parent # 获取项目根目录
    labfr=LabelFrame(parent,text='视频保存位置（鼠标左键双击输入框可更改） 点击"打开文件夹"可打开视频保存文件夹,若不存在将自动创建并打开')
    # Label(labfr,text='视频保存位置：').pack(side='left')
    pth=self.readConfigurationFile()
    self.pth=pth if pth else fr'{self.parentPath}\Video'
    self.vp=Entry(labfr,width=35,text=StringVar(value=self.pth))
    self.vp.pack(side='left',fill='both')
    Button(labfr,text='打开文件夹',command=self.ck).pack(side='left')
    labfr.pack(fill='x')

    labfr=LabelFrame(parent,text='主播直播间列表（备注+直播间地址，// 表示不需要监听的主播）')
    labfr.pack(side='right')
    self.notep=Text(labfr,kw,font=300,bd=0)
    self.notep.pack(anchor='nw',expand=1,fill='both')
    self.addRecod()
    # 鼠标左键双击更改视频保存路径
    self.vp.bind('<Double-Button-1>',self.ck)

  def readConfigurationFile(self):
      """读取配置文件"""
      config = configparser.ConfigParser()
      try:
        config.read(f'{self.parentPath}/config.ini',encoding='utf8')
        saveDir = config.get('DouYin','downloadPath')
      except Exception as e:
        return None
      return Path(saveDir)
  
  def ck(self,event):
    path= askdirectory(title='视频保存路径',initialdir=self.vp.get())
    path =path if path else self.vp.get()
    self.vp.configure(text=StringVar(value=path))

  def addRecod(self):
    """读取已保存文件"""
    try:
      with open(f'{self.parentPath}/MonitoringAddress.pkl','rb') as f:
        data=pickle.load(f)
    except FileNotFoundError:
      try:
        with open(f'{self.parentPath}/MonitoringAddress.json','r',encoding='utf-8') as f:
          data=f.readlines()
      except FileNotFoundError:
        return
    self.notep.insert(INSERT,''.join(data))

  def getData(self) -> list:
    """获取文本框中数据"""
    return self.notep.get(1.0,END).strip()

  def saveDate(self):
    """保存文件(二进制)"""
    # data=self.notep.get(1.0,END).strip()
    with open(f'{self.parentPath}/MonitoringAddress.pkl','wb') as f:
      pickle.dump(self.notep.get(1.0,END).strip(),f)
    recodpath=f'downloadPath={self.vp.get()}'
    string=f'[DouYin]\n{recodpath}'
    with open(f'{self.parentPath}/config.ini','w',encoding='utf-8') as f:
      f.write(string)

class CreateTable():
  """创建表格"""
  def __init__(self,parent:Frame):
    self.x,self.y=260,13
    self.fgcolor,self.bgcolor='#D15','#FFC' # 颜色 
    pad=5
    frame=Frame(parent,padx=pad,pady=pad,background=self.bgcolor)
    self.scro=Scrollbar(frame,width=0)
    ftable=Frame(frame)    

    ftHead=Frame(ftable)
    self.ftBody=Canvas(ftable,width=2*self.x,highlightthickness=0)

    self.fbody=Frame(self.ftBody)# 表体框架

    self.scro.pack(side='right',fill='y')
    frame.pack(anchor='nw')
    ftable.pack(side='left')
    ftHead.pack(),self.ftBody.pack()

    self.ftBody.create_window((0,0),window=self.fbody,anchor='nw')
    self.fbody.update()
    self.scro.config(command=self.ftBody.yview)


    self.txt=['No','监听','备注','昵称','主页','状态','点击观看','录视频','已录制'] # 定义表头
    self.select=dict()
    self.tableHeader=dict.fromkeys(self.txt,'')    
    self.Vis=[0.03,0.09,0.1,0.26,0.08,0.1,0.12,0.06,0.16]# 宽度
    self.rex=[round(sum(self.Vis[:i]),2) for i in range(len(self.Vis))]# 相对x坐标位置
    self.tabBody=dict()

    def on_mousewheel(event):
      """鼠标滚动"""
      self.ftBody.yview_scroll(-1*(int(event.delta/120)), "units")
    # 控件绑定点击事件
    parent.bind_class('Checkbutton','<Button-1>',lambda e:clicked(e,self.select))
    parent.bind_class('Button','<Button-1>',lambda e:clicked(e,self.select))
    parent.bind_class('Radiobutton','<Button-1>',lambda e:clicked(e,self.select))
    self.ftBody.bind_all("<MouseWheel>", on_mousewheel)    

    self.setTabHeader(ftHead)
    core.Public_v.update({'scrWidth':parent.winfo_screenwidth(),'scrHeight':parent.winfo_screenheight()})
    parent.after(1000,lambda:self.updateTab(parent))

# ---------------------------------------------------------------------------------------------------------------------
  def setTabHeader(self,parent:Frame):
    """设置表头"""
    tableHead=dict()
    tHead=LabelFrame(parent,name='tableHead',borderwidth=1,bg=self.bgcolor,fg=self.fgcolor)
    tHead.pack(ipadx=self.x,ipady=self.y+2)
    for index,item in enumerate(self.txt):
      # if index==1:# 监听全选框        
      #   tableHead.update({'isCheckBox_all':BooleanVar()})
      #   Checkbutton(tHead,text=item,border=3,bg=self.bgcolor,variable=tableHead['isCheckBox_all']).place(relwidth=self.Vis[index],relx=self.rex[index])
      #   continue
      Label(tHead,text=item,border=5,bg=self.bgcolor).place(relwidth=self.Vis[index],relx=self.rex[index])
    return self.select.update({'tableHead':tableHead})
  
  def updateTab(self,parent):
    """更新表行数"""
    Obj=core.Public_v['Obj']
    if not len(Obj):return
    comp=abs(len(self.tabBody)-len(Obj)) # 取绝对值，判断是否需要增删控件。0不需要，否则需要
    for _ in range(comp):
      if len(self.tabBody)>len(Obj):# 减少          
        lastKey=list(self.tabBody.keys())[-1]
        bodyLast=self.tabBody.pop(lastKey)
        self.deleteRow(bodyLast['rD'])
      elif len(self.tabBody)<len(Obj):# 增加          
        i=len(self.tabBody)
        self.addRow(i)
        self.select.update({'tabBody':self.tabBody})
      
    self.refreshData(self.select['tabBody'],Obj,len(self.txt))
    self.ftBody.configure(yscrollcommand=self.scro.set,scrollregion=self.ftBody.bbox('all'))

    parent.after(1000,lambda:self.updateTab(parent))

  def deleteRow(self,name:Widget):
    """删除一行控件"""
    name.destroy()    

  def addRow(self,i:int):
    """添加一行控件[框架]"""
    LabelFrame_=dict()
    rD=LabelFrame(self.fbody,name=f'rD_{i}',bd=1,bg=self.bgcolor,fg=self.fgcolor)
    rD.pack(ipadx=self.x,ipady=self.y)
    LabelFrame_.update({f'rD':rD})

    conf={
      'bd':0,
      'highlightbackground':'green',
      'highlightcolor':'blue',
      'fg':self.fgcolor,
      'bg':self.bgcolor
    }
    for index in range(len(self.tableHeader)):
      pl={
        'relwidth':self.Vis[index],
        'relx':self.rex[index],
        'relheight':1
      }
      if index==1:# 监听
        LabelFrame_.update({f'isCheckBox_{i}':BooleanVar()})
        ckb=Checkbutton(rD,name=f'checkbox_{i}_{index}',variable=LabelFrame_[f'isCheckBox_{i}'],**conf)
        ckb.place(**pl)
        LabelFrame_.update({f'checkbox_{i}_{index}':ckb})
      elif index==6:# 观看
        btn=Button(rD,name=f'isWatch_{i}_{index}',relief='flat',**conf)
        btn.place(**pl)
        LabelFrame_.update({f'isWatch_{i}_{index}':btn})
      elif index==7:# 录制
        LabelFrame_.update({f'Radio_{i}':BooleanVar()})
        rbtn=Radiobutton(rD,name=f'radio_{i}_{index}',**conf)
        rbtn.place(**pl)
        LabelFrame_.update({f'radio_{i}_{index}':rbtn})
      else:
        entry=Entry(rD,name=f'lb_{i}_{index}',justify='center',**conf)
        entry.place(**pl)     
        LabelFrame_.update({f'lb_{i}_{index}':entry})
    self.tabBody.update({f'LabelFrame_{i}':LabelFrame_})
    
  def refreshData(self,tabBody:dict,Obj,length):
    """刷新表数据"""
    try:
      for i,someOne in enumerate(Obj):
        for j,(k,v) in enumerate(Obj[someOne].items()):
          if j==length:break
          if j==0:
            v=i+1
          v1=StringVar(value=v)
          match k:
            case 'Listening':
              # tabBody[f'LabelFrame_{i}'][f'isCheckBox_{i}'].set(Obj[someOne]['isRecord'])
              continue      
            case 'nickname':
              # 如正在观看,更改昵称显示为当前房间人数状态
              if Obj[someOne]['isWatch']:
                v1=StringVar(value=f"{Obj[someOne]['userCount']}/{Obj[someOne]['total_userCount']}人")
            case 'authorURL':# 主页
              v1.set('查看')
            case 'Living':# 状态
              v1.set(Obj[someOne]['msg'])
            case 'isWatch':# 直播 watching
              if Obj[someOne]['Living']:
                if Obj[someOne]['isWatch']:
                  tabBody[f'LabelFrame_{i}'][f'isWatch_{i}_{j}'].configure(text='退出直播',fg='blue',state='normal')
                else:
                  v=f"{Obj[someOne]['userCount']}/{Obj[someOne]['total_userCount']}人"
                  tabBody[f'LabelFrame_{i}'][f'isWatch_{i}_{j}'].configure(text=v,fg='blue',state='normal')
              else:
                tabBody[f'LabelFrame_{i}'][f'isWatch_{i}_{j}'].configure(text='',state='disabled')          
              continue      
            case 'isRecord':# 录制视频 recoding
              if Obj[someOne]['Living']:
                tabBody[f'LabelFrame_{i}'][f'Radio_{i}'].set(value=Obj[someOne]['recoding'])
                tabBody[f'LabelFrame_{i}'][f'radio_{i}_{j}'].configure(state='normal')
              else:
                tabBody[f'LabelFrame_{i}'][f'Radio_{i}'].set(value=Obj[someOne]['isRecord'])
                tabBody[f'LabelFrame_{i}'][f'radio_{i}_{j}'].configure(state='disabled')
              tabBody[f'LabelFrame_{i}'][f'radio_{i}_{j}'].configure(variable=tabBody[f'LabelFrame_{i}'][f'Radio_{i}'],value=True)
              continue
            case 'reCorTime':
              if Obj[someOne]['Living']:
                # if Obj[someOne]['isRecord']:
                if Obj[someOne]['recoding']:
                  try:
                    ts=str(datetime.now()-Obj[someOne]['rec_stime']).split('.')[0]
                    v1=StringVar(value=(ts))
                  except KeyError as error:
                    if error.self.Vis =='rec_stime':
                      v1=StringVar(value='自动录制尚未开始')
                    else:
                      v1=StringVar(error)
                else:
                  v1=StringVar(value='已开播,未录制视频')
              else:
                v1=StringVar(value='')
          tabBody[f'LabelFrame_{i}'][f'lb_{i}_{j}'].configure(text=v1)
    except RuntimeError:
      print("RuntimeError:",RuntimeError)
    finally:
      return