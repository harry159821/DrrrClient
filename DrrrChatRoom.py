# -*- coding:utf-8 -*-

import sys
from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream, QUrl
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKit import QWebSettings
from PyQt5 import QtGui,QtCore,Qt,uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
import chardet

VERSION = 0.1
'''
http://qt.apidoc.info/5.1.1/qtdoc-online/classes.html
'''

# 图标按钮类重写类
class labelBtn(QtWidgets.QLabel):
    Clicked = QtCore.pyqtSignal(str)
    Entered = QtCore.pyqtSignal(str)
    Leaved = QtCore.pyqtSignal(str)
    Moved = QtCore.pyqtSignal(str,int,int)

    def __init__(self,name,timeoutset=None,parent=None):
        super(labelBtn,self).__init__()
        self.setMouseTracking(True)
        self.name = name
            
    def mouseReleaseEvent(self,event):
        self.Clicked.emit(self.name)
        
    def mouseMoveEvent(self,event):
        self.Moved.emit(self.name,event.globalPos().x(),event.globalPos().y())
        
    def enterEvent(self,event):
        self.Entered.emit(self.name)
   
    def leaveEvent(self,event):
        self.Leaved.emit(self.name)

class FrameLessTransparentWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FrameLessTransparentWindow,self).__init__()
        self.isMaxShow = 0
        self.setMouseTracking(True)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

    # def paintEvent(self,event):
    #     # 窗口阴影
    #     p = QtGui.QPainter(self)
    #     p.drawPixmap(0, 0, self.rect().width(), 
    #         self.rect().height(), QtGui.QPixmap('img/main_shadow2.png'))

    def minFunc(self,name):
        '''最小化函数'''
        self.minAnimation = QtCore.QPropertyAnimation(self,"windowOpacity")
        self.minAnimation.finished.connect(self.showMinimized2)
        self.minAnimation.setDuration(200)
        self.minAnimation.setStartValue(1)
        self.minAnimation.setEndValue(0)
        self.minAnimation.start()

    def showMinimized2(self):
        self.showMinimized()
        self.setWindowOpacity(1)

    def maxFunc(self,name):
        '''切换窗口模式'''
        if self.isMaxShow:
            self.verticalLayout.setContentsMargins(20,12,17,17)
            self.showNormal()
            self.isMaxShow = 0
        else:
            self.verticalLayout.setContentsMargins(0,0,0,0)
            self.showMaximized()
            self.isMaxShow = 1

    def closeFunc(self,name):
        '''窗口关闭函数'''
        self.closeAnimation = QtCore.QPropertyAnimation(self,"windowOpacity")
        self.closeAnimation.setDuration(200)
        self.closeAnimation.setStartValue(1)
        self.closeAnimation.setEndValue(0)
        self.closeAnimation.finished.connect(self.exitFunc)
        self.closeAnimation.start()

    def exitFunc(self):
        '''全部退出'''
        self.close()

    def buttonEnterFunc(self,name):
        '''按钮鼠标进入事件'''
        exec(str(('self.'+name+'PushButton.setPixmap(QtGui.QPixmap(r"./img/'+name+'.png"))').encode("utf-8")))

    def buttonLeavedFunc(self,name):
        '''按钮鼠标离开事件'''
        exec(str(('self.'+name+'PushButton.setPixmap(QtGui.QPixmap(r"./img/'+name+'Normal.png"))').encode("utf-8")))
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            self.globalPositon = event.globalPos()
            self.oldGeometry = self.geometry()
            self.oldSize = self.size()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # print event.globalPos(),self.dragPosition,self.pos().x()+self.size().width(),
                # self.pos().y()+self.size().height()
            # print self.dragPosition.x(),self.dragPosition.y()
            if self.dragPosition.x() < 12:
                if self.dragPosition.y() < 12:
                    # print "左上"
                    x = event.globalPos().x()-self.globalPositon.x()
                    y = event.globalPos().y()-self.globalPositon.y()  
                    self.setGeometry(self.oldGeometry.x()+x,self.oldGeometry.y()+y,
                        self.oldGeometry.width()-x,self.oldGeometry.height()-y)                                                         
                elif self.oldSize.height() - self.dragPosition.y() < 12:
                    x = event.globalPos().x()-self.globalPositon.x()
                    y = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y(),
                        self.oldGeometry.width(),self.oldGeometry.height()+y)                     
                    self.setGeometry(self.oldGeometry.x()+x,self.oldGeometry.y(),
                        self.oldGeometry.width()-x,self.oldGeometry.height()+y)                     
                    # print "左下"
                else:
                    num = event.globalPos().x()-self.globalPositon.x()
                    self.setGeometry(self.oldGeometry.x()+num,self.oldGeometry.y(),
                        self.oldGeometry.width()-num,self.oldGeometry.height())                    
                    # print "左"
            elif self.oldSize.width() - self.dragPosition.x() < 12:
                if self.dragPosition.y() < 12:
                    x = event.globalPos().x()-self.globalPositon.x()
                    y = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y()+y,
                        self.oldGeometry.width()+x,self.oldGeometry.height()-y)
                    # print "右上"
                elif self.oldSize.height() - self.dragPosition.y() < 12:
                    x = event.globalPos().x()-self.globalPositon.x()
                    y = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y(),
                        self.oldGeometry.width()+x,self.oldGeometry.height()+y)
                    # print "右下"
                else:
                    num = event.globalPos().x()-self.globalPositon.x()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y(),
                        self.oldGeometry.width()+num,self.oldGeometry.height())
                    # print "右"
            else:
                if self.dragPosition.y() < 12:
                    num = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y()+num,
                        self.oldGeometry.width(),self.oldGeometry.height()-num)                      
                    # print "上"
                elif self.oldSize.height() - self.dragPosition.y() < 12:
                    num = event.globalPos().y()-self.globalPositon.y()
                    self.setGeometry(self.oldGeometry.x(),self.oldGeometry.y(),
                        self.oldGeometry.width(),self.oldGeometry.height()+num)           
                    # print "下"          
                else:
                    # print "中"
                    self.move(event.globalPos() - self.dragPosition)                
            event.accept()

        self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
        self.oldSize = self.size()
        if self.dragPosition.x() < 12:
            if self.dragPosition.y() < 52:
                # self.setCursor(QtCore.Qt.SizeFDiagCursor)
                pass
            elif self.oldSize.height() - self.dragPosition.y() < 12:
                self.setCursor(QtCore.Qt.SizeBDiagCursor)
            else:
                self.setCursor(QtCore.Qt.SizeHorCursor)
        elif self.oldSize.width() - self.dragPosition.x() < 12:
            if self.dragPosition.y() < 52:
                # self.setCursor(QtCore.Qt.SizeBDiagCursor)
                pass
            elif self.oldSize.height() - self.dragPosition.y() < 12:
                self.setCursor(QtCore.Qt.SizeFDiagCursor)
            else:
                self.setCursor(QtCore.Qt.SizeHorCursor)
        else:
            if self.dragPosition.y() < 52:
                # self.setCursor(QtCore.Qt.SizeVerCursor)
                pass
            elif self.oldSize.height() - self.dragPosition.y() < 12:
                self.setCursor(QtCore.Qt.SizeVerCursor)
            else:
                self.setCursor(QtCore.Qt.ArrowCursor)

    def leaveEvent(self,event):
        # print "leaveEvent"
        self.setCursor(QtCore.Qt.ArrowCursor)

