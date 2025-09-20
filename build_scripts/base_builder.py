"""
基础构建器模块
提供通用的构建功能
"""

import sys

from .config import BuildConfig
from .utils import run_command, clean_build_directories


class BaseBuilder:
    """基础构建器类"""
    
    def __init__(self):
        self.config = BuildConfig()
        self.project_root = self.config.project_root
        self.app_name = self.config.app_name
        
    def get_pyinstaller_command(self, platform_name):
        """获取 PyInstaller 命令"""
        base_cmd = [
            sys.executable, '-m', 'PyInstaller',
            f'--name={self.app_name}',  # 移除引号，避免双重引号问题
            '--onefile',
            '--windowed',
            '--clean',
            '--noconfirm',
            f'--distpath={self.config.get_dist_path()}',
            f'--workpath={self.config.get_build_path()}',
            f'--specpath={self.project_root}',
        ]
        
        # 添加图标
        icon_path = self.config.get_icon_path(platform_name)
        if icon_path.exists():
            base_cmd.extend([f'--icon={str(icon_path)}'])
        
        # 添加数据文件
        separator = ";" if platform_name == "windows" else ":"
        assets_path = self.project_root / "assets"
        config_path = self.project_root / "config"
        
        if assets_path.exists():
            base_cmd.extend([f'--add-data={str(assets_path)}{separator}assets'])
        
        if config_path.exists():
            base_cmd.extend([f'--add-data={str(config_path)}{separator}config'])
        
        # 添加主文件
        base_cmd.append(str(self.project_root / "main.py"))
        
        return base_cmd
    
    def get_pyinstaller_command_onedir(self, platform_name):
        """获取 PyInstaller 命令 (onedir 模式)"""
        base_cmd = [
            sys.executable, '-m', 'PyInstaller',
            f'--name={self.app_name}',  # 移除引号，避免双重引号问题
            # 使用 onedir 模式而不是 onefile
            '--onedir',
            '--windowed',
            '--clean',
            '--noconfirm',
            # 优化构建性能
            '--log-level=WARN',  # 减少日志输出
            '--exclude-module=tkinter',  # 排除不需要的模块
            f'--distpath={self.config.get_dist_path()}',
            f'--workpath={self.config.get_build_path()}',
            f'--specpath={self.project_root}',
        ]
        
        # 添加图标
        icon_path = self.config.get_icon_path(platform_name)
        if icon_path.exists():
            base_cmd.extend([f'--icon={str(icon_path)}'])
        
        # 添加数据文件
        separator = ";" if platform_name == "windows" else ":"
        assets_path = self.project_root / "assets"
        config_path = self.project_root / "config"
        
        if assets_path.exists():
            base_cmd.extend([f'--add-data={str(assets_path)}{separator}assets'])
        
        if config_path.exists():
            base_cmd.extend([f'--add-data={str(config_path)}{separator}config'])
        
        # 添加主文件
        base_cmd.append(str(self.project_root / "main.py"))
        
        return base_cmd
    
    def build_executable(self, platform_name):
        """构建可执行文件"""
        print(f"🏗️  构建 {platform_name} 可执行文件...")
        
        cmd = self.get_pyinstaller_command(platform_name)
        
        # macOS构建PySide6应用需要更长时间，设置30分钟超时
        timeout = 1800 if platform_name == "macos" else 600
        result = run_command(cmd, cwd=self.project_root, timeout=timeout)
        if result and result.returncode == 0:
            print(f"✅ {platform_name} 可执行文件构建成功")
            return True
        else:
            print(f"❌ {platform_name} 可执行文件构建失败")
            return False
    
    def build_executable_onedir(self, platform_name):
        """构建可执行文件 (onedir 模式)"""
        print(f"🏗️  构建 {platform_name} 可执行文件 (onedir 模式)...")
        
        cmd = self.get_pyinstaller_command_onedir(platform_name)
        
        # macOS构建PySide6应用需要更长时间，设置30分钟超时
        timeout = 1800 if platform_name == "macos" else 600
        result = run_command(cmd, cwd=self.project_root, timeout=timeout)
        if result and result.returncode == 0:
            print(f"✅ {platform_name} 可执行文件构建成功")
            return True
        else:
            print(f"❌ {platform_name} 可执行文件构建失败")
            return False
    
    def clean(self):
        """清理构建目录"""
        clean_build_directories(self.project_root)
    
    def get_executable_path(self, platform_name):
        """获取可执行文件路径"""
        dist_path = self.config.get_dist_path()
        
        if platform_name == "windows":
            exe_name = f"{self.app_name}.exe"
        else:
            exe_name = self.app_name
        
        return dist_path / exe_name