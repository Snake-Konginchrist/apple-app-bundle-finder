"""
Windows 构建器模块
专门处理 Windows 平台的构建任务
"""

import shutil

from .base_builder import BaseBuilder
from .utils import run_command


class WindowsBuilder(BaseBuilder):
    """Windows 构建器"""
    
    def __init__(self):
        super().__init__()
        self.platform_name = "windows"
    
    def build(self):
        """构建 Windows 版本"""
        print("🔨 开始构建 Windows 版本...")
        
        # 构建可执行文件
        if not self.build_executable(self.platform_name):
            return False
        
        # 创建安装程序
        self.create_installer()
        
        # 创建便携版本
        self.create_portable_version()
        
        print("✅ Windows 版本构建完成")
        return True
    
    def create_installer(self):
        """创建 Windows 安装程序"""
        print("📦 创建 Windows 安装程序...")
        
        # 检查 NSIS 是否可用
        if not self.check_nsis():
            print("⚠️  NSIS 未安装，跳过安装程序创建")
            print("   您可以手动安装 NSIS 或下载安装程序")
            return
        
        # 创建 NSIS 脚本
        nsis_script = self.create_nsis_script()
        script_path = self.project_root / "installer.nsi"
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(nsis_script)
        
        # 运行 NSIS
        result = run_command(['makensis', str(script_path)], cwd=self.project_root)
        
        # 清理临时文件
        if script_path.exists():
            script_path.unlink()
        
        if result and result.returncode == 0:
            print("✅ Windows 安装程序创建成功")
        else:
            print("⚠️  Windows 安装程序创建失败")
    
    def create_nsis_script(self):
        """创建 NSIS 脚本"""
        return f"""
!define APP_NAME "{self.app_name}"
!define APP_VERSION "{self.config.version}"
!define APP_PUBLISHER "{self.config.author}"
!define APP_DESCRIPTION "{self.config.description}"
!define APP_EXE "{self.app_name}.exe"

Name "${{APP_NAME}}"
OutFile "..\\dist\\{self.app_name}_Setup.exe"
InstallDir "$PROGRAMFILES\\{self.app_name}"
InstallDirRegKey HKLM "Software\\{self.app_name}" "Install_Dir"
RequestExecutionLevel admin

; 包含现代界面
!include "MUI2.nsh"

; 界面设置
!define MUI_ABORTWARNING
!define MUI_ICON "..\\assets\\logo.ico"
!define MUI_UNICON "..\\assets\\logo.ico"

; 页面
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; 语言
!insertmacro MUI_LANGUAGE "SimpChinese"
!insertmacro MUI_LANGUAGE "English"

Section "{self.app_name}"
    SetOutPath "$INSTDIR"
    
    ; 复制主程序
    File "..\\dist\\${{APP_EXE}}"
    
    ; 复制资源文件
    SetOutPath "$INSTDIR\\assets"
    File /r "..\\assets\\*.*"
    
    SetOutPath "$INSTDIR\\config"
    File /r "..\\config\\*.*"
    
    ; 创建快捷方式
    CreateDirectory "$SMPROGRAMS\\{self.app_name}"
    CreateShortcut "$SMPROGRAMS\\{self.app_name}\\{self.app_name}.lnk" "$INSTDIR\\${{APP_EXE}}" "" "$INSTDIR\\assets\\logo.ico"
    CreateShortcut "$DESKTOP\\{self.app_name}.lnk" "$INSTDIR\\${{APP_EXE}}" "" "$INSTDIR\\assets\\logo.ico"
    
    ; 写入注册表
    WriteRegStr HKLM "Software\\{self.app_name}" "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.app_name}" "DisplayName" "{self.app_name}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.app_name}" "UninstallString" '"$INSTDIR\\uninstall.exe"'
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.app_name}" "DisplayIcon" "$INSTDIR\\assets\\logo.ico"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.app_name}" "Publisher" "{self.config.author}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.app_name}" "DisplayVersion" "{self.config.version}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.app_name}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.app_name}" "NoRepair" 1
    WriteUninstaller "uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\*.*"
    RMDir /r "$INSTDIR"
    Delete "$SMPROGRAMS\\{self.app_name}\\*.*"
    RMDir "$SMPROGRAMS\\{self.app_name}"
    Delete "$DESKTOP\\{self.app_name}.lnk"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.app_name}"
    DeleteRegKey HKLM "Software\\{self.app_name}"
SectionEnd
"""
    
    def create_portable_version(self):
        """创建便携版本"""
        print("📁 创建便携版本...")
        
        dist_path = self.config.get_dist_path()
        portable_dir = dist_path / f"{self.app_name}_Portable"
        
        # 删除已存在的便携目录
        if portable_dir.exists():
            shutil.rmtree(portable_dir)
        
        # 创建便携目录
        portable_dir.mkdir(exist_ok=True)
        
        # 复制可执行文件
        exe_path = self.get_executable_path(self.platform_name)
        if exe_path.exists():
            shutil.copy2(exe_path, portable_dir / exe_path.name)
        
        # 复制资源文件
        assets_dir = portable_dir / "assets"
        if (self.project_root / "assets").exists():
            shutil.copytree(self.project_root / "assets", assets_dir, dirs_exist_ok=True)
        
        config_dir = portable_dir / "config"
        if (self.project_root / "config").exists():
            shutil.copytree(self.project_root / "config", config_dir, dirs_exist_ok=True)
        
        # 创建说明文件
        readme_content = f"""{self.app_name} - 便携版本

版本: {self.config.version}
作者: {self.config.author}

使用方法:
1. 解压本压缩包到任意目录
2. 运行 {self.app_name}.exe
3. 无需安装，可直接使用

注意事项:
- 本程序为绿色软件，不会在系统中留下任何痕迹
- 所有配置和数据都保存在程序所在目录
- 删除整个目录即可完全卸载
"""
        
        with open(portable_dir / "README.txt", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ 便携版本创建完成")
    
    def check_nsis(self):
        """检查 NSIS 是否可用"""
        try:
            result = run_command(['makensis', '-VERSION'])
            return result is not None and result.returncode == 0
        except:
            return False