class ShadowsWindow(FrameLessTransparentWindow):
    def __init__(self):
        super(ShadowsWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  
        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.SHADOW_WIDTH=10

    def drawShadow(self,painter):
        # 绘制边框
        # self.pixmaps=QStringList()
        self.pixmaps=[]
        self.pixmaps.append("./img/shadow/left_top.png")
        self.pixmaps.append("./img/shadow/left_bottom.png")
        self.pixmaps.append("./img/shadow/right_top.png")
        self.pixmaps.append("./img/shadow/right_bottom.png")
        self.pixmaps.append("./img/shadow/top_mid.png")
        self.pixmaps.append("./img/shadow/bottom_mid.png")
        self.pixmaps.append("./img/shadow/left_mid.png")
        self.pixmaps.append("./img/shadow/right_mid.png")
        painter.drawPixmap(0, 0, 
            self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[0]))   # 左上角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, 0, 
            self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[2]))   # 右上角
        painter.drawPixmap(0,self.height()-self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[1]))   # 左下角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[3]))  # 右下角
        painter.drawPixmap(0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, 
            self.height()-2*self.SHADOW_WIDTH, 
            QPixmap(self.pixmaps[6]).scaled(self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH)) # 左
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH, 
            QPixmap(self.pixmaps[7]).scaled(self.SHADOW_WIDTH, self.height()- 2*self.SHADOW_WIDTH)) # 右
        painter.drawPixmap(self.SHADOW_WIDTH, 0, self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, 
            QPixmap(self.pixmaps[4]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH)) # 上
        painter.drawPixmap(self.SHADOW_WIDTH, 
            self.height()-self.SHADOW_WIDTH, 
            self.width()-2*self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH, QPixmap(self.pixmaps[5]).scaled(self.width()-2*self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH))   # 下        
        
    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawShadow(painter)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        # painter.drawRect(QRect(self.SHADOW_WIDTH, self.SHADOW_WIDTH,
            # self.width()-2*self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH))

