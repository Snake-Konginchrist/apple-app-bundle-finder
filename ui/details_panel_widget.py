"""
详细信息面板组件
显示应用描述、更新说明和详细信息
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGroupBox
)

from models.app_info import AppInfo
from ui.font_config import FontConfig
from utils.helpers import format_number


class DetailsPanelWidget(QWidget):
    """详细信息面板组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 应用描述 - 移除背景色，与详细信息保持一致
        desc_group = QGroupBox("应用描述")
        desc_group.setStyleSheet("""
            QGroupBox {
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                padding: 20px;
                margin-top: 10px;
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
        desc_layout = QVBoxLayout(desc_group)
        desc_layout.setContentsMargins(10, 10, 10, 10)
        
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setMaximumHeight(250)
        self.description_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                line-height: 1.6;
                color: #34495e;
                background-color: #fafafa;
            }
            QTextEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
        """)
        desc_layout.addWidget(self.description_text)
        
        layout.addWidget(desc_group)
        
        # 更新说明 - 移除背景色，与详细信息保持一致
        notes_group = QGroupBox("更新说明")
        notes_group.setStyleSheet("""
            QGroupBox {
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                padding: 20px;
                margin-top: 10px;
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
        notes_layout = QVBoxLayout(notes_group)
        notes_layout.setContentsMargins(10, 10, 10, 10)
        
        self.release_notes_text = QTextEdit()
        self.release_notes_text.setReadOnly(True)
        self.release_notes_text.setMaximumHeight(200)
        self.release_notes_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                line-height: 1.6;
                color: #34495e;
                background-color: #fafafa;
            }
            QTextEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
        """)
        notes_layout.addWidget(self.release_notes_text)
        
        layout.addWidget(notes_group)
        
        # 详细信息 - 移除背景色
        detail_group = QGroupBox("详细信息")
        detail_group.setStyleSheet("""
            QGroupBox {
                border-radius: 15px;
                border: 1px solid #e0e0e0;
                padding: 20px;
                margin-top: 10px;
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
        detail_layout = QVBoxLayout(detail_group)
        detail_layout.setContentsMargins(10, 10, 10, 10)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(FontConfig.get_monospace_font())  # 使用统一的等宽字体
        self.details_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                font-size: 13px;
                line-height: 1.6;
                color: #34495e;
                background-color: #fafafa;

            }
            QTextEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
        """)
        detail_layout.addWidget(self.details_text)
        
        layout.addWidget(detail_group)
    
    def clear_details(self):
        """清空详细信息"""
        self.description_text.setPlainText("")
        self.release_notes_text.setPlainText("")
        self.details_text.setPlainText("")
    
    def display_app_info(self, app_info: AppInfo):
        """显示应用详细信息"""
        # 描述信息
        self.description_text.setPlainText(app_info.description or "暂无描述")
        self.release_notes_text.setPlainText(app_info.release_notes or "暂无更新说明")
        
        # 详细信息
        self.display_detailed_info(app_info)
    
    def display_detailed_info(self, app_info: AppInfo):
        """显示详细信息"""
        details = []
        
        details.append(f"Track ID: {app_info.track_id}")
        details.append(f"Artist ID: {app_info.artist_id}")
        details.append(f"Bundle ID: {app_info.bundle_id}")
        details.append(f"版本: {app_info.version}")
        details.append(f"价格: {app_info.formatted_price}")
        details.append(f"货币: {app_info.currency}")
        details.append(f"文件大小: {app_info.get_formatted_file_size()}")
        details.append(f"内容分级: {app_info.content_advisory_rating or '未知'}")
        details.append(f"主要分类: {app_info.primary_genre_name}")
        
        if app_info.genres:
            details.append(f"所有分类: {', '.join(app_info.genres)}")
        
        details.append(f"平均评分: {app_info.average_user_rating or '未知'}")
        details.append(f"评分人数: {format_number(app_info.user_rating_count)}")
        details.append(f"当前版本评分: {app_info.average_user_rating_for_current_version or '未知'}")
        details.append(f"当前版本评分人数: {format_number(app_info.user_rating_count_for_current_version)}")
        
        if app_info.supported_devices:
            details.append(f"支持设备: {', '.join(app_info.supported_devices[:5])}...")
        
        details.append(f"Game Center: {'是' if app_info.is_game_center_enabled else '否'}")
        
        if app_info.track_view_url:
            details.append(f"App Store链接: {app_info.track_view_url}")
        
        if app_info.seller_url:
            details.append(f"开发者网站: {app_info.seller_url}")
        
        if app_info.support_url:
            details.append(f"支持网站: {app_info.support_url}")
        
        self.details_text.setPlainText('\n'.join(details))
    
    def set_description(self, text):
        """设置应用描述"""
        self.description_text.setPlainText(text or "暂无描述")
    
    def set_release_notes(self, text):
        """设置更新说明"""
        self.release_notes_text.setPlainText(text or "暂无更新说明")
    
    def set_detailed_info(self, text):
        """设置详细信息"""
        self.details_text.setPlainText(text or "")
    
    def get_description_widget(self):
        """获取描述文本控件"""
        return self.description_text
    
    def get_release_notes_widget(self):
        """获取更新说明文本控件"""
        return self.release_notes_text
    
    def get_details_widget(self):
        """获取详细信息文本控件"""
        return self.details_text