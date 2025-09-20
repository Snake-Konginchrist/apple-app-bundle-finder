"""
搜索区域组件
包含应用ID输入、国家选择和搜索按钮
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit,
    QComboBox, QPushButton, QLabel, QProgressBar
)

from ui.font_config import FontConfig

from utils.helpers import load_country_mapping


class SearchWidget(QWidget):
    """搜索区域组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 搜索区域 - 移除背景色
        search_frame = QWidget()
        search_frame.setStyleSheet("""
            QWidget {
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setSpacing(15)
        
        # 应用ID输入 - 现代化样式
        id_label = QLabel("应用ID:")
        id_label.setFont(FontConfig.get_label_font())  # 使用统一的标签字体
        id_label.setStyleSheet("color: #2c3e50;")
        search_layout.addWidget(id_label)
        
        self.app_id_input = QLineEdit()
        self.app_id_input.setPlaceholderText("请输入应用ID或Bundle ID")
        self.app_id_input.setMinimumWidth(300)
        self.app_id_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
                outline: none;
            }
        """)
        search_layout.addWidget(self.app_id_input)
        
        # 国家/地区选择 - 现代化样式
        country_label = QLabel("国家/地区:")
        country_label.setFont(FontConfig.get_label_font())  # 使用统一的标签字体
        country_label.setStyleSheet("color: #2c3e50;")
        search_layout.addWidget(country_label)
        
        self.country_combo = QComboBox()
        self.country_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
                color: #2c3e50;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: #ffffff;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
            }
        """)
        
        # 从配置文件加载国家列表，默认选择中国
        country_map = load_country_mapping()
        china_index = 0
        current_index = 0
        for code, name in country_map.items():
            self.country_combo.addItem(f"{code} - {name}")
            if code == "cn":
                china_index = current_index
            current_index += 1
        
        # 设置默认选择中国
        self.country_combo.setCurrentIndex(china_index)
        
        search_layout.addWidget(self.country_combo)
        
        # 搜索按钮 - 现代化渐变按钮
        self.search_button = QPushButton("🔍 查询")
        self.search_button.setMinimumWidth(100)
        self.search_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2980b9, stop:1 #21618c);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #21618c, stop:1 #1b4f72);
            }
            QPushButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        search_layout.addWidget(self.search_button)
        
        # 进度条 - 现代化样式
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                text-align: center;
                height: 8px;
                background-color: #fafafa;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
                border-radius: 6px;
            }
        """)
        search_layout.addWidget(self.progress_bar)
        
        layout.addWidget(search_frame)
    
    def get_search_params(self):
        """获取搜索参数"""
        app_id = self.app_id_input.text().strip()
        country_text = self.country_combo.currentText()
        country = country_text.split(" - ")[0]
        return app_id, country
    
    def set_search_enabled(self, enabled):
        """设置搜索按钮状态"""
        self.search_button.setEnabled(enabled)
    
    def show_progress(self, show):
        """显示/隐藏进度条"""
        self.progress_bar.setVisible(show)
        if show:
            self.progress_bar.setRange(0, 0)  # 不确定进度
    
    def set_app_id(self, app_id):
        """设置应用ID"""
        self.app_id_input.setText(app_id)
    
    def get_app_id(self):
        """获取应用ID"""
        return self.app_id_input.text().strip()