class titleBar(QWidget):
    def __init__(self,parent=None):
        super(titleBar,self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)  
        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.SHADOW_WIDTH = 30
        self.resize(1000,self.SHADOW_WIDTH)
        self.setMinimumHeight(self.SHADOW_WIDTH)
        self.setMouseTracking(True)

        # return
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
        self.setAttribute(Qt.WA_PaintOnScreen)
        # self.setStyleSheet('''
        #                 border-bottom: 0px solid rgb(170, 170, 170);
        #                 background: qlineargradient(spread:reflect,
        #                 x1:1, y1:1, x2:1, y1:1,
        #                 stop:1 rgba(250, 250, 250, 255),
        #                 stop:0 rgba(170, 170, 170, 255));
        #             ''')
        self.setStyleSheet("""
            .QMainWindow
            {
                background:transparent;
                border-bottom:10px;
            }
            .QWidget
            {
                border-top-left-radius:     8px;
                border-top-right-radius:    8px;
                border-bottom-right-radius: 0px;
                border-bottom-left-radius:  0px;
                border-style: solid;
                background: qlineargradient(spread:reflect,
                x1:1, y1:1, x2:1, y1:1,
                stop:1 rgba(230, 230, 230, 255),
                stop:0 rgba(175, 175, 175, 255));

                border-top:     1px solid #919191;
                border-left:    1px solid #919191;
                border-right:   1px solid #919191;
                border-bottom:  1px solid #919191;
            }
            """)

        self.title_label = QLabel()
        self.title_label.setText(u"    DRRR Chat Room")

        self.font = QtGui.QFont()
        self.font.setPixelSize(22)   # 设置字号32,以像素为单位
        self.font.setFamily("SimSun")# 设置字体，宋体
        # self.font.setFamily(u"微软雅黑")
        self.font.setBold(True)
        self.font.setItalic(False)   # 设置字型,不倾斜
        self.font.setUnderline(False)# 设置字型,无下划线

        self.title_label.setFont(self.font)

        self.close_button = QLabel()
        self.min_button   = QLabel()
        self.max_button   = QLabel()

        self.close_button.setPixmap(QPixmap("./img/orange.png"))
        self.min_button.setPixmap(QPixmap("./img/green.png"))
        self.max_button.setPixmap(QPixmap("./img/blue.png"))

        self.close_button.setFixedSize(15,15)
        self.min_button.setFixedSize(15,15)
        self.max_button.setFixedSize(15,15)

        self.close_button.setStyleSheet(""" 
                                    background:transparent
                                    """)
        self.min_button.setStyleSheet(""" 
                                    background:transparent
                                    """)
        self.max_button.setStyleSheet(""" 
                                    background:transparent
                                    """)
        self.title_label.setStyleSheet(""" 
                                    background:transparent;
                                    color:rgba(70,70,70,255);
                                    """)

        self.close_button.setScaledContents(True)
        self.min_button.setScaledContents(True)
        self.max_button.setScaledContents(True)

        self.searchLine = QLineEdit()
        self.searchLine.setStyleSheet(""" 
                                    border:2px groove gray;
                                    border-radius:10px;
                                    text-align:center;
                                    padding:2px 10px;
                                    background:white;
                                    """)

        # 水平管理器
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 20, 0)
        self.title_layout.addWidget(self.title_label,1,Qt.AlignCenter)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button,0,Qt.AlignVCenter)
        self.title_layout.addWidget(self.min_button  ,0,Qt.AlignVCenter)
        self.title_layout.addWidget(self.max_button  ,0,Qt.AlignVCenter)

        self.setLayout(self.title_layout)

    def drawShadow(self,painter):
        # 绘制边框
        # self.pixmaps=QStringList()
        self.pixmaps=[]
        self.pixmaps.append("./img/leftTopStatus.png")
        self.pixmaps.append("./img/shadow/left_bottom.png")
        self.pixmaps.append("./img/rightTopStatus.png")
        self.pixmaps.append("./img/shadow/right_bottom.png")
        self.pixmaps.append("./img/midTopStatus.png")
        self.pixmaps.append("./img/shadow/bottom_mid.png")
        self.pixmaps.append("./img/shadow/left_mid.png")
        self.pixmaps.append("./img/shadow/right_mid.png")
        painter.drawPixmap(0, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, 
            QPixmap(self.pixmaps[0]))   # 左上角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, 0, self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH, QPixmap(self.pixmaps[2]))   # 右上角
        painter.drawPixmap(self.SHADOW_WIDTH, 0, self.width()-2*self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH, QPixmap(self.pixmaps[4]).scaled(self.width()-2*self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH)) # 上

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawShadow(painter)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        # painter.drawRect(QRect(self.SHADOW_WIDTH, self.SHADOW_WIDTH, 
            # self.width()-2*self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH))

    def enterEvent(self,event):
        self.setCursor(QtCore.Qt.ArrowCursor)

