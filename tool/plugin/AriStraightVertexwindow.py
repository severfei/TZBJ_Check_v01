# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# 启动AriStraightVertex插件
def AriStraightVertexwindow(*args):
    # mel_script = os.path.join(os.path.dirname('__file__'), 'AriPolygonCounter.mel')
    mel_script = os.path.join('D:/TZBJ_Check_v01/script/AriStraightVertex.mel')
    try:
        pm.mel.eval("source \"{}\";".format(mel_script))
        pm.mel.eval('AriStraightVertex')
        logDate = datetimeinfo.dateTimeInfo()
        fieldText = logDate + u'已打开AriStraightVertex插件！！\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    except:
        'MelError'
        logDate = datetimeinfo.dateTimeInfo()
        fieldText = logDate + u'打开AriStraightVertex插件出错！！\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
