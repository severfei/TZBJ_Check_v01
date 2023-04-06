# ——*—— coding: utf-8 _*_
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
from tool import datetimeinfo
logDate = datetimeinfo.dateTimeInfo()


# check UVSet onlyOne  检查模型UV集是否唯一
def checkUVSetonlyOne(*args):
    logDate = datetimeinfo.dateTimeInfo()
    allMesh = cmds.ls(type='mesh')
    alluvset = list(set(cmds.polyUVSet(allMesh, query=True, allUVSets=True)))
    cmds.select(clear=True)

    if len(alluvset) == 1 and alluvset[0] == 'map1':
        print ('model UVset OK')
        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'【模型UV集】Check OK\n'
        cmds.button('checkUVSetonlyOneButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
    else:
        # ui edit info-------------------------------------------------------------
        fieldText = logDate + u'模型含有多个UV集\n或UV集名称不是[map1]\n'
        cmds.button('checkUVSetonlyOneButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('UVSetonlyOneClearbtn',e=True,en=True,c=cleanup_all_uvsets)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

        out = []
        default_uv = 'map1'
        for geo in allMesh:
            all_uv = list(set(cmds.polyUVSet(geo, q=True, auv=True)))
            curr_uv = cmds.polyUVSet(geo, q=True, cuv=True)
            custom_uv = [uv for uv in all_uv if uv.startswith('custom')]
            not_custom_uv = [uv for uv in all_uv if not uv.startswith('custom') and uv != default_uv]
            uv_amount = len(all_uv)
            cmds.select(cl=True)

            if uv_amount > 1:  # 检查UV集数量是否超过1个
                # out.append(geo)
                final_uv = cmds.polyUVSet(geo, q=True, auv=True)
                # ui edit info-------------------------------------------------------------
                fieldText =logDate + '\n【%s】包含:\n%s\n%s个UV集' % (geo, final_uv, len(final_uv))
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

                if default_uv not in all_uv:  # 如果模型中不含有默认map1
                    print ('nononononoone')
                    # ui edit info-------------------------------------------------------------
                    fieldText2 = logDate + '下列模型中没有名为【map1】的UV集:\n\n{}'.format(cmds.listRelatives(geo, p=True)[0])
                    cmds.button('UVsetCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText2, insertionPosition=0)

                if curr_uv == default_uv and len(not_custom_uv) > 0:
                    print((222222222))
                    for uv in not_custom_uv:
                        pass
                    extra = ''
                    if len(custom_uv) > 0:
                        extra = ' Did not touch %s.' % ','.join(custom_uv)
                    # print 'Info: Deleted %s from %s.%s' % (','.join(not_custom_uv), geo, extra)
                    # out.append('need to delete {0} from {1}.{2}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], extra))
                    fieldText3 = logDate + '请删除掉【{1}】中的 【{0}】'.format(','.join(not_custom_uv),
                                                                      cmds.listRelatives(geo, p=True)[0], extra)
                    cmds.button('UVsetCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                    cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText3, insertionPosition=0)

                elif uv_amount == 1:
                    print((333333333))
                    only_uv = all_uv[0]
                    if only_uv != default_uv:
                        # ui edit info-------------------------------------------------------------
                        fieldText4 = logDate + '请将模型{1}的UV集 【{0}】 \n重命名为 【map1】'.format(only_uv,
                                                                                         cmds.listRelatives(geo,
                                                                                                            p=True)[0])
                        cmds.button('UVsetCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
                        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText4, insertionPosition=0)
                        # out.append('need to rename {0} to map1:{1}'.format(only_uv, cmds.listRelatives(geo, p=True)[0]))





        return out

        # print (u'!!这个模型含有UVset错误')

def cleanup_all_uvsets(*args):
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
                fieldText = logDate + u'下列模型含有多个UV集且\n没有名为 map1 的UV集\n请手动重命名为 map1 后重新执行清理\n{}'.format(cmds.listRelatives(geo, p=True)[0])
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

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
                fieldText = logDate + u'已将模型【{1}】的UV集\n{0}删除\n并将UV集设置为：{2}.{3}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], default_uv, extra)
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
                # out.append('Deleted {0} from {1}.{2}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], extra))
            elif curr_uv in not_custom_uv and default_uv in all_uv:
                cmds.polyUVSet(geo, uvs=default_uv, cuv=True)
                for uv in not_custom_uv:
                    cmds.polyUVSet(geo, uvs=uv, d=True)

                extra = ''
                if len(custom_uv) > 0:
                    extra = ' Did not touch %s.' % ','.join(custom_uv)
                fieldText = logDate + u'Deleted {0} from {1}. Current uv set to {2}.{3}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], default_uv, extra)
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
                # out.append('Deleted {0} from {1}. Current uv set to {2}.{3}'.format(','.join(not_custom_uv), cmds.listRelatives(geo, p=True)[0], default_uv, extra))
        if uv_amount == 1:
            only_uv = all_uv[0]
            if only_uv != default_uv:
                print('Info: Renamed %s to map1:' % only_uv, geo)
                cmds.polyUVSet(geo, rename=True, newUVSet=default_uv)
                fieldText = logDate + u'已将模型【{1}】的uv集\n由{0} 修改为 map1'.format(only_uv, cmds.listRelatives(geo, p=True)[0])
                cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)
                # out.append('Renamed {0} to map1:{1}'.format(only_uv, cmds.listRelatives(geo, p=True)[0]))
        final_uv = cmds.polyUVSet(geo, q=True, auv=True)
        final_report = final_report + '\nFinal Report: %s = %s %s uv sets' % (geo, final_uv, len(final_uv))
    cmds.button('UVSetonlyOneClearbtn',e=True,en=False)
    checkUVSetonlyOne()


    return out





