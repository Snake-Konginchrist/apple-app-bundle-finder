"""
Linux 构建器模块
专门处理 Linux 平台的构建任务
"""

import shutil

from .base_builder import BaseBuilder
from .utils import run_command


class LinuxBuilder(BaseBuilder):
    """Linux 构建器"""
    
    def __init__(self):
        super().__init__()
        self.platform_name = "linux"
    
    def build(self):
        """构建 Linux 版本"""
        print("🔨 开始构建 Linux 版本...")
        
        # 构建可执行文件
        if not self.build_executable(self.platform_name):
            return False
        
        # 创建 AppImage
        self.create_appimage()
        
        # 创建压缩包
        self.create_archive()
        
        print("✅ Linux 版本构建完成")
        return True
    
    def create_appimage(self):
        """创建 AppImage"""
        print("📦 创建 AppImage...")
        
        # 检查 appimage-builder 是否可用
        if not self.check_appimage_builder():
            print("⚠️  appimage-builder 未安装，跳过 AppImage 创建")
            print("   安装方法: pip install appimage-builder")
            return
        
        dist_path = self.config.get_dist_path()
        exe_path = self.get_executable_path(self.platform_name)
        
        if not exe_path.exists():
            print("⚠️  可执行文件不存在，跳过 AppImage 创建")
            return
        
        # 创建 AppDir
        appdir_path = dist_path / "AppDir"
        if appdir_path.exists():
            shutil.rmtree(appdir_path)
        
        # 创建 AppDir 结构
        self.create_appdir_structure(appdir_path)
        
        # 创建 AppImage 配置
        self.create_appimage_config(appdir_path)
        
        # 构建 AppImage
        cmd = [
            'appimage-builder',
            '--recipe', str(appdir_path / 'AppImageBuilder.yml'),
            '--appdir', str(appdir_path),
            '--output', str(dist_path)
        ]
        
        result = run_command(cmd, cwd=dist_path)
        
        # 清理
        if appdir_path.exists():
            shutil.rmtree(appdir_path)
        
        if result and result.returncode == 0:
            print("✅ AppImage 创建成功")
        else:
            print("⚠️  AppImage 创建失败")
    
    def create_appdir_structure(self, appdir_path):
        """创建 AppDir 目录结构"""
        appdir_path.mkdir(parents=True, exist_ok=True)
        
        # 创建目录
        (appdir_path / "usr" / "bin").mkdir(parents=True, exist_ok=True)
        (appdir_path / "usr" / "share" / "applications").mkdir(parents=True, exist_ok=True)
        (appdir_path / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True, exist_ok=True)
        
        # 复制可执行文件
        exe_path = self.get_executable_path(self.platform_name)
        if exe_path.exists():
            shutil.copy2(exe_path, appdir_path / "usr" / "bin" / self.app_name.lower())
        
        # 复制资源文件
        if (self.project_root / "assets").exists():
            shutil.copytree(self.project_root / "assets", appdir_path / "assets", dirs_exist_ok=True)
        
        if (self.project_root / "config").exists():
            shutil.copytree(self.project_root / "config", appdir_path / "config", dirs_exist_ok=True)
        
        # 复制图标
        icon_path = self.config.get_icon_path(self.platform_name)
        if icon_path.exists():
            shutil.copy2(icon_path, appdir_path / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps" / f"{self.app_name.lower()}.png")
        
        # 创建桌面文件
        self.create_desktop_file(appdir_path)
    
    def create_desktop_file(self, appdir_path):
        """创建桌面文件"""
        desktop_content = f"""[Desktop Entry]
Name={self.app_name}
Comment={self.config.description}
Exec={self.app_name.lower()}
Icon={self.app_name.lower()}
Terminal=false
Type=Application
Categories=Utility;Application;
StartupNotify=true
"""
        
        desktop_file_path = appdir_path / "usr" / "share" / "applications" / f"{self.app_name.lower()}.desktop"
        with open(desktop_file_path, 'w', encoding='utf-8') as f:
            f.write(desktop_content)
        
        # 设置可执行权限
        desktop_file_path.chmod(0o755)
    
    def create_appimage_config(self, appdir_path):
        """创建 AppImage 配置"""
        config_content = f"""version: 1
script:
  - cp $(which {self.app_name.lower()}) usr/bin/
AppDir:
  path: {appdir_path}
  app_info:
    id: com.{self.config.author.lower()}.{self.app_name.lower()}
    name: {self.app_name.lower()}
    icon: {self.app_name.lower()}
    version: {self.config.version}
    exec: usr/bin/{self.app_name.lower()}
    exec_args: $@
  apt:
    arch: amd64
    sources:
      - sourceline: deb http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse
      - sourceline: deb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse
      - sourceline: deb http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse
      - sourceline: deb http://security.ubuntu.com/ubuntu focal-security main restricted universe multiverse
    include:
      - python3
      - python3-pip
      - python3-setuptools
      - python3-wheel
  files:
    include:
      - assets
      - config
    exclude:
      - usr/share/doc
      - usr/share/man
      - usr/share/locale
AppImage:
  arch: x86_64
  update-information: guess
"""
        
        with open(appdir_path / "AppImageBuilder.yml", 'w', encoding='utf-8') as f:
            f.write(config_content)
    
    def create_archive(self):
        """创建压缩包"""
        print("📁 创建压缩包...")
        
        dist_path = self.config.get_dist_path()
        exe_path = self.get_executable_path(self.platform_name)
        
        if not exe_path.exists():
            print("⚠️  可执行文件不存在，跳过压缩包创建")
            return
        
        # 创建临时目录
        temp_dir = dist_path / "archive_temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(exist_ok=True)
        
        # 复制可执行文件
        shutil.copy2(exe_path, temp_dir / exe_path.name)
        
        # 复制资源文件
        if (self.project_root / "assets").exists():
            shutil.copytree(self.project_root / "assets", temp_dir / "assets", dirs_exist_ok=True)
        
        if (self.project_root / "config").exists():
            shutil.copytree(self.project_root / "config", temp_dir / "config", dirs_exist_ok=True)
        
        # 创建启动脚本
        self.create_launch_script(temp_dir)
        
        # 创建说明文件
        self.create_readme(temp_dir)
        
        # 创建 tar.gz 压缩包
        archive_name = f"{self.app_name}_Linux_x64.tar.gz"
        archive_path = dist_path / archive_name
        
        cmd = [
            'tar', '-czf', str(archive_path),
            '-C', str(temp_dir.parent),
            temp_dir.name
        ]
        
        result = run_command(cmd)
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
        if result and result.returncode == 0:
            print("✅ 压缩包创建成功")
        else:
            print("⚠️  压缩包创建失败")
    
    def create_launch_script(self, temp_dir):
        """创建启动脚本"""
        script_content = f"""#!/bin/bash
# {self.app_name} 启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 设置环境变量
export PATH="$SCRIPT_DIR:$PATH"

# 运行程序
./{self.app_name}
"""
        
        script_path = temp_dir / f"{self.app_name}.sh"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # 设置可执行权限
        script_path.chmod(0o755)
    
    def create_readme(self, temp_dir):
        """创建说明文件"""
        readme_content = f"""{self.app_name} - Linux 版本

版本: {self.config.version}
作者: {self.config.author}

系统要求:
- Linux x86_64
- Python 3.6 或更高版本 (如果使用源码)

安装方法:
1. 解压压缩包到任意目录
2. 运行 {self.app_name}.sh 启动程序
3. 或者直接运行 {self.app_name} 可执行文件

卸载方法:
直接删除整个目录即可

注意事项:
- 确保有可执行权限: chmod +x {self.app_name}
- 如果遇到依赖问题，请安装相应的系统库
"""
        
        with open(temp_dir / "README.txt", 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def check_appimage_builder(self):
        """检查 appimage-builder 是否可用"""
        try:
            result = run_command(['appimage-builder', '--version'])
            return result is not None and result.returncode == 0
        except:
            return false