# -*- coding: utf-8 -*-

import imp
import sys
import maya.cmds as cmds

TZBJ_path = 'D:/TZBJ_Check_v01'
if TZBJ_path not in sys.path:
    sys.path.append(TZBJ_path)

from tool import datetimeinfo
logDate = datetimeinfo.dateTimeInfo()

from tool.python.menu import *
from tool.python import checkMaterialNaming
from tool.python import checkLaminaFaces
from tool.python import checkNsideFaces
from tool.python import checkMeshHistory
from tool.python import checkHoleFace
from tool.python import checkVertexNormalLock
from tool.python import checkNonParallelPlane
from tool.python import checkNonVariousVertices
from tool.python import checkUVSetonlyOne
from tool.python import checkNonVariousEdges
from tool.python import check_uv_sets
from tool.python import checkFaceassign
from tool.python import checkUnknownPlugin
from tool.python import checkUnneededDisplay
from tool.python import checkVirus
from tool.python import checkDuplicateOBJ
from tool.python import checkUVOut


from tool.plugin import UVpass
from tool.plugin import RemoveAllNamespaces
from tool.plugin import ig_EzRenamewindow
from tool.plugin import modeldonotshow
from tool.plugin import AriPolygonCounterwindow
from tool.plugin import AriSymmetryCheckerwindow
from tool.plugin import AriStraightVertexwindow
from tool.plugin import DoraSkinWeightImpExpwindow
from tool.plugin import CleanUp
from tool.plugin import SameNameJointSkinning


imp.reload(datetimeinfo)
imp.reload(checkMaterialNaming)
imp.reload(checkLaminaFaces)
imp.reload(checkNsideFaces)
imp.reload(checkMeshHistory)
imp.reload(checkHoleFace)
imp.reload(checkVertexNormalLock)
imp.reload(checkNonParallelPlane)
imp.reload(checkNonVariousVertices)
imp.reload(checkUVSetonlyOne)
imp.reload(checkNonVariousEdges)
imp.reload(check_uv_sets)
imp.reload(checkFaceassign)
imp.reload(checkUnknownPlugin)
imp.reload(checkUnneededDisplay)
imp.reload(checkVirus)
imp.reload(checkDuplicateOBJ)
imp.reload(CleanUp)
imp.reload(checkUVOut)

imp.reload(UVpass)
imp.reload(RemoveAllNamespaces)
imp.reload(ig_EzRenamewindow)
imp.reload(modeldonotshow)
imp.reload(AriPolygonCounterwindow)
imp.reload(AriSymmetryCheckerwindow)
imp.reload(AriStraightVertexwindow)
imp.reload(DoraSkinWeightImpExpwindow)
imp.reload(SameNameJointSkinning)





