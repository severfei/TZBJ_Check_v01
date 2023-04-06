# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo



# MEL转PY
def ezMel2Python(*args):
    from MeltoPY import ezMel2Python
    ezMel2Python.ezMel2Python()
    logDate = datetimeinfo.dateTimeInfo()
    fieldText = logDate + u'已打开MEL转Python插件\n'
    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)