"""
构建管理器模块
统一管理所有平台的构建过程
"""

import argparse
import sys
from pathlib import Path
from typing import List

from .config import BuildConfig
from .linux_builder import LinuxBuilder
from .macos_builder import MacOSBuilder
from .utils import print_build_info, print_separator, check_dependencies
from .windows_builder import WindowsBuilder


class BuildManager:
    """构建管理器"""
    
    def __init__(self):
        self.config = BuildConfig()
        self.builders = {
            'windows': WindowsBuilder(),
            'macos': MacOSBuilder(),
            'linux': LinuxBuilder()
        }
    
    def build(self, platform: str, installer: bool = False, architecture: str = None, clean: bool = False):
        """构建指定平台的应用"""
        if clean:
            print("🧹 清理构建目录...")
            self.clean_all()
            print_separator()
        
        if platform not in self.builders:
            print(f"⚠️  不支持的平台: {platform}")
            return False
        
        print(f"🚀 开始构建 {platform} 平台...")
        print_separator()
        
        try:
            builder = self.builders[platform]
            # 设置架构参数
            if architecture and hasattr(builder, 'set_architecture'):
                builder.set_architecture(architecture)
            
            if installer and hasattr(builder, 'build_installer'):
                success = builder.build_installer()
            else:
                success = builder.build()
            
            if success:
                print(f"✅ {platform} 平台构建成功")
                return True
            else:
                print(f"❌ {platform} 平台构建失败")
                return False
        except Exception as e:
            print(f"❌ {platform} 平台构建失败: {e}")
            return False
    
    def run(self, platforms: List[str] = None, clean: bool = False):
        """运行构建过程"""
        print_build_info(self.config)
        
        # 检查依赖
        if not self.check_dependencies():
            return False
        
        # 清理构建目录
        if clean:
            print("🧹 清理构建目录...")
            self.clean_all()
            print_separator()
        
        # 确定要构建的平台
        if platforms is None:
            platforms = self.get_enabled_platforms()
        
        if not platforms:
            print("⚠️  没有启用的平台需要构建")
            return False
        
        # 构建各个平台
        success = True
        for platform in platforms:
            if not self.build(platform, clean=False):
                success = False
        
        # 显示构建结果
        self.show_build_results(platforms)
        
        return success
    
    def get_enabled_platforms(self) -> List[str]:
        """获取启用的平台列表"""
        enabled_platforms = []
        
        if self.config.platforms.get('windows', {}).get('enabled', True):
            enabled_platforms.append('windows')
        
        if self.config.platforms.get('macos', {}).get('enabled', True):
            enabled_platforms.append('macos')
        
        if self.config.platforms.get('linux', {}).get('enabled', True):
            enabled_platforms.append('linux')
        
        return enabled_platforms
    
    def check_dependencies(self) -> bool:
        """检查依赖"""
        print("🔍 检查依赖...")
        
        # 检查 Python 依赖
        python_deps = ['PyInstaller']
        if not check_dependencies(python_deps, import_check=True):
            print("❌ Python 依赖检查失败")
            return False
        
        # 检查系统工具
        system_tools = []
        for platform in self.get_enabled_platforms():
            if platform == 'windows':
                system_tools.extend(['makensis'])
            elif platform == 'linux':
                system_tools.extend(['appimage-builder'])
        
        if system_tools and not check_dependencies(system_tools, import_check=False):
            print("⚠️  某些系统工具未安装，相关功能可能无法使用")
        
        print("✅ 依赖检查完成")
        return True
    
    def clean_all(self):
        """清理所有构建目录"""
        for builder in self.builders.values():
            builder.clean()
    
    def show_build_results(self, platforms: List[str]):
        """显示构建结果"""
        print("📊 构建结果:")
        print_separator()
        
        dist_path = self.config.get_dist_path()
        
        if not dist_path.exists():
            print("⚠️  构建目录不存在")
            return
        
        # 显示文件列表
        files = list(dist_path.iterdir())
        if not files:
            print("⚠️  没有找到构建文件")
            return
        
        print(f"📁 构建文件位于: {dist_path}")
        print("")
        
        for file in files:
            if file.is_file():
                size = file.stat().st_size
                size_str = self.format_file_size(size)
                print(f"  📄 {file.name} ({size_str})")
            elif file.is_dir() and file.suffix == '.app':
                size = self.get_directory_size(file)
                size_str = self.format_file_size(size)
                print(f"  📦 {file.name} ({size_str})")
        
        print("")
        print("✅ 构建完成！")
    
    def format_file_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def get_directory_size(self, directory: Path) -> int:
        """获取目录大小"""
        total_size = 0
        try:
            for file in directory.rglob('*'):
                if file.is_file():
                    total_size += file.stat().st_size
        except:
            pass
        return total_size

