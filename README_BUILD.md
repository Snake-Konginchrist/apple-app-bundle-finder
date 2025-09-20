# 构建系统使用说明

这个构建系统可以将您的应用程序打包成不同操作系统的安装包或可执行文件。基于 PyInstaller 实现，支持 Windows、macOS 和 Linux 平台。

## 目录结构

```
build_scripts/
├── __init__.py          # 包初始化文件
├── config.py            # 构建配置
├── utils.py             # 工具函数
├── base_builder.py      # 基础构建器
├── windows_builder.py   # Windows 构建器
├── macos_builder.py     # macOS 构建器
├── linux_builder.py     # Linux 构建器
└── build_manager.py     # 构建管理器
```

## 使用方法

### 基本用法

```bash
# 构建所有启用的平台
python build.py

# 构建特定平台
python build.py -p windows          # 仅构建 Windows
python build.py -p macos linux       # 构建 macOS 和 Linux

# 清理构建目录
python build.py -c

# 查看可用平台
python build.py -l

# 查看帮助信息
python build.py -h
```

### 配置构建选项

构建配置位于 `build_scripts/config.py` 文件中，包含应用信息、构建选项和平台配置。您可以修改以下设置：

- **应用信息**: 名称、版本、作者、描述
- **构建选项**: onefile/onedir 模式、窗口化、清理选项等
- **平台配置**: 启用/禁用各平台、安装器选项等

如需自定义配置，请编辑 `build_scripts/config.py` 文件中的相关设置。

## 平台特定功能

### Windows
- ✅ 单文件可执行文件 (.exe)
- ✅ NSIS 安装程序
- ✅ 便携版本（包含必要依赖）

### macOS
- ✅ 单文件可执行文件
- ✅ 应用包 (.app) - 使用 onedir 模式构建
- ✅ DMG 安装器

### Linux
- ✅ 单文件可执行文件
- ✅ AppImage (需要 appimage-builder)
- ✅ 压缩包

## 依赖安装

### Python 依赖
```bash
# 使用 pip
pip install pyinstaller pyside6

# 或使用 uv（推荐）
uv sync
```

### 系统依赖

#### Windows
- NSIS (可选，用于创建安装程序)
  - 下载地址: https://nsis.sourceforge.io/
  - 安装后确保 `makensis` 命令在 PATH 中

#### macOS
- Xcode 命令行工具 (必需)
  ```bash
  xcode-select --install
  ```

#### Linux
- appimage-builder (可选，用于创建 AppImage)
  ```bash
  pip install appimage-builder
  ```

## 图标要求

确保在 `assets/` 目录中有相应的图标文件：

- Windows: `logo.ico` (32x32 或 48x48 像素)
- macOS: `logo.icns` (包含多种分辨率)
- Linux: `logo.png` (推荐 256x256 像素)

如果没有图标文件，构建系统会使用默认图标。

## 构建输出

构建完成后，所有输出文件将保存在 `dist/` 目录中：

```
dist/
├── Apple应用Bundle查询器.exe          # Windows 可执行文件
├── Apple应用Bundle查询器_Setup.exe    # Windows 安装程序
├── Apple应用Bundle查询器_Portable/    # Windows 便携版本
├── Apple应用Bundle查询器.app/           # macOS 应用包
├── Apple应用Bundle查询器_macOS.dmg    # macOS 安装器
├── Apple应用Bundle查询器              # Linux 可执行文件
├── Apple应用Bundle查询器-x86_64.AppImage  # Linux AppImage
└── Apple应用Bundle查询器_Linux_x64.tar.gz  # Linux 压缩包
```

## 构建模式说明

### onefile 模式
- 将所有依赖打包到单个可执行文件中
- 启动时会解压依赖到临时目录
- 适用于 Windows 和 Linux 平台

### onedir 模式 (macOS 应用包)
- 将所有文件保留在目录结构中
- 更好的兼容性和启动速度
- 适用于 macOS 应用包构建

## 故障排除

### 常见问题

1. **PyInstaller 未安装**
   ```bash
   pip install pyinstaller
   ```

2. **NSIS 未安装 (Windows)**
   - 下载并安装 NSIS
   - 确保 makensis 命令在 PATH 中

3. **appimage-builder 未安装 (Linux)**
   ```bash
   pip install appimage-builder
   ```

4. **图标文件缺失**
   - 检查 `assets/` 目录中的图标文件
   - 确保图标格式正确

5. **macOS 构建失败**
   - 确保已安装 Xcode 命令行工具
   - 检查是否有足够的磁盘空间

6. **权限问题 (macOS/Linux)**
   ```bash
   chmod +x build.py
   ```

### 获取帮助

```bash
python build.py -h
```

### 调试构建过程

```bash
# 查看详细构建日志
python build.py -v

# 清理后重新构建
python build.py -c && python build.py
```

## 直接使用 PyInstaller 命令

除了使用构建系统，您也可以直接使用 PyInstaller 命令来打包应用程序。以下是针对不同平台和架构的打包方法：

### 基础命令格式

```bash
pyinstaller [选项] main.py
```

### Windows 平台