class StatusWindow(QMainWindow):
    def __init__(self):
        super(StatusWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.SHADOW_WIDTH = 25
        self.resize(1000,self.SHADOW_WIDTH)
        self.setMinimumHeight(self.SHADOW_WIDTH)
        self.setMouseTracking(True)

        self.font = QtGui.QFont()
        self.font.setPixelSize(18)   # 设置字号32,以像素为单位
        self.font.setFamily("SimSun")# 设置字体，宋体
        self.font.setBold(True)
        self.font.setItalic(False)   # 设置字型,不倾斜
        self.font.setUnderline(False)# 设置字型,无下划线
        self.status = QLabel(self)
        self.status.move(20,-2)        
        self.status.setFont(self.font)

        self.status.setText("Connected")

    def drawShadow(self,painter):
        # 绘制边框
        # self.pixmaps=QStringList()
        self.pixmaps=[]
        self.pixmaps.append("images/left_top.png")
        self.pixmaps.append("./img/leftStatus.png")
        self.pixmaps.append("images/right_top.png")
        self.pixmaps.append("./img/rightStatus.png")
        self.pixmaps.append("images/top_mid.png")
        self.pixmaps.append("./img/midStatus.png")
        self.pixmaps.append("images/left_mid.png")
        self.pixmaps.append("images/right_mid.png")
        painter.drawPixmap(0,self.height()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH, QPixmap(self.pixmaps[1]))   # 左下角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, 
            self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[3]))  # 右下角
        painter.drawPixmap(self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, 
            self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, 
            QPixmap(self.pixmaps[5]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH))   # 下        
        
    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawShadow(painter)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        # painter.drawRect(QRect(self.SHADOW_WIDTH, self.SHADOW_WIDTH, 
            # self.width()-2*self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH))

