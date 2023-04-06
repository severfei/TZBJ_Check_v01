# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.OpenMaya as om
from tool import datetimeinfo

# 检查模型是否有带洞的面
def checkHoleFace(*args):
    logDate = datetimeinfo.dateTimeInfo()
    # 获取所有的mesh节点
    dag_iterator = om.MItDag(om.MItDag.kDepthFirst, om.MFn.kMesh)
    # 创建选择列表，将所有破损边缘加入选择列表
    selection_list = om.MSelectionList()

    # 在每次执行函数之前清空选择列表
    selection_list.clear()

    while not dag_iterator.isDone():
        # 获取当前节点的MObject和MFnMesh对象
        current_item = dag_iterator.currentItem()
        current_mesh = om.MFnMesh(current_item)

        # 获取当前mesh的所有边缘
        edge_iterator = om.MItMeshEdge(current_item)

        while not edge_iterator.isDone():
            # 获取当前边缘所连接的两个面
            face_indices = om.MIntArray()
            edge_iterator.getConnectedFaces(face_indices)

            # 如果只有一个面，则说明这是边缘
            if face_indices.length() == 1:
                mesh_name = current_mesh.name()
                edge_index = edge_iterator.index()
                # 将破损边缘加入选择列表中
                selection_list.add('{0}.e[{1}]'.format(mesh_name, edge_index))
            edge_iterator.next()
        dag_iterator.next()

    # 如果选择列表不为空，则选中所有的破损边缘
    if not selection_list.isEmpty():
        def selectionHoleFace(*args):
            om.MGlobal.setActiveSelectionList(selection_list)
        fieldText = logDate + u'******* Error *******\n【模型有破损带洞面】\n【请根据具体项目要求进行处理！】\n'
        cmds.button('holesFaceCheckButton', e=True, bgc=[0.9, 0.4, 0.5])
        cmds.button('holesFacesetbtn', e=True, en=True, c=selectionHoleFace)
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)

    else:
        print('未发现破损边缘')
        fieldText = logDate + u'【模型破损带洞面】Check OK\n'
        cmds.button('holesFaceCheckButton', e=True, bgc=[0.5, 0.8, 0.7])
        cmds.scrollField('errorComentPrintField', e=True, insertText=fieldText, insertionPosition=0)


