"""
简单的NPM环境测试脚本
"""

import subprocess
import os
from pathlib import Path

def test_npm_environment():
    """测试NPM环境"""
    print("正在检测NPM环境...")
    
    # 方法1: 直接运行npm
    try:
        result = subprocess.run(
            ["npm", "--version"], 
            capture_output=True, 
            text=True, 
            shell=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✓ NPM可用，版本: {result.stdout.strip()}")
            return True, "npm"
        else:
            print(f"✗ NPM命令失败: {result.stderr}")
    except Exception as e:
        print(f"✗ NPM命令异常: {e}")
    
    # 方法2: 尝试npm.cmd
    try:
        result = subprocess.run(
            ["npm.cmd", "--version"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✓ NPM.CMD可用，版本: {result.stdout.strip()}")
            return True, "npm.cmd"
        else:
            print(f"✗ NPM.CMD命令失败: {result.stderr}")
    except Exception as e:
        print(f"✗ NPM.CMD命令异常: {e}")
    
    # 方法3: 查找Node.js安装路径
    print("\n正在查找Node.js安装路径...")
    possible_paths = [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs",
        Path.home() / "AppData" / "Roaming" / "npm"
    ]
    
    for path in possible_paths:
        path = Path(path)
        if path.exists():
            print(f"找到路径: {path}")
            npm_cmd = path / "npm.cmd"
            if npm_cmd.exists():
                try:
                    result = subprocess.run(
                        [str(npm_cmd), "--version"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        print(f"✓ 找到可用的NPM: {npm_cmd}")
                        print(f"  版本: {result.stdout.strip()}")
                        return True, str(npm_cmd)
                except Exception as e:
                    print(f"✗ 测试失败: {e}")
    
    print("\n✗ 未找到可用的NPM命令")
    return False, None

def test_current_registry(npm_cmd):
    """测试获取当前源"""
    try:
        result = subprocess.run(
            [npm_cmd, "config", "get", "registry"],
            capture_output=True,
            text=True,
            shell=True,
            timeout=10
        )
        if result.returncode == 0:
            registry = result.stdout.strip()
            print(f"✓ 当前NPM源: {registry}")
            return registry
        else:
            print(f"✗ 获取源失败: {result.stderr}")
    except Exception as e:
        print(f"✗ 获取源异常: {e}")
    return None

if __name__ == "__main__":
    success, npm_cmd = test_npm_environment()
    
    if success:
        print(f"\n使用命令: {npm_cmd}")
        registry = test_current_registry(npm_cmd)
        
        if registry:
            print(f"\n✓ NPM环境正常，可以运行主应用程序")
        else:
            print(f"\n⚠ NPM命令可用，但获取配置失败")
    else:
        print(f"\n✗ NPM环境有问题，请检查Node.js安装")
        print("建议:")
        print("1. 重新安装Node.js (https://nodejs.org/)")
        print("2. 安装时选择'Add to PATH'选项")
        print("3. 重启计算机后重试")
    
    input("\n按回车键退出...")
