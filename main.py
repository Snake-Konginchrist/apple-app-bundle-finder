#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apple应用信息查询工具 - 主程序入口
使用PySide6和Apple iTunes API查询应用信息
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """主函数 - 启动应用程序"""
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("Apple应用信息查询工具")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AppleAppBundleFinder")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序事件循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()