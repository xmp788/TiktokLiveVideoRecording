from PySide6.QtWidgets import QApplication,QMainWindow
from Ui.MainW_Ui import Ui_MainWindow
from comonMain import getConfig
import threading
class MyWindow(QMainWindow,Ui_MainWindow):
  def __init__(self):
    super().__init__()
    self.MaxW=655
    self.MaxH=320
    resize=(self.MaxW,self.MaxH)
    self.setupUi(self,resize)
def entrance():
  threading.Thread(target=getConfig,name='getData').start()
  app=QApplication()
  wd=MyWindow()
  wd.show()
  app.exec()
  # app.exit()
if __name__=='__main__':
  entrance()
  # https://p3-pc-weboff.byteimg.com/tos-cn-i-9r5gewecjs/logo-horizontal.svg