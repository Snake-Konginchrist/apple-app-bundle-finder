"""
打包工具模块
提供各种打包相关的工具函数
"""

import shutil
import subprocess
from pathlib import Path

def clean_build_directories(project_root):
    """清理构建目录"""
    print("🧹 清理构建目录...")
    build_dirs = ['build', 'dist', '__pycache__']
    
    for dir_name in build_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  已删除: {dir_path}")
    
    # 清理 Python 缓存文件
    for pycache in project_root.rglob('__pycache__'):
        shutil.rmtree(pycache)
    for pyc in project_root.rglob('*.pyc'):
        pyc.unlink()
    
    print("✅ 清理完成")

def run_command(cmd, cwd=None, capture_output=True, timeout=600):
    """运行命令并返回结果
    
    Args:
        cmd: 命令列表
        cwd: 工作目录
        capture_output: 是否捕获输出
        timeout: 超时时间（秒），默认10分钟
    """
    try:
        result = subprocess.run(cmd, capture_output=capture_output, text=True, cwd=cwd, timeout=timeout)
        if result.returncode != 0 and capture_output:
            print(f"❌ 命令失败: {' '.join(cmd)}")
            print(f"错误信息: {result.stderr}")
        return result
    except subprocess.TimeoutExpired:
        print(f"❌ 命令超时: {' '.join(cmd)}")
        print(f"⏰ 超时时间: {timeout}秒")
        print("💡 建议: 对于大型应用，可以尝试增加超时时间或优化构建配置")
        return None
    except Exception as e:
        print(f"❌ 运行命令出错: {e}")
        return None

def copy_directory(src, dst, ignore_patterns=None):
    """复制目录，支持忽略模式"""
    if ignore_patterns is None:
        ignore_patterns = []
    
    if not src.exists():
        return False
    
    dst.mkdir(parents=True, exist_ok=True)
    
    try:
        for item in src.iterdir():
            # 检查是否应该忽略
            should_ignore = False
            for pattern in ignore_patterns:
                if item.match(pattern):
                    should_ignore = True
                    break
            
            if should_ignore:
                continue
            
            if item.is_dir():
                copy_directory(item, dst / item.name, ignore_patterns)
            else:
                shutil.copy2(item, dst / item.name)
        
        return True
    except Exception as e:
        print(f"❌ 复制目录失败: {e}")
        return False

def create_directory(path):
    """创建目录"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"❌ 创建目录失败: {e}")
        return False

def remove_directory(path):
    """删除目录"""
    try:
        if path.exists():
            shutil.rmtree(path)
        return True
    except Exception as e:
        print(f"❌ 删除目录失败: {e}")
        return False

def get_platform_name():
    """获取当前平台名称"""
    import platform
    system = platform.system().lower()
    
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return system

def check_tool_availability(tool_name):
    """检查工具是否可用"""
    try:
        result = subprocess.run([tool_name, '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def format_file_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_directory_size(directory: Path) -> int:
    """获取目录大小"""
    total_size = 0
    try:
        for file in directory.rglob('*'):
            if file.is_file():
                total_size += file.stat().st_size
    except:
        pass
    return total_size

def print_build_info(config):
    """打印构建信息"""
    print(f"🚀 开始构建 {config.app_name} v{config.version}")
    print(f"👤 作者: {config.author}")
    print(f"📝 描述: {config.description}")
    print_separator()

def print_separator():
    """打印分隔线"""
    print("=" * 50)

def check_dependencies(dependencies, import_check=True):
    """检查依赖"""
    missing = []
    
    for dep in dependencies:
        if import_check:
            # 检查 Python 包
            try:
                # 处理特殊包名
                if dep.lower() == 'pyinstaller':
                    __import__('PyInstaller')
                else:
                    __import__(dep.lower().replace('-', '_'))
            except ImportError:
                missing.append(dep)
        else:
            # 检查系统命令
            if not shutil.which(dep.lower()):
                missing.append(dep)
    
    if missing:
        print(f"⚠️  未找到依赖: {', '.join(missing)}")
        return False
    
    return True