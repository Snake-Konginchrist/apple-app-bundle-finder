"""
macOS 构建器模块
专门处理 macOS 平台的构建任务
"""

import shutil

from .base_builder import BaseBuilder
from .utils import run_command


class MacOSBuilder(BaseBuilder):
    """macOS 构建器"""
    
    def __init__(self):
        super().__init__()
        self.platform_name = "macos"
    
    def build(self):
        """构建 macOS 版本"""
        print("🔨 开始构建 macOS 版本...")
        
        # PyInstaller 直接生成 .app 包
        if not self.build_executable_onedir(self.platform_name):
            return False
        
        # 创建 DMG 安装器
        self.create_dmg()
        
        print("✅ macOS 版本构建完成")
        return True
    

    
    def create_dmg(self):
        """创建 DMG 安装器"""
        print("💿 创建 DMG 安装器...")
        
        dist_path = self.config.get_dist_path()
        app_name = f"{self.app_name}.app"
        app_path = dist_path / app_name
        
        if not app_path.exists():
            print("⚠️  应用包不存在，跳过 DMG 创建")
            return
        
        # 创建临时目录用于 DMG 内容
        temp_dir = dist_path / "dmg_temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(exist_ok=True)
        
        # 复制应用包到临时目录
        shutil.copytree(app_path, temp_dir / app_name)
        
        # 创建背景说明
        self.create_dmg_background(temp_dir)
        
        # 创建 DMG
        dmg_path = dist_path / f"{self.app_name}.dmg"
        
        cmd = [
            'hdiutil', 'create',
            '-volname', self.app_name,
            '-srcfolder', str(temp_dir),
            '-ov',
            '-format', 'UDZO',
            str(dmg_path)
        ]
        
        result = run_command(cmd)
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
        if result and result.returncode == 0:
            print("✅ DMG 安装器创建成功")
        else:
            print("⚠️  DMG 安装器创建失败")
    
    def create_dmg_background(self, temp_dir):
        """创建 DMG 背景说明"""
        # 创建简单的背景说明
        readme_content = f"""{self.app_name}

将 {self.app_name}.app 拖到 Applications 文件夹中安装

版本: {self.config.version}
作者: {self.config.author}
"""
        
        with open(temp_dir / "README.txt", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # 创建符号链接到 Applications
        applications_link = temp_dir / "Applications"
        if not applications_link.exists():
            applications_link.symlink_to("/Applications")