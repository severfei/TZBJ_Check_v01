# ——*—— coding: utf-8 _*_
import maya.cmds as cmds



# 顶部窗口命令
def commonMenu():
    editMenu = cmds.menu(label=u'编辑')  # 创建一个顶部菜单按钮
    editMenuSave = cmds.menuItem(label=u'保存设置',  # 创建一个隶属于编辑的菜单项，标题为label
                                      command=editMenuSaveCmd,
                                      )
    editMenuReset = cmds.menuItem(label=u'重置设置',  # 创建一个隶属于编辑的菜单项，标题为label
                                       command=editMenuResetCmd,
                                       )
    editMenuDiv = cmds.menuItem(d=True, dl='test')  # 创建分割线菜单项,向分割线菜单项添加标签
    editMenuRadio = cmds.radioMenuItemCollection()
    editMenuTool = cmds.menuItem(
        label='TZBJ_CheckTool',  # 创建单选按钮标题
        radioButton=True,  # 创建单选按钮菜单
        enable=True,  # 菜单的启用状态（简写是en，因为类里边定义了状态，这里可以直接调用）
        command=editMenuToolCmd,
    )

    editMenuAction = cmds.menuItem(
        label='TZBJ_Action',  # 创建单选按钮标题
        radioButton=True,  # 创建单选按钮菜单
        enable=True,  # 菜单的启用状态（简写是en，因为类里边定义了状态，这里可以直接调用）
        command=editMenuSActionCmd,
    )
    helpMenu = cmds.menu(label='help')  # 创建一个新的顶部菜单按钮
    helpMenuItem = cmds.menuItem(  # 创建一个隶属于help的菜单项
        label='Help on %s' % 'tzbj',
        command=helpMenuCmd  # 创建command标签，可以指定该控件使用时发生的操作
    )
# 顶部窗口按钮功能
def commonButtons():
    pass
# 顶部窗口help按钮功能
def helpMenuCmd():
    cmds.launch(web = 'http://www.baidu.com')       #创建访问的具体指向，launch启动相应的应用程序以打开文档、网页或目录 指定
def editMenuSaveCmd():
    pass
def editMenuResetCmd():
    pass
def editMenuToolCmd():
    pass
def editMenuSActionCmd():
    pass
# 日志清除按钮功能
def logClear():
    pass