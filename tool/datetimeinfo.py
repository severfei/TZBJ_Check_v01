# ——*—— coding: utf-8 _*_


# get checkDateTime  获取检查文件时间
import maya.cmds as cmds

def dateTimeInfo(*args):
    output = ''
    inputDate = cmds.about(cd=True)
    inputTime = cmds.about(ct=True)
    output = '\n-----' + inputDate + '   ' + inputTime + '----------------------------\n'
    return output