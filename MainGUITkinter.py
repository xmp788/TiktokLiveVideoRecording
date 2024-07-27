from Ui.Tkinter_Ui import *
from comonMain import getConfig
import threading
from tkinter import *

class MyWindow(Ui_MainWindow,CreateTable):
  def __init__(self):
    super().__init__()
    # 设置窗口：宽，高(屏幕百分比)。xy坐标
    self.MaxW,self.MaxH,self.xy=0.4,0.3,'-0-25'
    self._win(self.MaxW,self.MaxH,self.xy)
    # self.resizable(width=False, height=False)
    self.Tabs=self._tabs({'table':'监听列表','setting':'设置'}).children
    self.setting=SetPage(self.Tabs['setting'])#,width=20,height=1)
    threading.Thread(target=getConfig,name='getData',args=(self.setting,)).start()
    self.tabel=CreateTable(self.Tabs['table'])
def entrance():
  wd=MyWindow()
  # wd.attributes('-alpha',1)
  # wd.overrideredirect(True)
  def quit():
    """退出程序保存相关设置数据"""
    wd.setting.saveDate()
    wd.destroy()
  wd.protocol("WM_DELETE_WINDOW",quit)
  wd.mainloop()
if __name__=='__main__':
  entrance()
  # https://p3-pc-weboff.byteimg.com/tos-cn-i-9r5gewecjs/logo-horizontal.svg
