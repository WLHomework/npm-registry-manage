"""
NPM环境诊断工具
用于诊断和解决NPM环境配置问题
"""

import os
import subprocess
import sys
from pathlib import Path


def check_node_installations():
    """检查Node.js安装情况"""
    print("=== Node.js 安装检查 ===")
    
    # 常见安装路径
    possible_paths = [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs",
        Path.home() / "AppData" / "Roaming" / "npm",
        Path.home() / "scoop" / "apps" / "nodejs" / "current",
        Path.home() / "scoop" / "shims",
        r"C:\tools\nodejs",
        r"D:\Program Files\nodejs",
        r"D:\nodejs"
    ]
    
    found_installations = []
    
    for path in possible_paths:
        path = Path(path)
        if path.exists():
            node_exe = path / "node.exe"
            npm_cmd = path / "npm.cmd"
            
            print(f"✓ 找到安装目录: {path}")
            
            if node_exe.exists():
                print(f"  - node.exe: 存在")
                try:
                    result = subprocess.run([str(node_exe), "--version"], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print(f"  - Node.js版本: {result.stdout.strip()}")
                    else:
                        print(f"  - Node.js版本检查失败")
                except Exception as e:
                    print(f"  - Node.js版本检查错误: {e}")
            else:
                print(f"  - node.exe: 不存在")
            
            if npm_cmd.exists():
                print(f"  - npm.cmd: 存在")
                try:
                    result = subprocess.run([str(npm_cmd), "--version"], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print(f"  - NPM版本: {result.stdout.strip()}")
                        found_installations.append(str(path))
                    else:
                        print(f"  - NPM版本检查失败")
                except Exception as e:
                    print(f"  - NPM版本检查错误: {e}")
            else:
                print(f"  - npm.cmd: 不存在")
            
            print()
    
    return found_installations


def check_path_environment():
    """检查PATH环境变量"""
    print("=== PATH 环境变量检查 ===")
    
    path_env = os.environ.get('PATH', '')
    path_dirs = path_env.split(os.pathsep)
    
    nodejs_paths = []
    for path_dir in path_dirs:
        if 'node' in path_dir.lower():
            nodejs_paths.append(path_dir)
            print(f"✓ PATH中的Node.js相关路径: {path_dir}")
    
    if not nodejs_paths:
        print("✗ PATH中未找到Node.js相关路径")
    
    print()
    return nodejs_paths


def test_npm_commands():
    """测试NPM命令"""
    print("=== NPM 命令测试 ===")
    
    commands_to_test = [
        ["npm", "--version"],
        ["npm.cmd", "--version"],
        ["node", "--version"],
        ["node.exe", "--version"]
    ]
    
    working_commands = []
    
    for cmd in commands_to_test:
        try:
            print(f"测试命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  timeout=10, shell=True)
            if result.returncode == 0:
                print(f"✓ 成功: {result.stdout.strip()}")
                working_commands.append(cmd)
            else:
                print(f"✗ 失败: {result.stderr.strip()}")
        except FileNotFoundError:
            print(f"✗ 命令未找到: {' '.join(cmd)}")
        except subprocess.TimeoutExpired:
            print(f"✗ 命令超时: {' '.join(cmd)}")
        except Exception as e:
            print(f"✗ 错误: {e}")
        print()
    
    return working_commands


def generate_fix_suggestions(found_installations, working_commands):
    """生成修复建议"""
    print("=== 修复建议 ===")
    
    if working_commands:
        print("✓ NPM命令可以正常使用，应用程序应该能够正常运行。")
        return
    
    if found_installations:
        print("发现Node.js安装，但命令行无法访问。建议:")
        print("1. 将以下路径添加到系统PATH环境变量:")
        for path in found_installations:
            print(f"   {path}")
        print("\n2. 添加PATH的步骤:")
        print("   - 右键'此电脑' -> 属性 -> 高级系统设置")
        print("   - 点击'环境变量'")
        print("   - 在'系统变量'中找到'Path'，点击'编辑'")
        print("   - 点击'新建'，添加Node.js路径")
        print("   - 确定保存，重启命令行")
        
        print("\n3. 或者重新安装Node.js并选择'Add to PATH'选项")
    else:
        print("未找到Node.js安装。建议:")
        print("1. 从官网下载Node.js: https://nodejs.org/")
        print("2. 选择LTS版本")
        print("3. 安装时确保勾选'Add to PATH'选项")
        print("4. 安装完成后重启计算机")


def main():
    """主诊断函数"""
    print("NPM环境诊断工具")
    print("=" * 50)
    
    # 检查Node.js安装
    found_installations = check_node_installations()
    
    # 检查PATH环境变量
    check_path_environment()
    
    # 测试NPM命令
    working_commands = test_npm_commands()
    
    # 生成修复建议
    generate_fix_suggestions(found_installations, working_commands)
    
    print("\n诊断完成!")
    input("按回车键退出...")


if __name__ == "__main__":
    main()