class NetworkReply(QNetworkReply):
    def __init__(self, reply):
        self.reply = reply
        QNetworkReply.__init__(self)

        # QMetaObject::invokeMethod(this, "downloadProgress", 
                # Qt::QueuedConnection, Q_ARG(qint64, m_content.size()), Q_ARG(qint64, m_content.size()));

        QMetaObject.invokeMethod(self, "readyRead",
                Qt.QueuedConnection)
        QMetaObject.invokeMethod(self, "finished",
                Qt.QueuedConnection)
        QMetaObject.invokeMethod(self, "metaDataChanged", 
                Qt.QueuedConnection)


        print self.readyRead.emit()
        print self.finished.emit()
        # print self.encrypted
        # print self.sslErrors

        # handle these to forward
        # self.reply.metaDataChanged.connect(self.applyMetaData)
        self.reply.metaDataChanged.connect(self.metaDataChanged)

        self.reply.readyRead.connect(self.readInternal)
        self.reply.error.connect(self.errorInternal)
        # forward signals
        self.reply.finished.connect(self.finished)
        # self.reply.uploadProgress.connect(self.uploadProgress)
        # self.reply.downloadProgress.connect(self.downloadProgress)
 
        self.setOpenMode(QNetworkReply.ReadOnly)
        self.data = self.buffer = ''
 
    def operation(self):
        return self.reply.operation()
 
    def request(self):
        return self.reply.request()
 
    def url(self):
        return self.reply.url()
 
    def abort(self):
        self.reply.abort()
 
    def close(self):
        self.reply.close()
 
    def isSequential(self):
        return self.reply.isSequential()
 
    def setReadBufferSize(self, size):
        QNetworkReply.setReadBufferSize(size)
        self.reply.setReadBufferSize(size)
 
    def applyMetaData(self):
        for header in self.reply.rawHeaderList():
            self.setRawHeader(header, self.reply.rawHeader(header))
 
        self.setHeader(QNetworkRequest.ContentTypeHeader, self.reply.header(QNetworkRequest.ContentTypeHeader))
        self.setHeader(QNetworkRequest.ContentLengthHeader, self.reply.header(QNetworkRequest.ContentLengthHeader))
        self.setHeader(QNetworkRequest.LocationHeader, self.reply.header(QNetworkRequest.LocationHeader))
        self.setHeader(QNetworkRequest.LastModifiedHeader, self.reply.header(QNetworkRequest.LastModifiedHeader))
        self.setHeader(QNetworkRequest.SetCookieHeader, self.reply.header(QNetworkRequest.SetCookieHeader))
 
        self.setAttribute(QNetworkRequest.HttpStatusCodeAttribute, self.reply.attribute(QNetworkRequest.HttpStatusCodeAttribute))
        self.setAttribute(QNetworkRequest.HttpReasonPhraseAttribute, self.reply.attribute(QNetworkRequest.HttpReasonPhraseAttribute))
        self.setAttribute(QNetworkRequest.RedirectionTargetAttribute, self.reply.attribute(QNetworkRequest.RedirectionTargetAttribute))
        self.setAttribute(QNetworkRequest.ConnectionEncryptedAttribute, self.reply.attribute(QNetworkRequest.ConnectionEncryptedAttribute))
        self.setAttribute(QNetworkRequest.CacheLoadControlAttribute, self.reply.attribute(QNetworkRequest.CacheLoadControlAttribute))
        self.setAttribute(QNetworkRequest.CacheSaveControlAttribute, self.reply.attribute(QNetworkRequest.CacheSaveControlAttribute))
        self.setAttribute(QNetworkRequest.SourceIsFromCacheAttribute, self.reply.attribute(QNetworkRequest.SourceIsFromCacheAttribute))
        # attribute does not exist
        #self.setAttribute(QNetworkRequest.DoNotBufferUploadDataAttribute, self.reply.attribute(QNetworkRequest.DoNotBufferUploadDataAttribute))
        self.metaDataChanged.emit()

    def errorInternal(self, e):
        self.error.emit(e)
        self.setError(e, str(e))
 
    def readInternal(self):
        # this is called 
        print self.reply
        s = self.reply.readAll()
        self.data += s
        self.buffer += s
        self.readyRead.emit()
 
    def bytesAvailable(self):
        return len(self.buffer) + self.reply.bytesAvailable()
 
    def readAll(self):
        # this is never called
        return self.data

    def read(self,size):
        return self.readData(size)

    def readData(self, maxSize):
        return "test"

        if self.offset < len(self.content):
            end = min(self.offset + maxSize, len(self.content))
            data = self.content[self.offset:end]
            self.offset = end
            # return data
            print str(data)
            return str(data)

