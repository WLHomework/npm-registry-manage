"""
NPM源管理器 - 主入口文件
一个现代化的NPM源管理应用程序
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QTranslator, QLocale
from PySide6.QtGui import QFont
from main_window import MainWindow


def setup_application():
    """设置应用程序"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("NPM源管理器")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("NPM Registry Manager")
    app.setOrganizationDomain("npmregistry.manager")
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    
    # 设置全局字体
    font = QFont("Microsoft YaHei UI", 9)
    app.setFont(font)
    
    # 设置应用程序样式表
    app.setStyleSheet("""
        QApplication {
            background-color: #F5F5F5;
        }
        
        QMainWindow {
            background-color: #F5F5F5;
        }
        
        QGroupBox {
            font-weight: 600;
            font-size: 14px;
            color: #333333;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 8px 0 8px;
            background-color: #F5F5F5;
        }
        
        QScrollArea {
            background-color: transparent;
        }
        
        QScrollArea > QWidget > QWidget {
            background-color: transparent;
        }
        
        QMessageBox {
            background-color: white;
        }
        
        QMessageBox QLabel {
            color: #333333;
        }
        
        QMessageBox QPushButton {
            background-color: #007ACC;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 16px;
            font-weight: 500;
            min-width: 60px;
        }
        
        QMessageBox QPushButton:hover {
            background-color: #005A9E;
        }
        
        QMessageBox QPushButton:pressed {
            background-color: #004578;
        }
    """)
    
    return app


def check_dependencies():
    """检查依赖项"""
    import subprocess
    import os
    
    # 检查常见的Node.js安装路径
    possible_paths = [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs", 
        os.path.expanduser("~\\AppData\\Roaming\\npm"),
        os.path.expanduser("~\\scoop\\apps\\nodejs\\current"),
        os.path.expanduser("~\\scoop\\shims")
    ]
    
    # 检查PATH环境变量
    current_path = os.environ.get('PATH', '')
    
    try:
        # 尝试直接运行npm
        result = subprocess.run(
            ["npm", "--version"], 
            capture_output=True, 
            text=True, 
            check=True,
            shell=True  # 在Windows上使用shell
        )
        return True, f"NPM版本: {result.stdout.strip()}"
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        # 如果直接运行失败，尝试查找Node.js安装位置
        found_paths = []
        for path in possible_paths:
            if os.path.exists(path):
                found_paths.append(path)
        
        # 尝试使用完整路径运行npm
        for path in found_paths:
            npm_path = os.path.join(path, "npm.cmd")
            if os.path.exists(npm_path):
                try:
                    result = subprocess.run(
                        [npm_path, "--version"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    # 找到了npm，但PATH可能有问题
                    return False, f"找到NPM (版本: {result.stdout.strip()})，但PATH配置有问题。\n\n请将以下路径添加到系统PATH环境变量：\n{path}\n\n或重启命令行工具后重试。"
                except:
                    continue
        
        # 检查Node.js是否安装
        node_found = False
        for path in found_paths:
            node_path = os.path.join(path, "node.exe")
            if os.path.exists(node_path):
                node_found = True
                break
        
        if node_found:
            return False, f"检测到Node.js已安装，但NPM不可用。\n\n可能的解决方案：\n1. 重新安装Node.js\n2. 检查PATH环境变量\n3. 重启计算机\n\n找到的Node.js路径：\n{chr(10).join(found_paths)}"
        else:
            return False, "未检测到Node.js安装。\n\n请从官网下载并安装Node.js：\nhttps://nodejs.org/\n\n安装完成后重启应用程序。"


def main():
    """主函数"""
    # 创建应用程序
    app = setup_application()
    
    try:
        # 检查依赖项
        deps_ok, deps_msg = check_dependencies()
        if not deps_ok:
            QMessageBox.critical(
                None,
                "依赖检查失败",
                f"{deps_msg}\n\n请安装Node.js和NPM后重试。\n\n下载地址: https://nodejs.org/"
            )
            return 1
        
        # 创建主窗口
        window = MainWindow()
        window.show()
        
        # 显示依赖信息（可选）
        print(f"✓ {deps_msg}")
        print("✓ 应用程序启动成功")
        
        # 运行应用程序
        return app.exec()
        
    except Exception as e:
        QMessageBox.critical(
            None,
            "启动失败",
            f"应用程序启动时发生错误:\n\n{str(e)}\n\n请检查系统环境并重试。"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
