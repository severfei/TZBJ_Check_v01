# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo
logDate = datetimeinfo.dateTimeInfo()

# 一键清理未知插件节点

def checkUnknownPlugin(*args):
    nonParallel = []
    unknownPluginList = cmds.unknownPlugin(q=True, l=True)
    if unknownPluginList == None:
        print ("OK! 文件中不存在未知插件节点 ")
        fieldText = logDate + u'【文件中不存在未知插件节点】 check OK!\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
        cmds.button('pluginnodesCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.button('pluginnodesClearbtn', e=True, en=False)
    else:
        fieldText = logDate + u'******* Error *******\n【文件存在未知插件节点】，请清理场景！\n'
        fieldText += "以下是未知插件节点列表：\n"
        for node in unknownPluginList:
            fieldText += node + "\n"
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
        def clearUnknownplugin(*args):
            try:
                for row in unknownPluginList:
                    nonParallel.append(row)
                    cmds.unknownPlugin(row, r=True)
                # cmds.button('pluginnodesClearbtn', e=True, en=False)
                fieldText = logDate + u'已清理文件中的未知插件节点\n'
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
                checkUnknownPlugin()
            except:
                fieldText = logDate + u'如果遇到清理不掉的未知插件\n请用【一键文件垃圾清理】进行场景整体清除！\n'
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
        cmds.button('pluginnodesCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('pluginnodesClearbtn',e=True, en=True,c=clearUnknownplugin)

