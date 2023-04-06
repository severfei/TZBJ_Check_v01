# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo


# 一键清理未知插件节点
def deleteUnknownPlugin(*args):
    logDate = datetimeinfo.dateTimeInfo()
    nonParallel = []
    unknownPluginList = cmds.unknownPlugin(q=True, l=True)
    if unknownPluginList == None:
        print ("文件中不存在未知插件节点 ")
        fieldText = logDate + u'文件中不存在未知插件节点\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        for row in unknownPluginList:
            nonParallel.append(row)
            cmds.unknownPlugin(row, r=True)
            # nonParallelPlane = cmds.ls(sl=True, flatten=True)
            # nonParallel.extend(nonParallelPlane)

            # print(u"已删除未知插件节点 : " + row)
        for i in nonParallel:
            fieldText = logDate + u'已删除未知插件节点\n' + i
            # fieldText = logDate + u'已删除未知插件节点:' + row
            cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

def check_unknown_nodes():

    unknown_nodes = cmds.ls(type='unknown')
    return unknown_nodes

# check_unknown_nodes()

def cleanup_delete_unknown_nodes():

    del_objs = []
    unknown_nodes = check_unknown_nodes()
    if unknown_nodes:
        for unknown_node in unknown_nodes:
            if not cmds.objExists(unknown_node):
                continue
            if not cmds.referenceQuery(unknown_node, inr=True):
                cmds.delete(unknown_node)
                del_objs.append(unknown_node)

    return del_objs
# cleanup_delete_unknown_nodes()
