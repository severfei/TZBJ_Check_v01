# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# 一键去除空间名
def RemoveAllNamespaces(*args):
    allNodes = pm.ls()
    # 获取文件中所有的node节点
    # Loop Through Them
    for node in allNodes:
        buffer = []
        # 标记和重命名
        buffer = node.split(":")
        newName = buffer[- 1]
        pm.catch(lambda: pm.rename(node, newName))
    logDate = datetimeinfo.dateTimeInfo()
    fieldText = logDate + u'空间名清除完毕！！\n'
    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
