from Ui.Tkinter_Ui import Ui_MainWindow,CreateTable
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
    self.tabel=CreateTable(self.Tabs['table'])
def entrance():
  threading.Thread(target=getConfig,name='getData').start()
  wd=MyWindow()
  wd.mainloop()
if __name__=='__main__':
  entrance()
  # https://p3-pc-weboff.byteimg.com/tos-cn-i-9r5gewecjs/logo-horizontal.svg
