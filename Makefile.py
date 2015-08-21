#!/usr/bin/python
# -*- coding:utf-8 -*-
from distutils.core import setup
import py2exe
import time,shutil,os,glob

TIME = time.time()
print u"Pack Begining 开始打包"

DATA = [ ("imageformats", glob.glob("C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats\*.dll")),
         ("platforms", glob.glob("C:\Python27\Lib\site-packages\PyQt5\plugins\platforms\*.dll"))
    ]

setup(
    version = "1.0",
    description = u"Drrr Project",
    name = "Drrr",
    url = None,
    author = u'harry159821',
    author_email = u'harry159821@gmail.com',
    license = "Harry159821 License",
    zipfile= None, 
    windows=[{
                "script":"DrrrChatRoom.py", # 列举出转换成GUI窗口程序的脚本
                'icon_resources': [(0, './drrr.ico')],  # 程序图标
                'copyright': "Copyright (c) 2015 harry159821." # copyright
            }],
    data_files = DATA,
    options={
        "py2exe":{
            # "optimize":2,       # 优化
            "compressed":False, # 压缩
            "bundle_files":3,   # 3 为不压缩pyd
            # "bundle_files":2,   # 1 为单文件
            # "dist_dir":".",   # 编译指向文件夹
            "includes":["sip",  # 包含的库
                        "PyQt5.QtGui", 
                        "PyQt5.QtCore",
                        "PyQt5.QtWebKitWidgets",
                        "PyQt5.QtNetwork",
                        "PyQt5.QtWebKit",
                        "PyQt5.QtPrintSupport",
                        ],  
            # "dll_excludes":["msvcm90.dll", # 不包含的DLL库
            #                 "msvcp90.dll", 
            #                 "msvcr90.dll"]
                }
            }
    )

print u"Pack Ending 打包完毕"
print u'用时:',time.time()-TIME

if os.path.isdir('build'): # 清除build文件夹
    shutil.rmtree('build')
    pass