# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# 一键传递UV
def UVpass(*args):
    import pymel.core as pm
    logDate = datetimeinfo.dateTimeInfo()
    selAry = pm.ls(sl=1)
    for i in range(0, len(selAry)):
        pm.polyTransfer(selAry[i], vc=0, uv=1, ao=selAry[0], v=0)
    fieldText = logDate + u'UV传递完毕，请检查是否成功！\n'
    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)