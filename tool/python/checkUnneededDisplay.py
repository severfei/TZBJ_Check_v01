# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo

import maya.cmds as cmds
logDate = datetimeinfo.dateTimeInfo()

def checkunneededdisplaylayers(*args):
    unneeded_layers = []
    display_layers = cmds.ls(type='displayLayer')
    for displayLayer in display_layers:
        if displayLayer != 'defaultLayer':
            unneeded_layers.append(displayLayer)
    if len(unneeded_layers) == 0:
        fieldText = logDate + u'【文件displaylayers层】Check OK\n'
        cmds.button('displayersCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.button('displayerssetbtn', e=True, en=False)
        cmds.button('displayersClearbtn', e=True, en=False)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        def displayersselect(*args):
            cmds.select(set(unneeded_layers), ne=True)
            wrongPrint = '\n'.join(unneeded_layers)
            fieldText = logDate + u'******* Error *******\n【文件含有下列显示层】\n' + wrongPrint + u'\n请删除多余的显示层！\n'
            cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

        def deleteunneededdisplaylayers(*args):
            del_objs = []
            cmds.select(cl=True)
            display_layers = unneeded_layers
            if len(display_layers) > 0:
                try:
                    cmds.delete(display_layers)
                    del_objs.append(display_layers)
                except:
                    pass
            cmds.button('historysetbtn', e=True, en=False)
            cmds.button('historyClearbtn', e=True, en=False)
            checkunneededdisplaylayers()
            return del_objs

        # ui edit info-------------------------------------------------------------
        wrongPrint = '\n'.join(unneeded_layers)
        fieldText = logDate + u'******* Error *******\n【文件含有下列显示层】\n' + wrongPrint + u'\n请删除多余的显示层！\n'
        cmds.button('displayersCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('displayerssetbtn', e=True, en=True, c=displayersselect)
        cmds.button('displayersClearbtn', e=True, en=True, c=deleteunneededdisplaylayers)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    return unneeded_layers




def check_unneeded_lights():

    lights = cmds.ls(lights=True)
    return lights


def check_unneeded_cameras():
    """
    \xe4\xb8\x8d\xe8\xa6\x81\xe3\x81\xaa\xe3\x82\xab\xe3\x83\xa1\xe3\x83\xa9\xe3\x81\xae\xe3\x83\xaa\xe3\x82\xb9\xe3\x83\x88\xe3\x82\xa2\xe3\x83\x83\xe3\x83\x97\xe9\x96\xa2\xe6\x95\xb0
    """
    unneeded_cameras = []
    cameras = cmds.ls(cameras=True)
    for camera in cameras:
        if camera != 'frontShape' and camera != 'perspShape' and camera != 'sideShape' and camera != 'topShape':
            unneeded_cameras.append(camera)

    return unneeded_cameras




def cleanup_delete_unneeded_lights():
    """
    \xe4\xb8\x8d\xe8\xa6\x81\xe3\x81\xaa\xe3\x83\xa9\xe3\x82\xa4\xe3\x83\x88\xe3\x81\xae\xe5\x89\x8a\xe9\x99\xa4\xe9\x96\xa2\xe6\x95\xb0
    """
    del_objs = []
    cmds.select(cl=True)
    lights = check_unneeded_lights()
    for light in lights:
        objs = cmds.listRelatives(light, p=True, f=True)
        try:
            cmds.delete(objs)
        except:
            import traceback
            error_message = traceback.format_exc()
            cmds.confirmDialog(icn='information', t='Confirm', m='{0}: \u30a8\u30e9\u30fc\u3067\u51e6\u7406\u3067\u304d\u307e\u305b\u3093\u3067\u3057\u305f\u3002\n\n{1}'.format(light, error_message), button=['OK'])

        del_objs.append(objs[0])

    return del_objs


def cleanup_delete_unneeded_cameras():
    """
    \xe4\xb8\x8d\xe8\xa6\x81\xe3\x81\xaa\xe3\x82\xab\xe3\x83\xa1\xe3\x83\xa9\xe3\x81\xae\xe5\x89\x8a\xe9\x99\xa4\xe9\x96\xa2\xe6\x95\xb0
    """
    del_objs = []
    cmds.select(cl=True)
    cameras = check_unneeded_cameras()
    for camera in cameras:
        objs = cmds.listRelatives(camera, p=True, f=True)
        tmp = objs[0].split('|')
        try:
            cmds.delete(tmp[1])
            del_objs.append(tmp[1])
        except:
            import traceback
            error_message = traceback.format_exc()
            cmds.confirmDialog(icn='information', t='Confirm', m='{0}: \u30a8\u30e9\u30fc\u3067\u51e6\u7406\u3067\u304d\u307e\u305b\u3093\u3067\u3057\u305f\u3002\n\n{1}'.format(camera, error_message), button=['OK'])

    return del_objs