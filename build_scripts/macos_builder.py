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
        
        # 构建可执行文件 (使用 onedir 模式而不是 onefile)
        if not self.build_executable_onedir(self.platform_name):
            return False
        
        # 创建应用包
        self.create_app_bundle()
        
        # 创建 DMG 安装器
        self.create_dmg()
        
        print("✅ macOS 版本构建完成")
        return True
    
    def create_app_bundle(self):
        """创建应用包"""
        print("📦 创建应用包...")
        
        dist_path = self.config.get_dist_path()
        app_name = f"{self.app_name}.app"
        app_path = dist_path / app_name
        
        # 删除已存在的应用包
        if app_path.exists():
            shutil.rmtree(app_path)
        
        # 创建应用包目录结构
        contents_dir = app_path / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        macos_dir.mkdir(parents=True, exist_ok=True)
        resources_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制整个应用目录（onedir模式生成的目录）
        source_dir = dist_path / self.app_name
        if source_dir.exists() and source_dir.is_dir():
            # 复制目录中的所有内容到MacOS目录
            for item in source_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, macos_dir / item.name)
                elif item.is_dir():
                    shutil.copytree(item, macos_dir / item.name, dirs_exist_ok=True)
            
            # 设置主可执行文件权限
            main_exe = macos_dir / self.app_name
            if main_exe.exists():
                main_exe.chmod(0o755)
        
        # 复制资源文件
        if (self.project_root / "assets").exists():
            shutil.copytree(self.project_root / "assets", resources_dir / "assets", dirs_exist_ok=True)
        
        if (self.project_root / "config").exists():
            shutil.copytree(self.project_root / "config", resources_dir / "config", dirs_exist_ok=True)
        
        # 创建 Info.plist
        self.create_info_plist(contents_dir)
        
        # 复制图标
        icon_path = self.config.get_icon_path(self.platform_name)
        if icon_path.exists():
            shutil.copy2(icon_path, resources_dir / "AppIcon.icns")
        
        print("✅ 应用包创建完成")
    
    def create_info_plist(self, contents_dir):
        """创建 Info.plist 文件"""
        info_plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>zh_CN</string>
    <key>CFBundleDisplayName</key>
    <string>{self.app_name}</string>
    <key>CFBundleExecutable</key>
    <string>{self.app_name}</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.{self.config.author.lower()}.{self.app_name.lower()}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{self.app_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>{self.config.version}</string>
    <key>CFBundleSignature</key>
    <string>APL{self.app_name[:4].upper()}</string>
    <key>CFBundleVersion</key>
    <string>{self.config.version}</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright © {self.config.author}. All rights reserved.</string>
    <key>NSAppleEventsUsageDescription</key>
    <string>此应用程序需要访问系统事件。</string>
</dict>
</plist>"""
        
        with open(contents_dir / "Info.plist", 'w', encoding='utf-8') as f:
            f.write(info_plist_content)
    
    def create_dmg(self):
        """创建 DMG 安装器"""
        print("💿 创建 DMG 安装器...")
        
        dist_path = self.config.get_dist_path()
        app_name = f"{self.app_name}.app"
        app_path = dist_path / app_name
        
        if not app_path.exists():
            print("⚠️  应用包不存在，跳过 DMG 创建")
            return
        
        # 创建临时目录
        temp_dir = dist_path / "dmg_temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(exist_ok=True)
        
        # 复制应用包到临时目录
        shutil.copytree(app_path, temp_dir / app_name)
        
        # 创建背景图片
        self.create_dmg_background(temp_dir)
        
        # 创建 DMG
        dmg_path = dist_path / f"{self.app_name}_macOS.dmg"
        
        # 使用 hdiutil 创建 DMG
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
        """创建 DMG 背景"""
        # 创建背景目录
        background_dir = temp_dir / ".background"
        background_dir.mkdir(exist_ok=True)
        
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