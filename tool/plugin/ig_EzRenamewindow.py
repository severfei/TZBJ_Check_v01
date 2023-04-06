# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo
import script.ig_EzRename


# 启动ig_EzRename插件
def ig_EzRenamewindow(*args):
    script.ig_EzRename.UI()
    logDate = datetimeinfo.dateTimeInfo()
    fieldText = logDate + u'已打开ig_EzRename重命名插件！！\n'
    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)