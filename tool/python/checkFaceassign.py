# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo

logDate = datetimeinfo.dateTimeInfo()

materials = cmds.ls(mat=True)

def checkfaceassign(*args):
    face_lists = []
    for mat in materials:
        cmds.hyperShade(objects=mat)
        assigns = cmds.ls(sl=True)
        for assign in assigns:
            if '.f' in assign:
                temp = assign.split('.')
                # print temp
                face_lists.append(temp[0])
        cmds.select(clear=True)

    if len(face_lists) == 0:
        fieldText = logDate + u'【选面给材质】 Check OK！\n'
        cmds.button('faceassignCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.button('faceassignsetbtn', e=True, en=False)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        def faceassignselectmodel(*args):
            objs = list(set(face_lists))
            cmds.select(objs, r=True)
        def faceassignselectface(*args):
            cmds.hyperShade(objects=mat)

        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'******* Error *******\n【包含选面给材质模型】，根据项目需求调整！\n'
        cmds.button('faceassignCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
        cmds.button('faceassignsetbtn', e=True, en=True,c=faceassignselectmodel)



# checkfaceassign()