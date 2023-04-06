# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import os
import pymel.core as pm
from tool import datetimeinfo

def CleanUp(*args):
    # 加载cleanup mel
    mel_script = os.path.join('D:/TZBJ_Check_v01/script/cleanUpScene.mel')
    pm.mel.eval("source \"{}\";".format(mel_script))
    logDate = datetimeinfo.dateTimeInfo()
    result = cmds.confirmDialog(
        title=u'清理确认',
        message=u'将进行以下内容的清理：\n「空集合」\n「空组」\n「空显示层」\n「Transform节点垃圾」\n「未使用的变形器」\n「未使用的笔刷」\n「未知节点」\n请确认是否要进行清理？\n如清理错误请【Ctrl+Z】进行撤销',
        button=[u'是', u'否'],
        defaultButton=u'是',
        cancelButton=u'否',
        dismissString=u'否')

    if result == u'是':
        # 未使用变形器
        mel.eval('deleteUnusedDeformers;')
        # 空组
        mel.eval('deleteEmptyGroups;')
        # 空集合
        mel.eval('deleteUnusedSets;')
        # 未使用笔刷
        mel.eval('deleteUnusedBrushes;')
        # 未知插件
        mel.eval('deleteUnknownNodes;')
        # 空显示层
        mel.eval('deleteEmptyLayers("Display");')

        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'文件清理已经完成，本次清理文件内容如下：\n「空集合」\n「空组」\n「空显示层」\n「Transform节点垃圾」\n「未使用的变形器」\n「未使用的笔刷」\n「未知节点」\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

    else:
        print(u'文件清理已经取消')
        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'文件清理已取消\n'
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
