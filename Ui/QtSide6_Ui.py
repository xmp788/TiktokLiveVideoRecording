import core,threading
from PySide6.QtCore import Qt,QTimer
from PySide6.QtWidgets import QMainWindow,QTabWidget,QWidget,QTableWidget,QTableWidgetItem,QCheckBox,QLabel,QPushButton,QRadioButton
from core.liveDataProcessing import LiveProcess
def watchParamPrepare(sb):
  obj=core.Public_v['Obj']
  LiveProcess(sb,obj[sb]['nickname'],obj[sb]['flv_rtmp'])
class Ui_MainWindow(object):
  def setupUi(self,MainWindow:QMainWindow,size) -> None:
    if not MainWindow.objectName():
      MainWindow.setObjectName("MainWindow")
    MainWindow.resize(size[0],size[1])
    MainWindow.setWindowTitle("TiktokLiveVideoRecording")
    
    self.tabWidget=QTabWidget(parent=MainWindow)
    self.tabWidget.setObjectName('tabWidget')
    self.tabWidget.setGeometry(0,0,size[0],size[1])
    self.tabWidget.setLayoutDirection(Qt.LeftToRight)

    tabWid={'home':'监听列表','setting':'设置'}
    for index,(key,value) in enumerate(tabWid.items()):
      setattr(self,key,QWidget(self.tabWidget))
      eval(f"self.{key}.setObjectName('{key}')")      
      eval(f"self.tabWidget.addTab(self.{key},'')")
      self.tabWidget.setTabText(index,value)
    self.tabWidget.setCurrentIndex(0)

  # 创建表
    self.tableWidget=QTableWidget(parent=self.home)
    self.tableWidget.setObjectName('dataItems')
    self.tableWidget.setGeometry(-1,-1,size[0],size[1])
    self.tableWidget.setColumnCount(9)# 表列数
    # self.tableWidget.setShowGrid(False)# 是否显示表格线
    # 创建表头
    self.tableHeader=['监听','序号','备注','昵称','主播主页','主播状态','直播','录制视频','已录制']
    self.tableWidget.setHorizontalHeaderLabels(self.tableHeader)
    # 2s刷新一次数据
    self.timer=QTimer(self)
    self.timer.timeout.connect(self.__addData)
    self.timer.start(2000)

# ------------------------------------------------------------------------------
  def __addData(self):
    self.tableWidget.setRowCount(len(core.Public_v['Obj'])+1)# 表行数
    try:
      for i,someOne in enumerate(core.Public_v['Obj']):
        setattr(self,f'checkbox_{i}',QCheckBox())
        eval(f"self.checkbox_{i}.setObjectName('checkbox_{i}')")
        eval(f"self.checkbox_{i}.setLayoutDirection(Qt.RightToLeft)")
        eval(f"self.checkbox_{i}.clicked.connect(self.Clicked)")
        isR=core.Public_v['Obj'][someOne]['isRecord']
        eval(f"self.checkbox_{i}.setChecked({isR})")
        eval(f"self.tableWidget.setCellWidget({i},0,self.checkbox_{i})")

        bl=core.Public_v['Obj'][someOne]['Living']
        for j,(key,val) in enumerate(core.Public_v['Obj'][someOne].items()):
          if j==len(self.tableHeader):break
          match key:
            case 'authorURL':
              val=f'<a {val}>查看</a>'
              setattr(self,f'authorURL_{i}',QLabel())
              eval(f"self.authorURL_{i}.setObjectName('author_{i}')")
              eval(f"self.authorURL_{i}.setText('{val}')")
              eval(f"self.authorURL_{i}.setAlignment(Qt.AlignCenter)")
              eval(f"self.tableWidget.setCellWidget({i},{j},self.authorURL_{i})")
              continue
            case 'Living':
                val=core.Public_v['Obj'][someOne]['msg']
            case 'isWatch':
              setattr(self,f'isWatch_{i}',QPushButton())
              eval(f"self.isWatch_{i}.setObjectName('isWatch_{i}')")
              eval(f"self.isWatch_{i}.clicked.connect(self.Clicked)")

              if bl:
                eval(f"self.isWatch_{i}.setEnabled({True})")
                eval(f"self.isWatch_{i}.setText('观看')")
                if core.Public_v['Obj'][someOne]['isWatch']:
                  eval(f"self.isWatch_{i}.setEnabled({False})")
                  eval(f"self.isWatch_{i}.setText('正在观看')")
                else:
                  eval(f"self.isWatch_{i}.setEnabled({True})")
                  eval(f"self.isWatch_{i}.setText('观看')")
              else:
                eval(f"self.isWatch_{i}.setText('观看')")
                eval(f"self.isWatch_{i}.setEnabled({False})")

              eval(f"self.tableWidget.setCellWidget({i},{j},self.isWatch_{i})")
              continue
            case 'isRecord':
              setattr(self,f'Radio_{i}',QRadioButton())
              eval(f"self.Radio_{i}.setObjectName('Radio_{i}')")
              # eval(f"self.Radio_{i}.setText('录制')")
              eval(f"self.Radio_{i}.setLayoutDirection(Qt.LeftToRight)")
              eval(f"self.Radio_{i}.clicked.connect(self.Clicked)")
              if eval(f"self.checkbox_{i}.isChecked()") or core.Public_v['Obj'][someOne]['recoding']:
                eval(f"self.Radio_{i}.setChecked(True)")
              eval(f"self.Radio_{i}.setEnabled({bl})")
              eval(f"self.tableWidget.setCellWidget({i},{j},self.Radio_{i})")
              continue
          self.tableWidget.setItem(i, j, QTableWidgetItem(val))
        self.tableWidget.resizeColumnsToContents()# 根据内容自动调整列宽
    except Exception as e:
      print('错误:',e)  
# ------------------------------------------------------------------------------
  def Clicked(self):
    sender = self.sender()  # 获取触发事件的子控件
    objName=sender.objectName()
    which=objName.split('_')
    note=self.tableWidget.item(int(which[1]),2).text()
    dot=self.tableWidget.item(int(which[1]),1).text()
    key=f'{dot}.{note}'
    match which[0]:
      case 'checkbox': 
        isCek=eval(f"self.{objName}.isChecked()")
        eval(f"self.Radio_{which[1]}.setChecked({isCek})")
        core.Public_v['Obj'][key]['isRecord']=isCek
      case 'isWatch':
        core.Public_v['Obj'][key]['isWatch']=True
        core.Public_v['Obj'][key]['watching']=True
        eval(f"self.isWatch_{which[1]}.setEnabled(False)")
        watchParamPrepare(key)
      case 'Radio':
        core.Public_v['Obj'][key]['recoding']=True

