"""
NPM源管理核心模块
提供npm源的查看、切换、测试等功能
"""

import subprocess
import json
import time
import requests
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class NPMRegistryManager:
    """NPM源管理器"""
    
    # 预定义的中国源列表
    CHINA_REGISTRIES = {
        "淘宝源": "https://registry.npmmirror.com/",
        "腾讯源": "https://mirrors.cloud.tencent.com/npm/",
        "华为源": "https://mirrors.huaweicloud.com/repository/npm/",
        "网易源": "https://mirrors.163.com/npm/",
        "中科大源": "https://npmreg.proxy.ustclug.org/",
        "官方源": "https://registry.npmjs.org/"
    }
    
    def __init__(self):
        self.npm_command = self._find_npm_command()
        self.current_registry = self.get_current_registry()
    
    def _find_npm_command(self) -> str:
        """查找可用的NPM命令"""
        # 常见的NPM命令路径
        possible_commands = ["npm", "npm.cmd"]
        
        # 常见的Node.js安装路径
        possible_paths = [
            r"C:\Program Files\nodejs",
            r"C:\Program Files (x86)\nodejs",
            Path.home() / "AppData" / "Roaming" / "npm",
            Path.home() / "scoop" / "apps" / "nodejs" / "current",
            Path.home() / "scoop" / "shims"
        ]
        
        # 首先尝试直接命令
        for cmd in possible_commands:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True, 
                                      timeout=5, shell=True)
                if result.returncode == 0:
                    return cmd
            except:
                continue
        
        # 如果直接命令失败，尝试完整路径
        for path in possible_paths:
            path = Path(path)
            if path.exists():
                for cmd in ["npm.cmd", "npm"]:
                    npm_path = path / cmd
                    if npm_path.exists():
                        try:
                            result = subprocess.run([str(npm_path), "--version"],
                                                  capture_output=True, text=True, timeout=5)
                            if result.returncode == 0:
                                return str(npm_path)
                        except:
                            continue
        
        raise Exception("未找到可用的NPM命令")
    
    def get_current_registry(self) -> str:
        """获取当前npm源"""
        try:
            result = subprocess.run(
                [self.npm_command, "config", "get", "registry"],
                capture_output=True,
                text=True,
                check=True,
                shell=True  # Windows环境下使用shell
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"获取当前npm源失败: {e}")
        except FileNotFoundError:
            raise Exception("未找到npm命令，请确保已安装Node.js和npm")
    
    def set_registry(self, registry_url: str) -> bool:
        """设置npm源"""
        try:
            subprocess.run(
                [self.npm_command, "config", "set", "registry", registry_url],
                capture_output=True,
                text=True,
                check=True,
                shell=True  # Windows环境下使用shell
            )
            self.current_registry = registry_url
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"设置npm源失败: {e}")
    
    def test_registry_speed(self, registry_url: str, timeout: int = 5) -> Tuple[bool, float]:
        """测试源的响应速度"""
        try:
            start_time = time.time()
            response = requests.get(registry_url, timeout=timeout)
            end_time = time.time()
            
            if response.status_code == 200:
                return True, round((end_time - start_time) * 1000, 2)  # 返回毫秒
            else:
                return False, 0.0
        except requests.RequestException:
            return False, 0.0
    
    def get_registry_info(self, registry_url: str) -> Dict:
        """获取源的详细信息"""
        try:
            response = requests.get(registry_url, timeout=5)
            if response.status_code == 200:
                # 尝试获取一些基本信息
                test_package_url = f"{registry_url.rstrip('/')}/vue"
                package_response = requests.get(test_package_url, timeout=5)
                
                return {
                    "status": "可用",
                    "response_code": response.status_code,
                    "can_fetch_packages": package_response.status_code == 200
                }
            else:
                return {
                    "status": "不可用",
                    "response_code": response.status_code,
                    "can_fetch_packages": False
                }
        except requests.RequestException as e:
            return {
                "status": "连接失败",
                "error": str(e),
                "can_fetch_packages": False
            }
    
    def get_npm_config(self) -> Dict:
        """获取npm配置信息"""
        try:
            result = subprocess.run(
                [self.npm_command, "config", "list", "--json"],
                capture_output=True,
                text=True,
                check=True,
                shell=True  # Windows环境下使用shell
            )
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            raise Exception(f"获取npm配置失败: {e}")
    
    def reset_to_default(self) -> bool:
        """重置到默认官方源"""
        return self.set_registry(self.CHINA_REGISTRIES["官方源"])
    
    def get_registry_name(self, registry_url: str) -> str:
        """根据URL获取源名称"""
        for name, url in self.CHINA_REGISTRIES.items():
            if url == registry_url:
                return name
        return "自定义源"
    
    def validate_registry_url(self, url: str) -> bool:
        """验证源URL格式"""
        if not url.startswith(('http://', 'https://')):
            return False
        if not url.endswith('/'):
            url += '/'
        try:
            response = requests.head(url, timeout=5)
            return response.status_code < 400
        except requests.RequestException:
            return False