def get_user_choice(prompt, options, default=None, allow_exit=True):
    """获取用户选择"""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        if default is not None and option == default:
            print(f"  {i}. {option} (默认)")
        else:
            print(f"  {i}. {option}")
    
    if allow_exit:
        print(f"  0. 退出")
    
    while True:
        try:
            choice = input(f"请选择 (0-{len(options)}): ").strip()
            if not choice and default is not None:
                return default
            
            choice_num = int(choice)
            if choice_num == 0 and allow_exit:
                return "exit"
            elif 1 <= choice_num <= len(options):
                return options[choice_num - 1]
            else:
                print(f"请输入 0-{len(options)} 之间的数字")
        except ValueError:
            print("请输入有效的数字")

def get_user_confirmation(prompt, default=True, allow_exit=True):
    """获取用户确认"""
    default_str = "Y/n" if default else "y/N"
    exit_hint = " (输入 'exit' 退出)" if allow_exit else ""
    
    while True:
        choice = input(f"{prompt} ({default_str}){exit_hint}: ").strip().lower()
        if not choice:
            return default
        if choice in ['y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
        if choice in ['exit', 'quit', 'q'] and allow_exit:
            return "exit"
        print("请输入 y/yes 或 n/no (或 'exit' 退出)")

def get_current_platform():
    """获取当前操作系统平台"""
    import platform
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return None

def get_current_architecture():
    """获取当前系统架构"""
    import platform
    machine = platform.machine().lower()
    
    if machine in ['x86_64', 'amd64']:
        return 'x64'
    elif machine in ['i386', 'i686']:
        return 'x86'
    elif machine in ['arm64', 'aarch64']:
        return 'arm64'
    elif machine == 'armv7':
        return 'arm'
    else:
        return 'x64'  # 默认回退到 x64

def interactive_build():
    """交互式构建"""
    print("🚀 Apple App Bundle Finder - 交互式构建")
    print_separator()
    manager = BuildManager()
    print_build_info(manager.config)
    
    # 选择构建类型
    build_type = get_user_choice("选择构建类型:", ["应用", "安装包"], default="应用")
    if build_type == "exit":
        print("\n已退出构建程序")
        return
    
    # 选择平台
    platforms = ["windows", "macos", "linux"]
    platform = get_user_choice("选择目标平台:", platforms, default=get_current_platform())
    if platform == "exit":
        print("\n已退出构建程序")
        return
    
    # 选择架构（仅适用于某些平台）
    architectures = ["x64", "x86"]
    if platform == "macos":
        architectures = ["x64", "arm64", "universal"]
    elif platform == "linux":
        architectures = ["x64", "x86", "arm64"]
    
    current_arch = get_current_architecture()
    architecture = get_user_choice("选择架构:", architectures, default=current_arch)
    if architecture == "exit":
        print("\n已退出构建程序")
        return
    
    # 确认构建
    confirm = get_user_confirmation(f"确认构建 {build_type} for {platform} {architecture} 吗?")
    if confirm == "exit":
        print("\n已退出构建程序")
        return
    elif confirm:
        # 创建构建管理器
        manager = BuildManager()
        
        # 执行构建
        try:
            success = manager.run([platform], clean=True)
            if success:
                print(f"\n✅ 构建成功完成!")
            else:
                print(f"\n❌ 构建失败!")
        except Exception as e:
            print(f"\n❌ 构建过程中出现错误: {e}")
    else:
        print("构建已取消")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Apple App Bundle Finder 构建系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python build.py                    # 交互式构建
  python build.py --cli               # 命令行模式
  python build.py -p windows         # 构建 Windows 版本
  python build.py -p macos --installer # 构建 macOS 安装包
  python build.py -p linux -a x64     # 构建 Linux x64 版本
        """
    )
    
    parser.add_argument('-p', '--platform', 
                       choices=['windows', 'macos', 'linux', 'all'],
                       help='目标平台 (默认: 当前平台)')
    parser.add_argument('-i', '--installer', 
                       action='store_true',
                       help='创建安装包')
    parser.add_argument('-a', '--architecture', 
                       choices=['x64', 'x86', 'arm64', 'universal'],
                       default=get_current_architecture(),
                       help=f'架构 (默认: {get_current_architecture()})')
    parser.add_argument('--interactive', 
                       action='store_true', default=True,
                       help='使用交互式模式 (默认)')
    parser.add_argument('--cli', 
                       action='store_true',
                       help='使用命令行模式')
    parser.add_argument('--clean', 
                       action='store_true',
                       help='清理之前的构建文件')
    parser.add_argument('-l', '--list', 
                       action='store_true',
                       help='列出可用平台')
    
    args = parser.parse_args()
    
    try:
        # 列出可用平台
        if args.list:
            print("可用平台:")
            for platform in ["windows", "macos", "linux"]:
                print(f"  - {platform}")
            return
        
        # 交互式模式
        if args.interactive and not args.cli:
            interactive_build()
            return
        
        # 命令行模式
        if not args.platform:
            args.platform = get_current_platform()
        
        if args.platform == 'all':
            platforms = ['windows', 'macos', 'linux']
        else:
            platforms = [args.platform]
        
        manager = BuildManager()
        
        success = True
        for platform in platforms:
            if not manager.build(platform, args.installer, args.architecture, args.clean):
                success = False
                break
        
        if success:
            print(f"\n✅ 构建成功完成!")
        else:
            print(f"\n❌ 构建失败!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作，已退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 构建过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()