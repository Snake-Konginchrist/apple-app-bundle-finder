"""
基本信息面板组件
显示应用图标、名称、开发者、Bundle ID、版本、价格等基本信息
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QGroupBox, QApplication
)

from models.app_info import AppInfo
from utils.helpers import format_number, load_image_from_url


class InfoPanelWidget(QWidget):
    """基本信息面板组件"""
    
    def __init__(self):
        super().__init__()
        self.current_app_info = None
        self.current_icon = None  # 保存原始图标用于重新缩放
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 基本信息组 - 移除背景色
        basic_group = QGroupBox("基本信息")
        basic_group.setStyleSheet("""
            QGroupBox {
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                padding: 15px;
                margin-top: 5px;
                font-size: 16px;
                font-weight: 600;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
            }
        """)
        basic_layout = QGridLayout(basic_group)
        basic_layout.setSpacing(8)  # 增加间距，避免字体截断
        basic_layout.setVerticalSpacing(10)  # 增加垂直间距
        # 设置列拉伸比例：标签列和值列都需要足够空间
        basic_layout.setColumnStretch(1, 1)  # 标签列也需要一些空间
        basic_layout.setColumnStretch(2, 2)    # 值列获得更多空间
        
        # 应用图标
        self.app_icon_label = QLabel()
        self.app_icon_label.setMinimumSize(80, 80)
        self.app_icon_label.setMaximumSize(120, 120)
        self.app_icon_label.setAlignment(Qt.AlignCenter)
        self.app_icon_label.setStyleSheet("""
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            background-color: #fafafa;
            font-size: 14px;
            color: #7f8c8d;
        """)
        self.app_icon_label.setText("暂无图标")
        basic_layout.addWidget(self.app_icon_label, 0, 0, 3, 1)
        
        # 应用名称 - 优化字体显示，避免截断
        name_label = QLabel("应用名称:")
        name_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        name_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        name_label.setStyleSheet("font-weight: 500; color: #7f8c8d; font-size: 14px; padding: 2px 0; min-height: 24px;")
        basic_layout.addWidget(name_label, 0, 1)
        
        self.app_name_label = QLabel("未查询")
        self.app_name_label.setWordWrap(True)
        self.app_name_label.setMinimumWidth(200)  # 设置最小宽度确保换行
        self.app_name_label.setStyleSheet("color: #34495e; font-size: 14px; padding: 2px 0; min-height: 20px;")
        basic_layout.addWidget(self.app_name_label, 0, 2)
        
        # 开发者 - 优化字体显示，避免截断
        dev_label = QLabel("开发者:")
        dev_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        dev_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        dev_label.setStyleSheet("font-weight: 500; color: #7f8c8d; font-size: 14px; padding: 2px 0; min-height: 24px;")
        basic_layout.addWidget(dev_label, 1, 1)
        
        self.developer_label = QLabel("未查询")
        self.developer_label.setWordWrap(True)
        self.developer_label.setStyleSheet("color: #34495e; font-size: 14px; padding: 2px 0; min-height: 20px;")
        basic_layout.addWidget(self.developer_label, 1, 2)
        
        # Bundle ID - 优化字体显示，避免截断
        bundle_label = QLabel("Bundle ID:")
        bundle_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        bundle_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        bundle_label.setStyleSheet("font-weight: 500; color: #7f8c8d; font-size: 14px; padding: 2px 0; min-height: 24px;")
        basic_layout.addWidget(bundle_label, 2, 1)
        
        self.bundle_id_label = QLabel("未查询")
        self.bundle_id_label.setWordWrap(True)
        self.bundle_id_label.setStyleSheet("color: #34495e; font-size: 14px; padding: 2px 0; min-height: 20px;")
        basic_layout.addWidget(self.bundle_id_label, 2, 2)
        
        layout.addWidget(basic_group)
        
        # 版本信息组 - 移除背景色
        version_group = QGroupBox("版本信息")
        version_group.setStyleSheet("""
            QGroupBox {
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                padding: 15px;
                margin-top: 5px;
                font-size: 16px;
                font-weight: 600;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
            }
        """)
        version_layout = QGridLayout(version_group)
        version_layout.setSpacing(8)  # 增加间距，避免字体截断
        version_layout.setVerticalSpacing(10)  # 增加垂直间距
        # 设置列拉伸比例
        version_layout.setColumnStretch(0, 1)  # 标签列也需要一些空间
        version_layout.setColumnStretch(1, 2)    # 值列获得更多空间
        
        version_label_style = "font-weight: 500; color: #7f8c8d; font-size: 14px; padding: 2px 0; min-height: 24px;"
        version_value_style = "color: #34495e; font-size: 14px; padding: 2px 0; min-height: 20px;"
        
        version_label = QLabel("当前版本:")
        version_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        version_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        version_label.setStyleSheet(version_label_style)
        version_layout.addWidget(version_label, 0, 0)
        self.version_label = QLabel("未查询")
        self.version_label.setWordWrap(True)
        self.version_label.setStyleSheet(version_value_style)
        version_layout.addWidget(self.version_label, 0, 1)
        
        release_date_label = QLabel("发布日期:")
        release_date_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        release_date_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        release_date_label.setStyleSheet(version_label_style)
        version_layout.addWidget(release_date_label, 1, 0)
        self.release_date_label = QLabel("未查询")
        self.release_date_label.setWordWrap(True)
        self.release_date_label.setStyleSheet(version_value_style)
        version_layout.addWidget(self.release_date_label, 1, 1)
        
        min_os_label = QLabel("最低系统:")
        min_os_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        min_os_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        min_os_label.setStyleSheet(version_label_style)
        version_layout.addWidget(min_os_label, 2, 0)
        self.min_os_label = QLabel("未查询")
        self.min_os_label.setWordWrap(True)
        self.min_os_label.setStyleSheet(version_value_style)
        version_layout.addWidget(self.min_os_label, 2, 1)
        
        layout.addWidget(version_group)
        
        # 评分信息组 - 移除背景色
        rating_group = QGroupBox("评分信息")
        rating_group.setStyleSheet("""
            QGroupBox {
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                padding: 15px;
                margin-top: 5px;
                font-size: 16px;
                font-weight: 600;
                color: #2c3e50;
                min-height: 40px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
            }
        """)
        rating_layout = QGridLayout(rating_group)
        rating_layout.setSpacing(8)  # 增加间距，避免字体截断
        rating_layout.setVerticalSpacing(10)  # 增加垂直间距
        # 设置列拉伸比例
        rating_layout.setColumnStretch(0, 1)  # 标签列也需要一些空间
        rating_layout.setColumnStretch(1, 2)    # 值列获得更多空间
        
        rating_label_style = "font-weight: 500; color: #7f8c8d; font-size: 14px; padding: 2px 0; min-height: 24px;"
        rating_value_style = "color: #34495e; font-size: 14px; padding: 2px 0; min-height: 20px;"
        
        rating_label = QLabel("平均评分:")
        rating_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        rating_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        rating_label.setStyleSheet(rating_label_style)
        rating_layout.addWidget(rating_label, 0, 0)
        self.rating_label = QLabel("未查询")
        self.rating_label.setWordWrap(True)
        self.rating_label.setStyleSheet(rating_value_style)
        rating_layout.addWidget(self.rating_label, 0, 1)
        
        rating_count_label = QLabel("评分人数:")
        rating_count_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        rating_count_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        rating_count_label.setStyleSheet(rating_label_style)
        rating_layout.addWidget(rating_count_label, 1, 0)
        self.rating_count_label = QLabel("未查询")
        self.rating_count_label.setWordWrap(True)
        self.rating_count_label.setStyleSheet(rating_value_style)
        rating_layout.addWidget(self.rating_count_label, 1, 1)
        
        layout.addWidget(rating_group)
        
        # 其他信息组 - 移除背景色，与版本信息和评分信息保持一致
        other_group = QGroupBox("其他信息")
        other_group.setStyleSheet("""
            QGroupBox {
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                padding: 15px;
                margin-top: 5px;
                font-size: 16px;
                font-weight: 600;
                color: #2c3e50;
                min-height: 40px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
            }
        """)
        other_layout = QGridLayout(other_group)
        other_layout.setSpacing(8)  # 增加间距，避免字体截断
        other_layout.setVerticalSpacing(10)  # 增加垂直间距
        # 设置列拉伸比例
        other_layout.setColumnStretch(0, 1)  # 标签列也需要一些空间
        other_layout.setColumnStretch(1, 2)    # 值列获得更多空间
        
        other_label_style = "font-weight: 500; color: #7f8c8d; font-size: 14px; padding: 2px 0; min-height: 24px;"
        other_value_style = "color: #34495e; font-size: 14px; padding: 2px 0; min-height: 20px;"
        
        price_label = QLabel("价格:")
        price_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        price_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        price_label.setStyleSheet(other_label_style)
        other_layout.addWidget(price_label, 0, 0)
        self.price_label = QLabel("未查询")
        self.price_label.setWordWrap(True)
        self.price_label.setStyleSheet(other_value_style)
        other_layout.addWidget(self.price_label, 0, 1)
        
        file_size_label = QLabel("文件大小:")
        file_size_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        file_size_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        file_size_label.setStyleSheet(other_label_style)
        other_layout.addWidget(file_size_label, 1, 0)
        self.file_size_label = QLabel("未查询")
        self.file_size_label.setWordWrap(True)
        self.file_size_label.setStyleSheet(other_value_style)
        other_layout.addWidget(self.file_size_label, 1, 1)
        
        category_label = QLabel("分类:")
        category_label.setMinimumWidth(80)  # 设置标签最小宽度避免截断
        category_label.setWordWrap(True)  # 设置自动换行，与值字段保持一致
        category_label.setStyleSheet(other_label_style)
        other_layout.addWidget(category_label, 2, 0)
        self.category_label = QLabel("未查询")
        self.category_label.setWordWrap(True)
        self.category_label.setStyleSheet(other_value_style)
        other_layout.addWidget(self.category_label, 2, 1)
        
        layout.addWidget(other_group)
        
        # 操作按钮 - 现代化样式
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.view_in_store_button = QPushButton("🌐 在App Store中查看")
        self.view_in_store_button.setEnabled(False)
        self.view_in_store_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                min-width: 150px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #229954, stop:1 #1e8449);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e8449, stop:1 #196f3d);
            }
            QPushButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        button_layout.addWidget(self.view_in_store_button)
        
        self.copy_info_button = QPushButton("📋 复制信息")
        self.copy_info_button.setEnabled(False)
        self.copy_info_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e67e22, stop:1 #d35400);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d35400, stop:1 #ba4a00);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ba4a00, stop:1 #a04000);
            }
            QPushButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        button_layout.addWidget(self.copy_info_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 添加弹性空间
        layout.addStretch()
    
    def clear_info(self):
        """清空信息"""
        self.current_app_info = None
        self.current_icon = None  # 清空保存的图标
        self.app_icon_label.setText("暂无图标")
        self.app_name_label.setText("未查询")
        self.developer_label.setText("未查询")
        self.bundle_id_label.setText("未查询")
        self.version_label.setText("未查询")
        self.release_date_label.setText("未查询")
        self.min_os_label.setText("未查询")
        self.rating_label.setText("未查询")
        self.rating_count_label.setText("未查询")
        self.price_label.setText("未查询")
        self.file_size_label.setText("未查询")
        self.category_label.setText("未查询")
        self.view_in_store_button.setEnabled(False)
        self.copy_info_button.setEnabled(False)
    
    def display_app_info(self, app_info: AppInfo):
        """显示应用信息"""
        self.current_app_info = app_info
        
        # 基本信息
        self.app_name_label.setText(app_info.track_name or "未知")
        self.developer_label.setText(app_info.artist_name or "未知")
        self.bundle_id_label.setText(app_info.bundle_id or "未知")
        
        # 版本信息
        self.version_label.setText(app_info.version or "未知")
        self.release_date_label.setText(app_info.get_formatted_release_date())
        self.min_os_label.setText(app_info.minimum_os_version or "未知")
        
        # 评分信息
        self.rating_label.setText(app_info.get_rating_stars())
        self.rating_count_label.setText(format_number(app_info.user_rating_count))
        
        # 其他信息
        self.price_label.setText(app_info.formatted_price or "未知")
        self.file_size_label.setText(app_info.get_formatted_file_size())
        self.category_label.setText(app_info.primary_genre_name or "未知")
        
        # 加载应用图标
        self.load_app_icon(app_info.artwork_url_100)
        
        # 启用按钮
        self.view_in_store_button.setEnabled(bool(app_info.track_view_url))
        self.copy_info_button.setEnabled(True)
    
    def load_app_icon(self, icon_url: str):
        """加载应用图标"""
        if not icon_url:
            self.app_icon_label.setText("暂无图标")
            return
        
        # 在新线程中加载图标
        QTimer.singleShot(100, lambda: self._load_icon_async(icon_url))
    
    def _load_icon_async(self, icon_url: str):
        """异步加载图标"""
        try:
            pixmap = load_image_from_url(icon_url)
            if pixmap:
                self.current_icon = pixmap  # 保存原始图标
                self.rescale_icon()  # 根据当前标签大小缩放图标
            else:
                self.app_icon_label.setText("加载失败")
        except Exception as e:
            print(f"加载图标失败: {e}")
            self.app_icon_label.setText("加载失败")
    
    def rescale_icon(self):
        """重新缩放图标以适应标签大小"""
        if self.current_icon and not self.current_icon.isNull():
            # 获取标签当前大小，保持1:1比例缩放图标
            label_size = self.app_icon_label.size()
            icon_size = min(label_size.width(), label_size.height()) - 8  # 减去边框和内边距
            scaled_pixmap = self.current_icon.scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.app_icon_label.setPixmap(scaled_pixmap)
    
    def resizeEvent(self, event):
        """处理窗口大小改变事件"""
        super().resizeEvent(event)
        # 当标签大小改变时重新缩放图标
        QTimer.singleShot(0, self.rescale_icon)
    
    def copy_app_info(self):
        """复制应用信息到剪贴板"""
        if not self.current_app_info:
            return
        
        app_info = self.current_app_info
        info_text = f"""应用名称: {app_info.track_name}