class DownloadReply(QNetworkReply):
    # readyRead = pyqtSignal()
    # finished  = pyqtSignal()
    # sslErrors = pyqtSignal(list)

    def __init__(self, parent, url, operation):
        QNetworkReply.__init__(self, parent)
        self.content = "<html><head><title>Test</title></head><body>This is a test.</body></html>"
        self.offset = 0            

        self.setHeader(QNetworkRequest.ContentTypeHeader, QVariant("text/html; charset=ASCII"))
        self.setHeader(QNetworkRequest.ContentLengthHeader, QVariant(len(self.content)))
        # QTimer.singleShot(0, self, SIGNAL("readyRead()"))        
        # QTimer.singleShot(0, self, SIGNAL("finished()"))
        self.readyRead.emit()
        self.finished.emit()
        self.open(self.ReadOnly | self.Unbuffered)
        self.setUrl(url)
    
    def abort(self):
        print "abort"
        pass
    
    def bytesAvailable(self):
        print 'bytesAvailable'
        # NOTE:
        # This works for Win:
        #      return len(self.content) - self.offset
        # but it does not work under OS X. 
        # Solution which works for OS X and Win:
        #     return len(self.content) - self.offset + QNetworkReply.bytesAvailable(self)
        return len(self.content) - self.offset
    
    def isSequential(self):
        print 'isSequential'
        return True
    
    def read(self):
        print "read"
        pass

    def readData(self, maxSize):        
        print 'readData'
        if self.offset < len(self.content):
            end = min(self.offset + maxSize, len(self.content))
            data = self.content[self.offset:end]
            self.offset = end
            print str(data)
            return data
            return str(data)

class NetworkAccessManager(QNetworkAccessManager):

    def __init__(self, old_manager):
    
        QNetworkAccessManager.__init__(self)
        self.old_manager = old_manager
        self.setCache(old_manager.cache())
        self.setCookieJar(old_manager.cookieJar())
        self.setProxy(old_manager.proxy())
        self.setProxyFactory(old_manager.proxyFactory())

    def customReplyFinished(self):
        self.finished.emit(self.sender())

    def getData(self):
        # data = self.reply.readAll()
        # print data
        # self.reply.reset()
        # self.reply.writeData(data)
        # self.reply.offset = 0
        pass

    def createRequest(self, operation, request, data):

        # replyy = QNetworkReplyImpl()

        print operation,request.url()
        # return QNetworkAccessManager.createRequest(self, operation, request, data)

        # reply = DownloadReply(self, request.url(), self.GetOperation)
        # return reply

        # return NetworkReply(QNetworkAccessManager.createRequest(self, operation, request, data))

        if operation == self.GetOperation and 'http://drrr.com/xml.php' in str(request.url()):
            self.networkReply = NetworkReply(QNetworkAccessManager.createRequest(self, operation, request, data))
            return self.networkReply
            
            print request.url()
            reply = DownloadReply(self, request.url(), self.GetOperation)
            # reply.finished.connect(self.customReplyFinished)
            return reply

            # self.reply = QNetworkAccessManager.createRequest(self, operation, request, data)
            # self.request = request
            # self.data = data
            # self.reply.readyRead.connect(self.getData)
            # return self.reply

        else:
            return QNetworkAccessManager.createRequest(self, operation, request, data)

        if request.url().scheme() != "download":
            pass
            # return QNetworkAccessManager.createRequest(self, operation, request, data)
        
        if operation == self.GetOperation:
            print "GetOperation"
            # Handle download:// URLs separately by creating custom
            # QNetworkReply objects.
            reply = DownloadReply(self, request.url(), self.GetOperation)
            return reply
        else:
            return QNetworkAccessManager.createRequest(self, operation, request, data)

