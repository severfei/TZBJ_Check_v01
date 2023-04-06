# -*- coding: utf-8 -*-

import sys
sys.path.append('D:\TZBJ_Check_v01')

from tool import tool_window

if sys.version_info.major == 2:
    reload(tool_window)
else:
    import importlib
    importlib.reload(tool_window)

if __name__ == '__main__':
    tool_window.TZBJ_Checker().creatUI()
