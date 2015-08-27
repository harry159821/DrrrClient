# -*- mode: python -*-
a = Analysis(['DrrrChatRoom.py'],
             pathex=['E:\\Project\\DrrrPC'],
             hiddenimports=['PyQt5.QtNetwork', 
                            'PyQt5.QtMultimedia',
                            'PyQt5.QtPrintSupport'],
             hookspath=None,
             excludes=[
                      'PyQt5.QtOpenGL',
                      'PyQt5.QtQuick',
                      'PyQt5.QtQml',
                      'PyQt5.QtSensors',
                      'PyQt5.QtSerialPort',
                      'PyQt5.QtSql',
                      'PyQt5.QtSvg',
                      'PyQt5.QtTest',
                    ],
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='DrrrChatRoom.exe',
          debug=False,
          strip=None,
          upx=False,
          console=False , icon='drrr.ico')

Exclude_File = ["icudt",
                "icuin",
                "icuuc",
                "Qt5Qml",
                "Qt5Qmld",
                "Qt5Cored",
                "Qt5Guid",
                "Qt5OpenGL",
                "Qt5Quick",
                "Qt5Quickd",
                "Qt5Sensors",
                "Qt5SerialPort",
                "Qt5Svg",
                "Qt5Sql",
                "Qt5Test",
                "QtWebKit.dll"
                ]
for excludefile in Exclude_File:
    a.binaries = [x for x in a.binaries if excludefile not in x[1]]
for excludefile in Exclude_File:
    a.binaries = [x for x in a.binaries if excludefile not in str(x)]

a.binaries.append(('qt5_plugins\\mediaservice\\dsengine.dll', 'D:/Python27/Lib/site-packages/PyQt5/plugins\\mediaservice\\dsengine.dll', 'BINARY'))
a.binaries.append(('qt5_plugins\\mediaservice\\qtmedia_audioengine.dll', 'D:/Python27/Lib/site-packages/PyQt5/plugins\\mediaservice\\qtmedia_audioengine.dll', 'BINARY'))
a.binaries.append(('qt5_plugins\\mediaservice\\wmfengine.dll', 'D:/Python27/Lib/site-packages/PyQt5/plugins\\mediaservice\\wmfengine.dll', 'BINARY'))

for dataFile in glob.glob("img/*.*"):
    a.binaries.append((dataFile,dataFile,'BINARY'))

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=False,
               name='DrrrChatRoom')