开发者: {app_info.artist_name}
Bundle ID: {app_info.bundle_id}
版本: {app_info.version}
发布日期: {app_info.get_formatted_release_date()}
价格: {app_info.formatted_price}
文件大小: {app_info.get_formatted_file_size()}
分类: {app_info.primary_genre_name}
评分: {app_info.get_rating_stars()}
评分人数: {format_number(app_info.user_rating_count)}
最低系统版本: {app_info.minimum_os_version}
App Store链接: {app_info.track_view_url}"""
        
        clipboard = QApplication.clipboard()
        clipboard.setText(info_text)
        
        return True  # 返回成功状态
    
    def get_app_info(self):
        """获取当前应用信息"""
        return self.current_app_info
    
    # 获取各个控件的方法，方便主窗口访问
    def get_app_icon_label(self):
        return self.app_icon_label
    
    def get_app_name_label(self):
        return self.app_name_label
    
    def get_developer_label(self):
        return self.developer_label
    
    def get_bundle_id_label(self):
        return self.bundle_id_label
    
    def get_version_label(self):
        return self.version_label
    
    def get_release_date_label(self):
        return self.release_date_label
    
    def get_min_os_label(self):
        return self.min_os_label
    
    def get_rating_label(self):
        return self.rating_label
    
    def get_rating_count_label(self):
        return self.rating_count_label
    
    def get_price_label(self):
        return self.price_label
    
    def get_file_size_label(self):
        return self.file_size_label
    
    def get_category_label(self):
        return self.category_label
    
    def get_view_button(self):
        return self.view_in_store_button
    
    def get_copy_button(self):
        return self.copy_info_button