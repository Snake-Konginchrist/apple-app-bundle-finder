"""
打包配置模块
存储应用打包相关的配置信息
"""

from pathlib import Path

class BuildConfig:
    """构建配置类"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.app_name = "Apple App Bundle Finder"
        self.app_identifier = "cn.skstudio.appleappbundlefinder"
        self.version = "1.0.0"
        self.author = "Snake Konginchrist"
        self.description = "一个用于查询 Apple 应用 Bundle ID 的工具"
        self.copyright = "Copyright © 2025 Snake Konginchrist. All rights reserved."
        self.website = "https://github.com/Snake-Konginchrist/apple-app-bundle-finder"
        self.license = "MIT"
        
        # 平台配置
        self.platforms = {
            "windows": {
                "enabled": True,
                "installer": True,
                "portable": True
            },
            "macos": {
                "enabled": True,
                "dmg": True,
                "app_bundle": True
            },
            "linux": {
                "enabled": True,
                "appimage": True,
                "portable": True
            }
        }
        
        # 文件配置
        self.files = {
            "include": [
                "assets/",
                "config/",
                "ui/",
                "api/",
                "models/",
                "utils/",
                "main.py"
            ],
            "exclude": [
                "__pycache__/",
                "*.pyc",
                "*.pyo",
                "*.pyd",
                ".git/",
                ".gitignore",
                "build/",
                "dist/",
                "*.spec",
                "*.md",
                "*.txt",
                "uv.lock",
                ".python-version"
            ]
        }
        
        # 构建选项
        self.build_options = {
            "onefile": True,
            "windowed": True,
            "clean": True,
            "noconfirm": True,
            "optimize": 2,
            "strip": True,
            "upx": False
        }
    
    def get_icon_path(self, platform):
        """获取图标路径"""
        icon_files = {
            "windows": "logo.ico",
            "macos": "logo.icns", 
            "linux": "logo.png"
        }
        
        icon_name = icon_files.get(platform, "logo.png")
        icon_path = self.project_root / "assets" / icon_name
        
        # 如果平台特定的图标不存在，使用通用图标
        if not icon_path.exists():
            generic_icon = self.project_root / "assets" / "logo.png"
            if generic_icon.exists():
                return generic_icon
        
        return icon_path
    
    def get_dist_path(self):
        """获取输出目录"""
        return self.project_root / "dist"
    
    def get_build_path(self):
        """获取构建目录"""
        return self.project_root / "build"