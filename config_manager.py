"""
配置管理模块
处理应用程序的配置文件读写和用户偏好设置
"""

import json
import os
from typing import Dict, Any
from pathlib import Path


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".npm-registry-manager"
        self.config_file = self.config_dir / "config.json"
        self.history_file = self.config_dir / "history.json"
        
        # 确保配置目录存在
        self.config_dir.mkdir(exist_ok=True)
        
        # 默认配置
        self.default_config = {
            "auto_test_speed": True,
            "test_timeout": 5,
            "remember_last_registry": True,
            "show_speed_in_list": True,
            "window_geometry": {
                "width": 800,
                "height": 600,
                "x": 100,
                "y": 100
            },
            "custom_registries": []
        }
        
        self.config = self.load_config()
        self.history = self.load_history()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置，确保所有键都存在
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            else:
                return self.default_config.copy()
        except (json.JSONDecodeError, IOError) as e:
            print(f"加载配置文件失败，使用默认配置: {e}")
            return self.default_config.copy()
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def load_history(self) -> Dict[str, Any]:
        """加载历史记录"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    "registry_switches": [],
                    "speed_tests": {},
                    "last_used_registry": None
                }
        except (json.JSONDecodeError, IOError) as e:
            print(f"加载历史记录失败: {e}")
            return {
                "registry_switches": [],
                "speed_tests": {},
                "last_used_registry": None
            }
    
    def save_history(self) -> bool:
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"保存历史记录失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        self.config[key] = value
        self.save_config()
    
    def add_custom_registry(self, name: str, url: str) -> bool:
        """添加自定义源"""
        custom_registries = self.config.get("custom_registries", [])
        
        # 检查是否已存在
        for registry in custom_registries:
            if registry["name"] == name or registry["url"] == url:
                return False
        
        custom_registries.append({"name": name, "url": url})
        self.config["custom_registries"] = custom_registries
        self.save_config()
        return True
    
    def remove_custom_registry(self, name: str) -> bool:
        """移除自定义源"""
        custom_registries = self.config.get("custom_registries", [])
        original_length = len(custom_registries)
        
        self.config["custom_registries"] = [
            registry for registry in custom_registries 
            if registry["name"] != name
        ]
        
        if len(self.config["custom_registries"]) < original_length:
            self.save_config()
            return True
        return False
    
    def get_custom_registries(self) -> list:
        """获取自定义源列表"""
        return self.config.get("custom_registries", [])
    
    def record_registry_switch(self, from_registry: str, to_registry: str) -> None:
        """记录源切换历史"""
        import datetime
        
        switch_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "from": from_registry,
            "to": to_registry
        }
        
        self.history["registry_switches"].append(switch_record)
        
        # 只保留最近100条记录
        if len(self.history["registry_switches"]) > 100:
            self.history["registry_switches"] = self.history["registry_switches"][-100:]
        
        self.history["last_used_registry"] = to_registry
        self.save_history()
    
    def record_speed_test(self, registry_url: str, speed: float, success: bool) -> None:
        """记录速度测试结果"""
        import datetime
        
        if registry_url not in self.history["speed_tests"]:
            self.history["speed_tests"][registry_url] = []
        
        test_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "speed": speed,
            "success": success
        }
        
        self.history["speed_tests"][registry_url].append(test_record)
        
        # 只保留最近10次测试结果
        if len(self.history["speed_tests"][registry_url]) > 10:
            self.history["speed_tests"][registry_url] = self.history["speed_tests"][registry_url][-10:]
        
        self.save_history()
    
    def get_average_speed(self, registry_url: str) -> float:
        """获取源的平均速度"""
        if registry_url not in self.history["speed_tests"]:
            return 0.0
        
        tests = self.history["speed_tests"][registry_url]
        successful_tests = [test["speed"] for test in tests if test["success"]]
        
        if not successful_tests:
            return 0.0
        
        return sum(successful_tests) / len(successful_tests)
    
    def get_window_geometry(self) -> Dict[str, int]:
        """获取窗口几何信息"""
        return self.config.get("window_geometry", self.default_config["window_geometry"])
    
    def save_window_geometry(self, width: int, height: int, x: int, y: int) -> None:
        """保存窗口几何信息"""
        self.config["window_geometry"] = {
            "width": width,
            "height": height,
            "x": x,
            "y": y
        }
        self.save_config()
