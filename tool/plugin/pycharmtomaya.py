# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# Pycharm MAYA 互通
def pycharmtomaya(*args):

    if not cmds.commandPort(":4434", query=True):
        cmds.commandPort(name=":4434")
    logDate = datetimeinfo.dateTimeInfo()
    fieldText = logDate + u'Pycharm MAYA2020互通完成！！\n'
    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    #
    if not cmds.commandPort(":4435", query=True):
        cmds.commandPort(name=":4435")
    logDate = datetimeinfo.dateTimeInfo()
    fieldText = logDate + u'Pycharm MAYA2022互通完成！！\n'
    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