#### x64 架构（64位）
```bash
# 单文件可执行文件
pyinstaller --onefile --windowed --target-arch=x64 --name="Apple App Bundle Finder" main.py

# 带图标的版本
pyinstaller --onefile --windowed --target-arch=x64 --name="Apple App Bundle Finder" --icon=assets/logo.ico main.py

# 包含数据文件
pyinstaller --onefile --windowed --target-arch=x64 --name="Apple App Bundle Finder" --icon=assets/logo.ico --add-data="assets;assets" --add-data="config;config" main.py
```

#### x86 架构（32位）
```bash
# 需要先安装 32位 Python 环境
pyinstaller --onefile --windowed --target-arch=x86 --name="Apple App Bundle Finder" --icon=assets/logo.ico main.py
```

### macOS 平台

#### Intel 芯片（x86_64）
```bash
# 单文件可执行文件
pyinstaller --onefile --windowed --target-arch=x86_64 --name="Apple App Bundle Finder" --icon=assets/logo.icns main.py

# 应用包格式（推荐）
pyinstaller --onedir --windowed --target-arch=x86_64 --name="Apple App Bundle Finder" --icon=assets/logo.icns main.py
```

#### Apple Silicon（M1/M2 - arm64）
```bash
# 确保使用 arm64 架构的 Python
pyinstaller --onedir --windowed --target-arch=arm64 --name="Apple App Bundle Finder" --icon=assets/logo.icns main.py

# 通用二进制（同时支持 Intel 和 Apple Silicon）
# 需要分别构建两个版本然后合并
pyinstaller --onefile --windowed --target-arch=universal2 --name="Apple App Bundle Finder" --icon=assets/logo.icns main.py
# 然后使用 lipo 命令合并
```

### Linux 平台

#### x86_64 架构
```bash
# 单文件可执行文件
pyinstaller --onefile --windowed --target-arch=x86_64 --name="Apple App Bundle Finder" main.py

# 包含数据文件
pyinstaller --onefile --windowed --target-arch=x86_64 --name="Apple App Bundle Finder" --add-data="assets:assets" --add-data="config:config" main.py
```

#### ARM64 架构
```bash
# 在 ARM64 Linux 系统上
pyinstaller --onefile --windowed --target-arch=aarch64 --name="Apple App Bundle Finder" main.py
```

### 跨平台构建注意事项

#### 1. 平台特定依赖
```bash
# Windows 可能需要
pip install pywin32-ctypes

# macOS 可能需要
pip install py2app

# Linux 可能需要
pip install patchelf
```

#### 2. 隐藏导入
```bash
# 如果 PyInstaller 无法自动检测到某些模块
pyinstaller --onefile --windowed --hidden-import=module_name main.py

# 多个隐藏导入
pyinstaller --onefile --windowed --hidden-import=module1 --hidden-import=module2 main.py
```

#### 3. 排除模块
```bash
# 排除不需要的模块以减小文件大小
pyinstaller --onefile --windowed --exclude-module=tkinter --exclude-module=matplotlib main.py
```

#### 4. 高级选项
```bash
# 指定输出目录
pyinstaller --onefile --windowed --distpath=dist --workpath=build --specpath=. main.py

# 调试模式（保留控制台）
pyinstaller --onefile --name="Apple应用Bundle查询器" main.py

# 清理之前的构建
pyinstaller --onefile --windowed --clean main.py
```

### 验证构建结果

```bash
# 检查生成的可执行文件
file dist/Apple应用Bundle查询器*  # Linux/macOS
# 或
Get-ItemProperty dist/Apple应用Bundle查询器* | Select-Object Name,Length,LastWriteTime  # PowerShell

# 测试运行
./dist/Apple应用Bundle查询器  # Linux/macOS
# 或
.\dist\Apple应用Bundle查询器.exe  # Windows
```

### 常见问题解决

#### 1. 架构不匹配
- 确保使用正确架构的 Python 解释器
- 在 M1 Mac 上，使用 `arch -arm64 python` 或 `arch -x86_64 python`

#### 2. 依赖缺失
```bash
# 查看缺失的依赖
pyinstaller --onefile --windowed --debug=all main.py
```

#### 3. 文件过大
```bash
# 使用 UPX 压缩（可选）
pyinstaller --onefile --windowed --upx-dir=/path/to/upx main.py
```

#### 4. 权限问题（macOS/Linux）
```bash
chmod +x dist/Apple应用Bundle查询器
```

## 高级用法

### 自定义构建脚本

您可以继承基础构建器类来创建自定义的构建逻辑，具体实现请参考构建脚本中的示例。

### 程序化使用

构建系统支持程序化调用，可以：
- 构建特定平台
- 清理构建目录
- 自定义构建参数
- 批量处理多个平台

### 自定义 PyInstaller 参数

如需修改 PyInstaller 的默认参数，可以编辑构建脚本中的相关配置，添加或修改命令行选项。

## 注意事项

1. **macOS 应用包**: 使用 onedir 模式构建，确保所有依赖正确包含
2. **Windows 安装程序**: 需要 NSIS 已安装并配置
3. **Linux AppImage**: 需要 appimage-builder 依赖
4. **构建时间**: macOS 构建 PySide6 应用可能需要较长时间（5-15分钟）
5. **磁盘空间**: 确保有足够的磁盘空间用于构建过程

## 更新日志

- v1.0.0: 初始版本，支持 Windows、macOS、Linux 平台
- 支持 onefile 和 onedir 构建模式
- 自动创建应用包和安装器