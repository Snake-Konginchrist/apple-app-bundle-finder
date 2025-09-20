"""
跨平台字体配置模块
提供统一的字体配置方案，确保在不同操作系统上的显示一致性
"""

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
import platform


class FontConfig:
    """字体配置类"""
    
    @staticmethod
    def setup_application_fonts():
        """设置应用程序的全局字体配置"""
        app = QApplication.instance()
        if not app:
            return
        
        # 获取系统类型
        system = platform.system()
        
        # 设置应用程序默认字体
        default_font = QFont()
        
        if system == "Windows":
            # Windows 系统字体
            default_font.setFamily("Segoe UI")
        elif system == "Darwin":
            # macOS 系统字体
            default_font.setFamily("Helvetica Neue")
        else:
            # Linux 或其他系统
            default_font.setFamily("DejaVu Sans")
        
        default_font.setPointSize(12)  # 标准字号，增大字体大小
        default_font.setStyleHint(QFont.SansSerif)
        app.setFont(default_font)
        
        return default_font
    
    @staticmethod
    def get_title_font():
        """获取标题字体（应用名称等）"""
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        font.setStyleHint(QFont.SansSerif)
        
        system = platform.system()
        if system == "Windows":
            font.setFamily("Segoe UI")
        elif system == "Darwin":
            font.setFamily("Helvetica Neue")
        else:
            font.setFamily("DejaVu Sans")
        
        return font
    
    @staticmethod
    def get_monospace_font():
        """获取等宽字体（用于显示代码或结构化数据）"""
        font = QFont()
        font.setStyleHint(QFont.Monospace, QFont.PreferDefault)
        font.setFixedPitch(True)
        font.setPointSize(14)  # 增大等宽字体大小
        
        system = platform.system()
        if system == "Windows":
            font.setFamily("Consolas")
        elif system == "Darwin":
            font.setFamily("Menlo")
        else:
            font.setFamily("DejaVu Sans Mono")
        
        return font
    
    @staticmethod
    def get_label_font():
        """获取标签字体（字段名称）"""
        font = QFont()
        font.setWeight(QFont.Medium)  # 500 权重
        font.setPointSize(16)  # 增大标签字体大小
        font.setStyleHint(QFont.SansSerif)
        
        system = platform.system()
        if system == "Windows":
            font.setFamily("Segoe UI")
        elif system == "Darwin":
            font.setFamily("Helvetica Neue")
        else:
            font.setFamily("DejaVu Sans")
        
        return font
    
    @staticmethod
    def get_value_font():
        """获取值字体（字段内容）"""
        font = QFont()
        font.setPointSize(16)  # 增大值字体大小
        font.setStyleHint(QFont.SansSerif)
        
        system = platform.system()
        if system == "Windows":
            font.setFamily("Segoe UI")
        elif system == "Darwin":
            font.setFamily("Helvetica Neue")
        else:
            font.setFamily("DejaVu Sans")
        
        return font
    
    @staticmethod
    def get_button_font():
        """获取按钮字体"""
        font = QFont()
        font.setWeight(QFont.Medium)
        font.setPointSize(16)  # 增大按钮字体大小
        font.setStyleHint(QFont.SansSerif)
        
        system = platform.system()
        if system == "Windows":
            font.setFamily("Segoe UI")
        elif system == "Darwin":
            font.setFamily("Helvetica Neue")
        else:
            font.setFamily("DejaVu Sans")
        
        return font
    
    @staticmethod
    def get_status_font():
        """获取状态栏字体"""
        font = QFont()
        font.setPointSize(15)  # 增大状态栏字体大小
        font.setStyleHint(QFont.SansSerif)
        
        system = platform.system()
        if system == "Windows":
            font.setFamily("Segoe UI")
        elif system == "Darwin":
            font.setFamily("Helvetica Neue")
        else:
            font.setFamily("DejaVu Sans")
        
        return font