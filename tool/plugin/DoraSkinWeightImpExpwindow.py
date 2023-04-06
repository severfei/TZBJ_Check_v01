# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo
from script import DoraSkinWeightImpExp


# 启动DoraSkinWeightImpExp插件
def DoraSkinWeightImpExpwindow(*args):
    mel_script = os.path.join('D:/TZBJ_Check_v01/script/DoraSkinWeightImpExp.mel')
    try:
        pm.mel.eval("source \"{}\";".format(mel_script))
        pm.mel.eval('DoraSkinWeightImpExp')
        logDate = datetimeinfo.dateTimeInfo()
        fieldText = logDate + u'已打开DoraSkinWeightImpExp插件！！\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    except:
        'MelError'
        logDate = datetimeinfo.dateTimeInfo()
        fieldText = logDate + u'打开DoraSkinWeightImpExp插件出错！！\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)