class TZBJ_Checker(object):
    #--------------------------------------UI区----------------------------------------
    # UI 按键
    def __init__(self):
        self.window = 'TZBJ_Check'
        self.size = (600,800)

    def creatUI(self):
        if cmds.window(self.window, exists=True):  # 如果窗口存在则删除窗口并运行自定义窗口重新打开
            cmds.deleteUI(self.window, window=True)
        self.window = cmds.window(
            self.window,
            widthHeight = self.size,
            title ='TZBJ_Check',
            menuBar = True
        )
        commonMenu()
        self.tab1Layout()
        self.fenqu_model()
        self.fenqu_plugin()
        self.errorTab()
        self.tab2Layout()
        # self.fenqu_UV()
        # self.fenqu2_1()
        self.tab3Layout()
        # self.jindutiao()
        cmds.showWindow()

    def tab1Layout(self):
        self.tab1 = cmds.tabLayout('checkTab')
        # 创建一总框架
        self.mainLayout = cmds.paneLayout(u'常用功能', p=self.tab1, configuration="horizontal3", w=300, h=200)
        self.main2Layout = cmds.paneLayout('layout', p=self.mainLayout, configuration="vertical3")
        # 创建一个列布局
        self.scendLayout = cmds.columnLayout(
            p=self.main2Layout,
            w=300, h=200,
            rs=2
        )

    #  ---------------------------------------------日志相关------------------------------------------
    # error log clear  错误日志清除
    def logClear(self, *args):
        cmds.scrollField('errorComentPrintField', e=True, clear=True)

    # 创建日志分区
    def errorTab(self):
        self.errorComemtTab = cmds.tabLayout('errorComemtTab', parent=self.main2Layout, )
        self.errorList = cmds.paneLayout(u'日志', p=self.errorComemtTab, configuration="horizontal2")
        cmds.scrollField('errorComentPrintField', ed=False, p=self.errorList, h=600, w=270)
        # cmds.button('exportComentButton', p=u'日志', l='coment export csv')
        cmds.button('clearLogButton', p=self.errorList, l=u'清空日志', c=self.logClear)

    # 创建竖向第一个分区
    def fenqu_model(self):
        # 创建第一个分区
        self.cla1 = cmds.frameLayout(l=u'模型检查区', p=self.scendLayout, cll=True,lw=300)

        # 创建横向3个选项的功能
        self.rowmaniLayout = cmds.rowColumnLayout(
            p=self.cla1, nc=3, cw=[(1, 200), (2, 100),(3,1)],
            columnOffset=[(1, 'both', 5), (2, 'both', 5),(3, 'both', 5) ],
            rat=[(1, 'top', 5)]
            )
        self.checkAllbtn = cmds.button(l=u'检查全部', p=self.rowmaniLayout, bgc=[0, 1, 0],c=self.modelallCheck)
        cmds.button(l=u'重置', p=self.rowmaniLayout, bgc=[0, 1, 0],c=self.modelallCheckClear)
        cmds.button(l=u'重置2', vis=False,p=self.rowmaniLayout, bgc=[0, 1, 0])

        self.rowLayout = cmds.rowColumnLayout(
            p=self.rowmaniLayout,
            nc=3,
            w=600,
            columnOffset=[(1, 'both', 5), (2, 'both', 5),(3, 'both', 5) ],
            cw=[(1, 195), (2, 45),(3,45) ],
            rat=[(1, 'top', 10),]
        )

        cmds.button('meshHistoryCheckButton', p=self.rowLayout, l=u'检查模型是否存在历史',
                    c=checkMeshHistory.checkMeshHistory)
        cmds.button('historysetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('historyClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('vertexNormalLockCheckButton', p=self.rowLayout, l=u'检查法线是否锁定',
                    c=checkVertexNormalLock.checkVertexNormalLock)
        cmds.button('vertexNormalLocksetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('vertexNormalLockClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('nSideFacesCheckButton', p=self.rowLayout, l=u'检查是否存在五边面',
                    c=checkNsideFaces.checkNsideFaces)
        cmds.button('nSideFacessetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('nSideFacesClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('holesFaceCheckButton', p=self.rowLayout, l=u'检查是否存在破损带洞面',
                    c=checkHoleFace.checkHoleFace)
        cmds.button('holesFacesetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('holesFaceClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('laminaFacesCheckButton', p=self.rowLayout, l=u'检查是否存在错误重叠面',
                    c=checkLaminaFaces.checkLaminaFaces)
        cmds.button('laminaFacessetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('laminaFacesClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('DuplicateOBJCheckButton', p=self.rowLayout, l=u'检查是否存在错误重叠模型',
                    c=checkDuplicateOBJ.checkDuplicateOBJ)
        cmds.button('DuplicateOBJsetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('DuplicateOBJClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('nonVariousVerticesCheckButton', p=self.rowLayout, l=u'检查是否存在非多样性顶点',
                    c=checkNonVariousVertices.checkNonVariousVertices)
        cmds.button('nonVariousVerticessetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('nonVariousVerticesClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('nonVariousEdgesCheckButton', p=self.rowLayout, l=u'检查是否存在非多样性线',
                    c=checkNonVariousEdges.checkNonVariousEdges)
        cmds.button('nonVariousEdgessetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('nonVariousEdgesClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('materialCheckButton', p=self.rowLayout, l=u'检查材质球名是否正确',
                    c=checkMaterialNaming.checkMaterialNaming)
        cmds.button('materialsetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('materialClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('faceassignCheckButton', p=self.rowLayout, l=u'检查是否选面给材质',
                    c=checkFaceassign.checkfaceassign)
        cmds.button('faceassignsetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('faceassignClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('UVCheckButton', p=self.rowLayout, l=u'检查UV是否超出第一象限',
                    c=checkUVOut.checkUVOut)
        cmds.button('UVsetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('UVClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('checkUVSetonlyOneButton', p=self.rowLayout, l=u'检查UV集是否唯一＆且为map1',
                    c=checkUVSetonlyOne.checkUVSetonlyOne)
        cmds.button('UVSetonlyOnesetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('UVSetonlyOneClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('displayersCheckButton', p=self.rowLayout, l=u'检查是否存在显示层',
                    c=checkUnneededDisplay.checkunneededdisplaylayers)
        cmds.button('displayerssetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('displayersClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('pluginnodesCheckButton', p=self.rowLayout, l=u'检查是否存在未知插件＆节点',
                    c=checkUnknownPlugin.checkUnknownPlugin)
        cmds.button('pluginnodessetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('pluginnodesClearbtn', l=u'清理', p=self.rowLayout, en=False)

        cmds.button('virusCheckButton', p=self.rowLayout, l=u'检查文件是否感染病毒',
                    c=checkVirus.checkantivirus)
        cmds.button('virussetbtn', l=u'选择', p=self.rowLayout, en=False)
        cmds.button('virusClearbtn', l=u'清理', p=self.rowLayout, en=False)



    #--------------------------------------模型检查全部与重置---------------------------------------
    #检查全部选项
    def modelallCheck(self, *args):
        try:
            # 清除缓存
            cmds.flushUndo()
            checkMeshHistory.checkMeshHistory()
            checkVertexNormalLock.checkVertexNormalLock()
            checkNsideFaces.checkNsideFaces()
            checkHoleFace.checkHoleFace()
            checkLaminaFaces.checkLaminaFaces()
            checkDuplicateOBJ.checkDuplicateOBJ()
            checkNonVariousVertices.checkNonVariousVertices()
            checkNonVariousEdges.checkNonVariousEdges()
            checkMaterialNaming.checkMaterialNaming()
            checkFaceassign.checkfaceassign()
            checkUVSetonlyOne.checkUVSetonlyOne()
            checkUVOut.checkUVOut()
            checkUnneededDisplay.checkunneededdisplaylayers()
            checkUnknownPlugin.checkUnknownPlugin()
            checkVirus.checkantivirus()

        except:
            fieldText = logDate + u'文件中没有模型存在!请打开正确的文件\n'
            cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)


    # check button clear 清除检查按钮
    def modelallCheckClear(self, *args):
        cmds.button('meshHistoryCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('historysetbtn', e=True, en=False)
        cmds.button('historyClearbtn', e=True, en=False)

        cmds.button('vertexNormalLockCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('vertexNormalLocksetbtn', e=True, en=False)
        cmds.button('vertexNormalLockClearbtn', e=True, en=False)

        cmds.button('nSideFacesCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('nSideFacessetbtn', e=True, en=False)
        cmds.button('nSideFacesClearbtn', e=True, en=False)

        cmds.button('holesFaceCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('holesFacesetbtn', e=True, en=False)
        cmds.button('holesFaceClearbtn', e=True, en=False)

        cmds.button('nonVariousVerticesCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('nonVariousVerticessetbtn', e=True, en=False)
        cmds.button('nonVariousVerticesClearbtn', e=True, en=False)

        cmds.button('nonVariousEdgesCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('nonVariousEdgessetbtn', e=True, en=False)
        cmds.button('nonVariousEdgesClearbtn',e=True, en=False)

        cmds.button('UVCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('UVsetbtn', e=True, en=False)
        cmds.button('UVClearbtn', e=True, en=False)

        cmds.button('checkUVSetonlyOneButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('UVSetonlyOnesetbtn', e=True, en=False)
        cmds.button('UVSetonlyOneClearbtn', e=True, en=False)

        cmds.button('materialCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('materialsetbtn', e=True, en=False)
        cmds.button('materialClearbtn',e=True, en=False)

        cmds.button('laminaFacesCheckButton',e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('laminaFacessetbtn',e=True, en=False)
        cmds.button('laminaFacesClearbtn',e=True, en=False)

        cmds.button('faceassignCheckButton',e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('faceassignsetbtn',e=True, en=False)
        cmds.button('faceassignClearbtn',e=True, en=False)

        cmds.button('pluginnodesCheckButton',e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('pluginnodessetbtn',e=True, en=False)
        cmds.button('pluginnodesClearbtn',e=True, en=False)

        cmds.button('displayersCheckButton',e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('displayerssetbtn',e=True, en=False)
        cmds.button('displayersClearbtn',e=True, en=False)

        cmds.button('virusCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('virussetbtn', e=True, en=False)
        cmds.button('virusClearbtn', e=True, en=False)

        cmds.button('DuplicateOBJCheckButton', e=True, bgc=[0.36, 0.36, 0.36])
        cmds.button('DuplicateOBJsetbtn', e=True, en=False)
        cmds.button('DuplicateOBJClearbtn', e=True, en=False)

        self.logClear()



    # 创建竖向第二个分区
    def fenqu_UV(self):
        rowmainUVLayout = cmds.frameLayout('framUVlayout', l=u'UV检查区', p=self.scendLayout, cll=True,lw=300)
        rowmainUVscLayout = cmds.rowColumnLayout(
            p=rowmainUVLayout, nc=3, cw=[(1, 200), (2, 100), (3, 1)],
            columnOffset=[(1, 'both', 5), (2, 'both', 5), (3, 'both', 5)],
            rat=[(1, 'top', 5)]
        )
        checkAllUVbtn = cmds.button(l=u'检查全部', p=rowmainUVscLayout, bgc=[0, 1, 0], c=self.modelallCheck)
        cmds.button(l=u'重置', p=rowmainUVscLayout, bgc=[0, 1, 0], c=self.modelallCheckClear)
        cmds.button(l=u'重置2', vis=False, p=rowmainUVscLayout, bgc=[0, 1, 0])

        rowUVLayout = cmds.rowColumnLayout(
            p=rowmainUVLayout,
            nc=3,
            w=600,
            columnOffset=[(1, 'both', 5), (2, 'both', 5), (3, 'both', 5)],
            cw=[(1, 195), (2, 45), (3, 45)],
            rat=[(1, 'top', 5), ]
        )
        cmds.button(p=rowUVLayout)
        cmds.button(p=rowUVLayout)
        cmds.button(p=rowUVLayout)



    def fenqu_plugin(self):
        # 创建第二个分区
        self.cla2 = cmds.frameLayout('fram2layout', l=u'常用插件', p=self.scendLayout, cll=True)
        # 创建横向3个选项的功能
        self.row2maniLayout = cmds.rowColumnLayout(
            'rowlayout',
            p='fram2layout',
            nc=2,cw=[(1, 150), (2, 150)],
            columnOffset=[(1, 'both', 10), (2, 'both', 10)],
            rat=[1, 'top', 10]
        )
        cmds.button(l=u'一键文件垃圾清理', bgc=[0, 0.8, 1],c=CleanUp.CleanUp)
        cmds.button(l=u'AriStraightVertex', bgc=[0, 0.8, 1],c=AriStraightVertexwindow.AriStraightVertexwindow)
        cmds.button(l=u'一键UV传递', bgc=[0, 0.8, 1],c=UVpass.UVpass)
        cmds.button(l=u'AriPolygonCounter', bgc=[0, 0.8, 1],c=AriPolygonCounterwindow.AriPolygonCounterwindow)
        cmds.button(l=u'一键去除空间名', bgc=[0, 0.8, 1],c=RemoveAllNamespaces.RemoveAllNamespaces)
        cmds.button(l=u'模型对称检查插件', bgc=[0, 0.8, 1],c=AriSymmetryCheckerwindow.AriSymmetryCheckerwindow)
        cmds.button(l=u'一键修复模型不显示', bgc=[0, 0.8, 1],c=modeldonotshow.modeldonotshow)
        cmds.button(l=u'ig_Ez重命名插件', bgc=[0, 0.8, 1],c=ig_EzRenamewindow.ig_EzRenamewindow)
        cmds.button(l=u'DoraSkin权重插件', bgc=[0, 0.8, 1],c=DoraSkinWeightImpExpwindow.DoraSkinWeightImpExpwindow)
        cmds.button(l=u'SameName蒙皮插件', bgc=[0, 0.8, 1],c=SameNameJointSkinning.SameNameJointWindow)


    # 创建进度条
    def jindutiao(self):
        jindutiaolayout = cmds.formLayout(
            p=self.scendLayout,
        )
        progressControl = cmds.progressBar(maxValue=10, width=300,p=jindutiaolayout)
#  ----------------------------------------------第一竖向分区结束------------------------------------------

    #创建第二个tab
    def tab2Layout(self):
        self.tab2Layout = cmds.columnLayout(u'工具箱',p=self.tab1)
        self.fenqu2mainLayout = cmds.paneLayout(p=self.tab2Layout, configuration="horizontal3", w=300, h=200,)
        self.fenqu2main2Layout = cmds.paneLayout( p=self.fenqu2mainLayout, configuration="vertical3")
    # def fenqu2_1(self):
    #     self.cla2 = cmds.frameLayout(l='常用工具',p=self.fenqu2main2Layout,mh=10, cll=True,bgc=[0, 0.5, 0.5])
    #     cmds.button(l='MEL转Python插件',p=self.cla2,c=ezMel2Python.ezMel2Python)
    #     cmds.button(l='pycharm与maya互通',p=self.cla2,c=pycharmtomaya.pycharmtomaya)
    #     cmds.button(l='test')

    #创建第三个tab
    def tab3Layout(self):
        self.tab3Layout = cmds.columnLayout(u'设置',p=self.tab1,w=200, h=200)


# TZBJ_Checker().creatUI()








