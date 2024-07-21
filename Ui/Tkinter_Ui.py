from tkinter import *
from tkinter.ttk import Notebook
from Ui.processClicke import clicked
from datetime import datetime
import core

class Ui_MainWindow(Tk):
  def __init__(self):
    super().__init__()
    
  def _win(self,win_width,win_height,xy:str):
    self.title('抖音直播监听')
    # 获取屏幕大小 
    scrWidth,scrHeight=self.winfo_screenwidth(),self.winfo_screenheight()
    sizePosition=f'{int(win_width*scrWidth)}x{int(win_height*scrHeight)}{xy}'
    self.geometry(sizePosition)    

  def _tabs(self,kw:dict):
    """创建选择卡"""   
    Tabs=Notebook(self)
    for tab in kw.items():
      frame=Frame(Tabs,name=tab[0],bg='pink')
      Tabs.add(frame,text=tab[1])
    Tabs.pack(fill='both',expand=1)
    return Tabs

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
    # self.updateTab(parent)
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
    rD=LabelFrame(self.fbody,name=f'rD_{i}',border=1,bg=self.bgcolor,fg=self.fgcolor)
    rD.pack(ipadx=self.x,ipady=self.y)
    LabelFrame_.update({f'rD':rD})

    for index in range(len(self.tableHeader)):
      highlightbackground="red"
      highlightcolor="blue"
      if index==1:
        LabelFrame_.update({f'isCheckBox_{i}':BooleanVar()})
        CKB=Checkbutton(rD,name=f'checkbox_{i}_{index}',border=0,bg=self.bgcolor,variable=LabelFrame_[f'isCheckBox_{i}'])
        CKB.place(relwidth=self.Vis[index],relx=self.rex[index])
        LabelFrame_.update({f'checkbox_{i}_{index}':CKB})
      elif index==6:
        btn=Button(rD,name=f'isWatch_{i}_{index}',border=0,bg=self.bgcolor,relief='flat')
        btn.place(relwidth=self.Vis[index],relx=self.rex[index])
        LabelFrame_.update({f'isWatch_{i}_{index}':btn})
      elif index==7:
        LabelFrame_.update({f'Radio_{i}':BooleanVar()})
        rbtn=Radiobutton(rD,name=f'radio_{i}_{index}',border=0,bg=self.bgcolor)
        rbtn.place(relwidth=self.Vis[index],relx=self.rex[index])
        LabelFrame_.update({f'radio_{i}_{index}':rbtn})
      else:
        entry=Entry(rD,name=f'lb_{i}_{index}',bd=0,fg=self.fgcolor,bg=self.bgcolor,justify='center')
        entry.place(relwidth=self.Vis[index],relx=self.rex[index],relheight=1)     
        LabelFrame_.update({f'lb_{i}_{index}':entry})
    self.tabBody.update({f'LabelFrame_{i}':LabelFrame_})
    
  def refreshData(self,tabBody:dict,Obj,length):
    """刷新表数据"""
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
            tabBody[f'LabelFrame_{i}'][f'Radio_{i}'].set(value=Obj[someOne]['recoding'])
            if Obj[someOne]['Living']:
              tabBody[f'LabelFrame_{i}'][f'radio_{i}_{j}'].configure(state='normal')
            else:
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