class DrrrWindow(ShadowsWindow):
    def __init__(self):
        super(DrrrWindow, self).__init__()
        self.setWindowTitle("Drrr Chat Room")

        self.WebView = QWebView()
        self.WebView.resize(3000,3000)
        # self.WebView.load(QUrl("http://drrr.com/"))
        # self.WebView.load(QUrl("file:///E:/Project/DrrrPC/img/index.html"))
        self.WebView.setZoomFactor(0.8)

        self.WebView.loadStarted.connect(self.loadStarted)
        self.WebView.loadFinished.connect(self.loadFinished)
        self.WebView.loadProgress.connect(self.loading)

        # self.connect(self.WebView, SIGNAL("loadStarted(bool)"), self.loadStarted)
        # self.connect(self.WebView, SIGNAL("loadFinished(bool)"), self.loadFinished)
        # self.connect(self.WebView, SIGNAL("loadProgress(int)"), self.loading)

        self.cookieJar = QNetworkCookieJar()
        self.WebView.page().networkAccessManager().setCookieJar(self.cookieJar)
        # self.WebView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.WebView.page().linkClicked.connect(self.linkClicked)
        self.WebView.page().contentsChanged.connect(self.contentsChanged)
        # self.WebView.page().networkAccessManager().setHeader(QNetworkRequest.ContentTypeHeader, QVariant("text/html; charset=GBK"))

        self.WebView.page().javaScriptAlert = self._javascript_alert                
        self.WebView.page().javaScriptConsoleMessage = self._javascript_console_message
        self.WebView.page().javaScriptConfirm = self._javascript_confirm
        self.WebView.page().javaScriptPrompt = self._javascript_prompt

        # NetworkAccessManager
        # self.NetworkAccessManager = QNetworkAccessManager()
        # self.WebView.page().setNetworkAccessManager(self.NetworkAccessManager)
        # self.NetworkAccessManager.finished.connect(self.NetworkAccessManagerReplyFinished)        
        # self.NetworkAccessManager.get(QNetworkRequest(QUrl("http://www.baidu.com")))        

        self.old_manager = self.WebView.page().networkAccessManager()
        self.new_manager = NetworkAccessManager(self.old_manager)
        self.WebView.page().setNetworkAccessManager(self.new_manager)

        self.titlebar = titleBar()
        self.statusBar = StatusWindow()

        # 中心窗口布局
        self.contentLayout = QVBoxLayout()
        self.contentWidget = QWidget()
        self.contentWidget.gridLayout = QtWidgets.QGridLayout(self.contentWidget)
        self.contentWidget.gridLayout.addLayout(self.contentLayout, 0, 0, 1, 1)
        self.contentLayout.addWidget(self.WebView)
        self.contentWidget.gridLayout.setContentsMargins(0,0,0,0)
        self.contentLayout.setContentsMargins(1,0,1,0)
        self.contentWidget.setStyleSheet("""
            border-left:    1px solid black;
            border-right:   1px solid black;
            """)

        # self.titlebar.titlebarBotton = QPushButton(self.titlebar)
        # self.titlebar.titlebarBotton.setText('Push ME')
        # self.titlebar.titlebarBotton.clicked.connect(self.getData)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.titlebar)
        self.main_layout.addWidget(self.contentWidget)
        self.main_layout.addWidget(self.statusBar)
        self.main_layout.setSpacing(0)

        # 窗口属性
        self.setWindowFlags(Qt.Widget | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
        
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.main_layout)
        self.widget.setMouseTracking(True)        
        # self.resize(500,650)
        self.resize(650,650)
        self.center()

        self.WebView.load(QUrl("http://drrr.com/"))
        self.show()

    def center(self,screenNum=0):
        '''多屏居中支持'''
        self.desktop = QApplication.desktop()
        screen = self.desktop.availableGeometry(screenNum)
        size = self.geometry()
        self.normalGeometry2 = QtCore.QRect((screen.width()-size.width())/2+screen.left(),
                         (screen.height()-size.height())/2,
                         size.width(),size.height())
        self.setGeometry((screen.width()-size.width())/2+screen.left(),
                         (screen.height()-size.height())/2,
                         size.width(),size.height())

    def getData(self):
        print self.bbb == None
        print str(self.bbb)

    def readyRead(self):
        pass
        # print self.NetworkAccessManager.readAll()

    def NetworkAccessManagerReplyFinished(self,response):
        # NO USE
        print response.readAll()
        # print response.header(QNetworkRequest.ContentTypeHeader)
        # print response.url()
        # print chardet.detect(response.readAll().data())
        # print response.readAll().data().encode("utf-8")
        # print response
        # self.bbb = response.readAll()
        # print self.bbb == None

        if 'http://drrr.com/xml.php' in response.url().toString():
            # print response.readAll().data().encode("utf-8")
            # print QString.fromAscii(response.readAll())
            pass
        response.deleteLater()

    def contentsChanged(self):
        print 'contentsChanged'
        pass

    def _javascript_alert(self, webframe, message):
        print '_javascript_alert'
        
    def _javascript_console_message(self, message, line, sourceid):
        print "_javascript_console_message"

    def _javascript_confirm(self, webframe, message):
        print "_javascript_confirm"
        return QWebPage.javaScriptConfirm(self.WebView.page(), webframe, message)

    def _javascript_prompt(self, webframe, message, defaultvalue, result):
        print "_javascript_prompt"

    def linkClicked(self,url):
        print url

    def loadStarted(self):
        print 'requestedUrl:' + self.WebView.page().mainFrame().requestedUrl().toString()
    
    def loadFinished(self, flag):
        '''
        findFirst里的参数语法#号开头的查找id名的，
        点号”.”开头的则是查找class名字的，
        如果没有前面符号的则是查找标准HTML标记比如findFirst(“body”)
        http://www.w3.org/TR/CSS2/selector.html#q1
        网页源代码:self.WebView.page().currentFrame().toHtml().toUtf8()
        set value的方法:setText,setAttribute
        get 的方法:
            Text = TextInput.attribute("value")
            frame.findAllElements("input[name=submit]") 
            updates.evaluateJavaScript("this.checked").toBool()   (check框)
            firstName.evaluateJavaScript("this.value").toString()   (普通)
        
        <div id=”in_nav”>
        上一篇：<a title=”新股中签的回报率” href=”/yobin/blog/item/86ad9223e5add74fad34de92.html”>新股中签的回报率</a>
        下一篇：<a title=”人民时评：且看美国的信息自由” href=”/yobin/blog/item/dc3491587b51cbd59c8204ba.html”>人民时评：且看美国的信息自由</a></div>

        QWebElement e_nav=m_blog.findFirst("#in_nav");
        QWebElement prev_nav=e_nav.findFirst("a");

        '''
        self.statusBar.status.setText(u"Connected")

        # effect.mp3

        # print 'loadFinished:' + str(self.WebView.url().toString())

        if 'http://drrr.com/lounge/' in str(self.WebView.url().toString()):
            frame = self.WebView.page().mainFrame().toHtml()
            # print 'effect.mp3:','effect.mp3' in frame
            # if 'http://drrr.com/js/effect.mp3' in frame:
                # self.WebView.setHtml(frame.replace('http://drrr.com/js/effect.mp3','effect.mp3'))


        if 'https://passport.baidu.com/v2/?login' == str(self.WebView.url().toString()):

            print 'passport.baidu.com load finish'
            frame = self.WebView.page().mainFrame()
            #print doc.toPlainText().toUtf8()
            doc = frame.documentElement()
            #m_blog = doc.findFirst("#form1")
            #print m_blog.toPlainText().toUtf8()

            '''
            百度搜索
            baiduInput = doc.findFirst('input[id="kw1"]')
            baiduInput.setAttribute('value',u'我不知道')
            print baiduInput.attribute("value")
            #baiduinput.setFocus()
            baiduSearch = doc.findFirst('input[id="su1"]')
            baiduSearch.evaluateJavaScript("this.click()")
            #doc.evaluateJavaScript("document.getElementById('su1').click()")
            #baiduInput.evaluateJavaScript("javascript:F.call('ps/sug','pssubmit');")
            '''

            nameInput = doc.findFirst('input[id="TANGRAM__3__userName"]')
            #nameInput = doc.findFirst('#TANGRAM__3__userName')
            nameInput.setAttribute('value',u'harryide')
            passwordInput = doc.findFirst('input[id="TANGRAM__3__password"]')
            passwordInput.setAttribute('value',u'*******')

            loginBtn = doc.findFirst('input[id="TANGRAM__3__submit"]')
            loginBtn.evaluateJavaScript("this.click()")
                                            
            
    def loading(self, percent):
        self.statusBar.status.setText("Loading %d%%" % percent)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QNetworkProxyFactory.setUseSystemConfiguration(True)
    QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled,True)
    QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled,True)
    QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptEnabled,True)
    # QNetworkRequest.setHeader()

    drrr = DrrrWindow()

    sys.exit(app.exec_())

'''
self.nam = nam or QNetworkAccessManager()
self.page().setNetworkAccessManager(self.nam)

QWebView webView = new QWebView();
QNetworkCookieJar cookieJar = new QNetworkCookieJar();
QNetworkAccessManager nam = new QNetworkAccessManager();
nam.setCookieJar(cookieJar);
webView.page()->setNetworkAccessManager(nam);

QByteArray postData("e_user=Max&e_pwd=Secret");
QNetworkRequest netRequest;
netRequest.setUrl(QUrl("http://example.com/do_login.php"));
netRequest.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded; charset=UTF-8");

ui->webView->load(netRequest, QNetworkAccessManager::PostOperation, postData);
'''