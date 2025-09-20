#!/usr/bin/env python3
"""
构建脚本入口点
使用说明:
    python build.py                    # 构建所有启用的平台
    python build.py -p windows         # 仅构建 Windows 版本
    python build.py -p macos linux     # 构建 macOS 和 Linux 版本
    python build.py -c                 # 清理构建目录
    python build.py -l                 # 列出可用平台
"""

from build_scripts.build_manager import main

if __name__ == "__main__":
    main()