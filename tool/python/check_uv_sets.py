# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo
from maya.OpenMaya import MSelectionList, MItSelectionList, MDagPath, MObject, MItMeshPolygon, MScriptUtil, MItDag

logDate = datetimeinfo.dateTimeInfo()
def check_process_all_uv(*args):
    out = []
    default_uv = 'map1'
    final_report = ''

    for geo in cmds.ls(type='mesh'):
        all_uv = list(set(cmds.polyUVSet(geo, q=True, auv=True)))
        curr_uv = cmds.polyUVSet(geo, q=True, cuv=True)
        custom_uv = [uv for uv in all_uv if uv.startswith('custom')]
        not_custom_uv = [uv for uv in all_uv if not uv.startswith('custom') and uv != default_uv]
        uv_amount = len(all_uv)
        cmds.select(cl=True)

        if len(all_uv) == 1 and all_uv[0] == 'map1':
            fieldText2 = logDate + '【{1}】 UVset Check OK'.format(all_uv[0], cmds.listRelatives(geo, p=True)[0])
            # cmds.button('UVsetCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
            cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText2, insertionPosition=0)

        if uv_amount > 1:  #检查UV集数量是否超过1个
            if default_uv not in all_uv:  #如果模型中不含有默认map1
                # ui edit info-------------------------------------------------------------
                fieldText = logDate + u'下列模型中没有名为【map1】的UV集:\n{}'.format(cmds.listRelatives(geo, p=True)[0])
                cmds.button('UVsetCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

            elif curr_uv in custom_uv and default_uv in all_uv and len(custom_uv) > 0:
                for uv in [ s for s in not_custom_uv if s != curr_uv or s != default_uv ]:
                    if uv in list(set(cmds.polyUVSet(geo, q=True, auv=True))):
                        if uv not in cmds.polyUVSet(geo, q=True, cuv=True) and uv != default_uv:
                            pass

                # print 'Info: Merged non-custom UVs and set uv to %s:' % curr_uv, geo
                # out.append('need to merge non-custom UVs:{}'.format(cmds.listRelatives(geo, p=True)[0]))
                fieldText = logDate + u'need to merge non-custom UVs:{}'.format(cmds.listRelatives(geo, p=True)[0])
                cmds.button('UVsetCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

            elif curr_uv in custom_uv and default_uv in all_uv:
                # print 'Info: Set current uv from %s to map1:' % curr_uv, geo
                # out.append('need to set current uv from {0} to map1:{1}'.format(curr_uv, cmds.listRelatives(geo, p=True)[0]))

                fieldText = logDate + u'need to set current uv from {0} to map1:{1}'.format(curr_uv, cmds.listRelatives(geo, p=True)[0])
                cmds.button('UVsetCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

            elif curr_uv == default_uv and len(not_custom_uv) > 0:
                for uv in not_custom_uv:
                    pass

                extra = ''
                if len(custom_uv) > 0:
                    extra = ' Did not touch %s.' % ','.join(custom_uv)
                # print 'Info: Deleted %s from %s.%s' % (','.join(not_custom_uv), geo, extra)
                # out.append('need to delete {0} from {1}.{2}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], extra))
                fieldText = logDate + u'请删除掉【{1}】中的 【{0}】'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], extra)
                cmds.button('UVsetCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

            elif curr_uv in not_custom_uv and default_uv in all_uv:
                for uv in not_custom_uv:
                    pass

                extra = ''
                if len(custom_uv) > 0:
                    extra = ' Did not touch %s.' % ','.join(custom_uv)
                # print 'Info: Deleted %s from %s. Current uv set to %s.%s' % (','.join(not_custom_uv),geo,default_uv,extra)
                # out.append('need to delete {0} from {1}. Current uv set to {2}.{3}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], default_uv, extra))
                fieldText = logDate + u'need to delete {0} from {1}. Current uv set to {2}.{3}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], default_uv, extra)
                cmds.button('UVsetCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
        elif uv_amount == 1:
            only_uv = all_uv[0]
            if only_uv != default_uv:
                # ui edit info-------------------------------------------------------------
                fieldText2 = logDate + '请将模型{1}的UV集 【{0}】 \n重命名为 【map1】'.format(only_uv, cmds.listRelatives(geo, p=True)[0])
                cmds.button('UVsetCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText2, insertionPosition=0)
                # out.append('need to rename {0} to map1:{1}'.format(only_uv, cmds.listRelatives(geo, p=True)[0]))


        final_uv = cmds.polyUVSet(geo, q=True, auv=True)
        # ui edit info-------------------------------------------------------------
        fieldText = '\n%s包含:\n%s\n%s个UV集' % (geo, final_uv, len(final_uv))
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

    if len(final_report) > 0:
        print(final_report)
    return out


def cleanup_process_all_uv(*args):
    out = []
    default_uv = 'map1'
    final_report = ''
    for geo in cmds.ls(type='mesh'):
        all_uv = list(set(cmds.polyUVSet(geo, q=True, auv=True)))
        curr_uv, = cmds.polyUVSet(geo, q=True, cuv=True)
        custom_uv = [ uv for uv in all_uv if uv.startswith('custom') ]
        not_custom_uv = [ uv for uv in all_uv if not uv.startswith('custom') and uv != default_uv ]
        uv_amount = len(all_uv)
        cmds.select(cl=True)
        if uv_amount > 1:
            if default_uv not in all_uv:
                print('Info: No map1 in all uv sets:', geo, all_uv)
                out.append('no map1 in all uv sets:{}'.format(cmds.listRelatives(geo, p=True)[0]))
            elif curr_uv in custom_uv and default_uv in all_uv and len(custom_uv) > 0:
                cmds.polyCopyUV(geo, uvs=default_uv)
                for uv in [ s for s in not_custom_uv if s != curr_uv or s != default_uv ]:
                    if uv in list(set(cmds.polyUVSet(geo, q=True, auv=True))):
                        if uv not in cmds.polyUVSet(geo, q=True, cuv=True) and uv != default_uv:
                            pass

                cmds.polyUVSet(geo, uvs=curr_uv, cuv=True)
                print('Info: Merged non-custom UVs and set uv to %s:' % curr_uv, geo)
                out.append('Merged non-custom UVs:{}'.format(cmds.listRelatives(geo, p=True)[0]))
            elif curr_uv in custom_uv and default_uv in all_uv:
                cmds.polyUVSet(geo, uvs=default_uv, cuv=True)
                print('Info: Set current uv from %s to map1:' % curr_uv, geo)
                out.append('Set current uv from {0} to map1:{1}'.format(curr_uv, cmds.listRelatives(geo, p=True)[0]))
            elif curr_uv == default_uv and len(not_custom_uv) > 0:
                for uv in not_custom_uv:
                    cmds.polyUVSet(geo, uvs=uv, d=True)

                extra = ''
                if len(custom_uv) > 0:
                    extra = ' Did not touch %s.' % ','.join(custom_uv)
                print('Info: Deleted %s from %s.%s' % (','.join(not_custom_uv), geo, extra))
                out.append('Deleted {0} from {1}.{2}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], extra))
            elif curr_uv in not_custom_uv and default_uv in all_uv:
                cmds.polyUVSet(geo, uvs=default_uv, cuv=True)
                for uv in not_custom_uv:
                    cmds.polyUVSet(geo, uvs=uv, d=True)

                extra = ''
                if len(custom_uv) > 0:
                    extra = ' Did not touch %s.' % ','.join(custom_uv)
                print('Info: Deleted %s from %s. Current uv set to %s.%s' % (','.join(not_custom_uv),
                 geo,
                 default_uv,
                 extra))
                out.append('Deleted {0} from {1}. Current uv set to {2}.{3}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], default_uv, extra))
        if uv_amount == 1:
            only_uv = all_uv[0]
            if only_uv != default_uv:
                print('Info: Renamed %s to map1:' % only_uv, geo)
                cmds.polyUVSet(geo, rename=True, newUVSet=default_uv)
                out.append('Renamed {0} to map1:{1}'.format(only_uv, cmds.listRelatives(geo, p=True)[0]))
        final_uv = cmds.polyUVSet(geo, q=True, auv=True)
        final_report = final_report + '\nFinal Report: %s = %s %s uv sets' % (geo, final_uv, len(final_uv))

    if len(final_report) > 0:
        print(final_report)
    return out

def check_zero_uv(*args):
    out = []
    for obj in cmds.ls(type='mesh'):
        selection = MSelectionList()
        selection.add(obj)
        iterSelection = MItSelectionList(selection)
        dag = MDagPath()
        mObject = MObject()
        iterSelection.getDagPath(dag, mObject)
        polyIter = MItMeshPolygon(dag)
        areaValue = MScriptUtil()
        areaValue.createFromDouble(0.0)
        areaPointer = areaValue.asDoublePtr()
        uvArea = 0
        while not polyIter.isDone():
            polyIter.getUVArea(areaPointer)
            area = MScriptUtil(areaPointer).asDouble()
            uvArea += area
            next(polyIter)

        if uvArea == 0.0:
            out.append(cmds.listRelatives(obj, p=True)[0])

    return out


def cleanup_zero_uv(*args):
    out = []
    no_uv = check_zero_uv()
    for geo in no_uv:
        cmds.polyAutoProjection('%s.f[*]' % geo, lm=0, ibd=True, cm=False, l=2, sc=1, o=1, ps=0.2)
        cmds.delete(geo, ch=True)
        print('Fixed zero UV area and applied default UV:', geo)
        out.append(cmds.listRelatives(geo, p=True)[0])

    return out