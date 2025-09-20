#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口界面模块
实现应用的主要用户界面
"""

import webbrowser
import platform

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QSplitter, QMessageBox
)

from ui.font_config import FontConfig

from api.itunes_api import iTunesAPI
from models.app_info import AppInfo
from ui.details_panel_widget import DetailsPanelWidget
from ui.info_panel_widget import InfoPanelWidget
from ui.search_widget import SearchWidget
from utils.helpers import is_valid_app_id


class SearchWorker(QThread):
    """搜索工作线程"""
    
    # 信号定义
    search_finished = Signal(object)  # AppInfo对象或None
    search_error = Signal(str)  # 错误信息
    
    def __init__(self, app_id: str, country: str):
        super().__init__()
        self.app_id = app_id
        self.country = country
        self.api = iTunesAPI()
    
    def run(self):
        """执行搜索"""
        try:
            app_info = self.api.lookup_by_id(self.app_id, self.country)
            self.search_finished.emit(app_info)
        except Exception as e:
            self.search_error.emit(str(e))


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.current_app_info = None
        self.search_worker = None
        
        # 设置统一的字体配置
        FontConfig.setup_application_fonts()
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Apple应用信息查询工具")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # 设置应用图标（根据操作系统选择合适格式）
        system = platform.system()
        if system == "Darwin":  # macOS
            icon_path = "assets/logo.icns"
        elif system == "Windows":  # Windows
            icon_path = "assets/logo.ico"
        else:  # Linux 或其他系统
            icon_path = "assets/logo.png"
        
        self.setWindowIcon(QIcon(icon_path))
        
        # 设置状态栏样式（移除窗口背景色）
        self.setStyleSheet("""
            QStatusBar {
                background-color: #ffffff;
                color: #2c3e50;
                border-top: 1px solid #e0e0e0;
                font-size: 13px;
                padding: 5px;
            }
        """)
        
        # 创建中央部件（移除背景色）
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # 创建搜索区域
        self.search_widget = SearchWidget()
        main_layout.addWidget(self.search_widget)
        
        # 创建分割器 - 现代化样式
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e0e0e0;
                border-radius: 2px;
            }
            QSplitter::handle:horizontal {
                width: 4px;
                margin: 0 8px;
            }
        """)
        main_layout.addWidget(splitter)
        
        # 创建左侧信息面板
        self.info_widget = InfoPanelWidget()
        splitter.addWidget(self.info_widget)
        
        # 创建右侧详细信息面板
        self.details_widget = DetailsPanelWidget()
        splitter.addWidget(self.details_widget)
        
        # 设置分割器比例
        splitter.setSizes([550, 550])
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")
    
    def setup_connections(self):
        """设置信号连接"""
        # 搜索相关信号
        self.search_widget.search_button.clicked.connect(self.search_app)
        self.search_widget.app_id_input.returnPressed.connect(self.search_app)
        
        # 操作按钮信号
        self.info_widget.get_view_button().clicked.connect(self.view_in_app_store)
        self.info_widget.get_copy_button().clicked.connect(self.copy_app_info)
    
    def search_app(self):
        """搜索应用"""
        app_id = self.search_widget.get_app_id()
        
        if not app_id:
            QMessageBox.warning(self, "警告", "请输入应用ID或Bundle ID")
            return
        
        if not is_valid_app_id(app_id):
            QMessageBox.warning(self, "警告", "请输入有效的应用ID或Bundle ID")
            return
        
        # 获取选择的国家代码
        country_text = self.search_widget.country_combo.currentText()
        country = country_text.split(" - ")[0]
        
        # 开始搜索
        self.start_search(app_id, country)
    
    def start_search(self, app_id: str, country: str):
        """开始搜索"""
        # 禁用搜索按钮，显示进度条
        self.search_widget.set_search_enabled(False)
        self.search_widget.show_progress(True)
        self.statusBar().showMessage(f"正在查询应用信息...")
        
        # 创建并启动工作线程
        self.search_worker = SearchWorker(app_id, country)
        self.search_worker.search_finished.connect(self.on_search_finished)
        self.search_worker.search_error.connect(self.on_search_error)
        self.search_worker.start()
    
    def on_search_finished(self, app_info: AppInfo):
        """搜索完成处理"""
        self.search_widget.set_search_enabled(True)
        self.search_widget.show_progress(False)
        
        if app_info:
            self.current_app_info = app_info
            self.info_widget.display_app_info(app_info)
            self.details_widget.display_app_info(app_info)
            self.details_widget.display_detailed_info(app_info)
            self.statusBar().showMessage("查询完成")
        else:
            QMessageBox.information(self, "提示", "未找到相关应用信息")
            self.statusBar().showMessage("未找到应用")
    
    def on_search_error(self, error_message: str):
        """搜索错误处理"""
        self.search_widget.set_search_enabled(True)
        self.search_widget.show_progress(False)
        QMessageBox.critical(self, "错误", f"查询失败：{error_message}")
        self.statusBar().showMessage("查询失败")

    def view_in_app_store(self):
        """在App Store中查看"""
        if self.current_app_info and self.current_app_info.track_view_url:
            webbrowser.open(self.current_app_info.track_view_url)
    
    def copy_app_info(self):
        """复制应用信息到剪贴板"""
        if self.info_widget.copy_app_info():
            self.statusBar().showMessage("应用信息已复制到剪贴板", 3000)