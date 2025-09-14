"""
主窗口模块
应用程序的主界面
"""

import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from npm_manager import NPMRegistryManager
from config_manager import ConfigManager
from ui_components import *


class SpeedTestWorker(QThread):
    """速度测试工作线程"""
    
    result_ready = Signal(str, bool, float)  # url, success, speed
    
    def __init__(self, npm_manager, registries):
        super().__init__()
        self.npm_manager = npm_manager
        self.registries = registries
    
    def run(self):
        """执行速度测试"""
        for name, url in self.registries.items():
            success, speed = self.npm_manager.test_registry_speed(url)
            self.result_ready.emit(url, success, speed)


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.npm_manager = NPMRegistryManager()
        self.config_manager = ConfigManager()
        self.speed_test_worker = None
        self.registry_cards = {}
        
        self.setup_ui()
        self.setup_connections()
        self.load_initial_data()
        self.restore_window_geometry()
    
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("NPM源管理器")
        self.setWindowIcon(QIcon())  # 可以添加图标
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 工具栏
        self.create_toolbar()
        
        # 内容区域
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # 左侧面板
        self.create_left_panel(content_layout)
        
        # 右侧面板
        self.create_right_panel(content_layout)
        
        main_layout.addWidget(content_widget)
        
        # 状态栏
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E0E0E0;
            }
        """)
        toolbar.setFixedHeight(60)
        
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(20, 10, 20, 10)
        
        # 标题
        title_label = QLabel("NPM源管理器")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #333333;
        """)
        toolbar_layout.addWidget(title_label)
        
        toolbar_layout.addStretch()
        
        # 工具按钮
        self.refresh_btn = ModernButton("刷新")
        self.refresh_btn.clicked.connect(self.refresh_data)
        toolbar_layout.addWidget(self.refresh_btn)
        
        self.test_speed_btn = ModernButton("测试速度")
        self.test_speed_btn.clicked.connect(self.test_all_speeds)
        toolbar_layout.addWidget(self.test_speed_btn)
        
        # 将工具栏添加到主布局
        self.centralWidget().layout().insertWidget(0, toolbar)
    
    def create_left_panel(self, parent_layout):
        """创建左侧面板"""
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
            }
        """)
        left_panel.setFixedWidth(350)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(16)
        
        # 当前源信息
        current_group = QGroupBox("当前源信息")
        current_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                color: #333333;
                border: none;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        current_layout = QVBoxLayout(current_group)
        
        self.current_registry_label = QLabel()
        self.current_registry_label.setStyleSheet("""
            background-color: #F8F9FA;
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            padding: 12px;
            font-size: 12px;
            color: #666666;
        """)
        self.current_registry_label.setWordWrap(True)
        current_layout.addWidget(self.current_registry_label)
        
        left_layout.addWidget(current_group)
        
        # 快速操作
        quick_group = QGroupBox("快速操作")
        quick_group.setStyleSheet(current_group.styleSheet())
        
        quick_layout = QVBoxLayout(quick_group)
        
        self.reset_btn = ModernButton("重置为官方源", primary=True)
        self.reset_btn.clicked.connect(self.reset_to_official)
        quick_layout.addWidget(self.reset_btn)
        
        # 自定义源添加
        custom_frame = QFrame()
        custom_layout = QVBoxLayout(custom_frame)
        custom_layout.setContentsMargins(0, 10, 0, 0)
        
        custom_label = QLabel("添加自定义源:")
        custom_label.setStyleSheet("font-weight: 500; color: #333333;")
        custom_layout.addWidget(custom_label)
        
        self.custom_name_input = CustomLineEdit("源名称")
        custom_layout.addWidget(self.custom_name_input)
        
        self.custom_url_input = CustomLineEdit("源URL")
        custom_layout.addWidget(self.custom_url_input)
        
        self.add_custom_btn = ModernButton("添加")
        self.add_custom_btn.clicked.connect(self.add_custom_registry)
        custom_layout.addWidget(self.add_custom_btn)
        
        quick_layout.addWidget(custom_frame)
        left_layout.addWidget(quick_group)
        
        left_layout.addStretch()
        parent_layout.addWidget(left_panel)
    
    def create_right_panel(self, parent_layout):
        """创建右侧面板"""
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
            }
        """)
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(16)
        
        # 标题和加载动画
        header_layout = QHBoxLayout()
        
        sources_label = QLabel("可用源列表")
        sources_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #333333;
        """)
        header_layout.addWidget(sources_label)
        
        header_layout.addStretch()
        
        # 加载动画
        self.loading_spinner = LoadingSpinner(24)
        self.loading_spinner.hide()
        header_layout.addWidget(self.loading_spinner)
        
        right_layout.addLayout(header_layout)
        
        # 源列表滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #F0F0F0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #CCCCCC;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #999999;
            }
        """)
        
        # 源列表容器
        self.registry_container = QWidget()
        self.registry_layout = QVBoxLayout(self.registry_container)
        self.registry_layout.setContentsMargins(0, 0, 0, 0)
        self.registry_layout.setSpacing(12)
        
        scroll_area.setWidget(self.registry_container)
        right_layout.addWidget(scroll_area)
        
        parent_layout.addWidget(right_panel)
    
    def setup_connections(self):
        """设置信号连接"""
        pass
    
    def load_initial_data(self):
        """加载初始数据"""
        try:
            # 更新当前源信息
            self.update_current_registry_info()
            
            # 加载源列表
            self.load_registry_list()
            
            # 更新状态栏
            current_name = self.npm_manager.get_registry_name(self.npm_manager.current_registry)
            self.status_bar.set_current_registry(current_name)
            self.status_bar.set_status("就绪", "success")
            
        except Exception as e:
            self.show_error_message("初始化失败", str(e))
            self.status_bar.set_status(f"初始化失败: {str(e)}", "error")
    
    def update_current_registry_info(self):
        """更新当前源信息"""
        try:
            current_url = self.npm_manager.current_registry
            current_name = self.npm_manager.get_registry_name(current_url)
            
            info_text = f"名称: {current_name}\nURL: {current_url}"
            self.current_registry_label.setText(info_text)
            
        except Exception as e:
            self.current_registry_label.setText(f"获取信息失败: {str(e)}")
    
    def load_registry_list(self):
        """加载源列表"""
        # 清空现有卡片
        for card in self.registry_cards.values():
            card.setParent(None)
        self.registry_cards.clear()
        
        # 获取所有源
        all_registries = self.npm_manager.CHINA_REGISTRIES.copy()
        
        # 添加自定义源
        for custom in self.config_manager.get_custom_registries():
            all_registries[custom["name"]] = custom["url"]
        
        # 创建源卡片
        current_url = self.npm_manager.current_registry
        
        for name, url in all_registries.items():
            is_current = (url == current_url)
            
            # 获取历史平均速度
            avg_speed = self.config_manager.get_average_speed(url)
            speed = avg_speed if avg_speed > 0 else None
            
            card = RegistryCard(name, url, is_current, speed)
            card.clicked.connect(self.switch_registry)
            
            self.registry_cards[url] = card
            self.registry_layout.addWidget(card)
        
        # 添加弹性空间
        self.registry_layout.addStretch()
    
    def switch_registry(self, registry_url):
        """切换源"""
        try:
            old_registry = self.npm_manager.current_registry
            
            self.status_bar.set_status("正在切换源...", "info")
            QApplication.processEvents()
            
            success = self.npm_manager.set_registry(registry_url)
            
            if success:
                # 记录切换历史
                self.config_manager.record_registry_switch(old_registry, registry_url)
                
                # 更新界面
                self.update_current_registry_info()
                self.load_registry_list()
                
                # 更新状态栏
                new_name = self.npm_manager.get_registry_name(registry_url)
                self.status_bar.set_current_registry(new_name)
                self.status_bar.set_status("源切换成功", "success")
                
                self.show_success_message("切换成功", f"已切换到: {new_name}")
            else:
                self.status_bar.set_status("源切换失败", "error")
                
        except Exception as e:
            self.show_error_message("切换失败", str(e))
            self.status_bar.set_status(f"切换失败: {str(e)}", "error")
    
    def test_all_speeds(self):
        """测试所有源的速度"""
        if self.speed_test_worker and self.speed_test_worker.isRunning():
            return
        
        self.test_speed_btn.setEnabled(False)
        self.loading_spinner.start()
        self.status_bar.set_status("正在测试源速度...", "info")
        
        # 获取所有源
        all_registries = self.npm_manager.CHINA_REGISTRIES.copy()
        for custom in self.config_manager.get_custom_registries():
            all_registries[custom["name"]] = custom["url"]
        
        # 启动速度测试线程
        self.speed_test_worker = SpeedTestWorker(self.npm_manager, all_registries)
        self.speed_test_worker.result_ready.connect(self.on_speed_test_result)
        self.speed_test_worker.finished.connect(self.on_speed_test_finished)
        self.speed_test_worker.start()
    
    def on_speed_test_result(self, url, success, speed):
        """处理速度测试结果"""
        # 记录测试结果
        self.config_manager.record_speed_test(url, speed, success)
        
        # 更新对应的卡片
        if url in self.registry_cards:
            card = self.registry_cards[url]
            # 重新创建卡片以更新速度显示
            name = None
            for n, u in self.npm_manager.CHINA_REGISTRIES.items():
                if u == url:
                    name = n
                    break
            
            if not name:
                for custom in self.config_manager.get_custom_registries():
                    if custom["url"] == url:
                        name = custom["name"]
                        break
            
            if name:
                is_current = (url == self.npm_manager.current_registry)
                new_card = RegistryCard(name, url, is_current, speed if success else 0)
                new_card.clicked.connect(self.switch_registry)
                
                # 替换旧卡片
                old_index = self.registry_layout.indexOf(card)
                self.registry_layout.removeWidget(card)
                card.setParent(None)
                self.registry_layout.insertWidget(old_index, new_card)
                self.registry_cards[url] = new_card
    
    def on_speed_test_finished(self):
        """速度测试完成"""
        self.test_speed_btn.setEnabled(True)
        self.loading_spinner.stop()
        self.status_bar.set_status("速度测试完成", "success")
    
    def refresh_data(self):
        """刷新数据"""
        try:
            self.npm_manager.current_registry = self.npm_manager.get_current_registry()
            self.load_initial_data()
        except Exception as e:
            self.show_error_message("刷新失败", str(e))
    
    def reset_to_official(self):
        """重置为官方源"""
        try:
            old_registry = self.npm_manager.current_registry
            success = self.npm_manager.reset_to_default()
            
            if success:
                self.config_manager.record_registry_switch(old_registry, self.npm_manager.CHINA_REGISTRIES["官方源"])
                self.load_initial_data()
                self.show_success_message("重置成功", "已重置为官方源")
            
        except Exception as e:
            self.show_error_message("重置失败", str(e))
    
    def add_custom_registry(self):
        """添加自定义源"""
        name = self.custom_name_input.text().strip()
        url = self.custom_url_input.text().strip()
        
        if not name or not url:
            self.show_warning_message("输入错误", "请填写完整的源名称和URL")
            return
        
        if not self.npm_manager.validate_registry_url(url):
            self.show_warning_message("URL错误", "请输入有效的源URL")
            return
        
        if self.config_manager.add_custom_registry(name, url):
            self.custom_name_input.clear()
            self.custom_url_input.clear()
            self.load_registry_list()
            self.show_success_message("添加成功", f"自定义源 '{name}' 已添加")
        else:
            self.show_warning_message("添加失败", "源名称或URL已存在")
    
    
    def show_success_message(self, title, message):
        """显示成功消息"""
        QMessageBox.information(self, title, message)
    
    def show_error_message(self, title, message):
        """显示错误消息"""
        QMessageBox.critical(self, title, message)
    
    def show_warning_message(self, title, message):
        """显示警告消息"""
        QMessageBox.warning(self, title, message)
    
    def show_info_message(self, title, message):
        """显示信息消息"""
        QMessageBox.information(self, title, message)
    
    def restore_window_geometry(self):
        """恢复窗口几何信息"""
        geometry = self.config_manager.get_window_geometry()
        self.resize(geometry["width"], geometry["height"])
        self.move(geometry["x"], geometry["y"])
    
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 保存窗口几何信息
        geometry = self.geometry()
        self.config_manager.save_window_geometry(
            geometry.width(),
            geometry.height(),
            geometry.x(),
            geometry.y()
        )
        
        # 停止速度测试线程
        if self.speed_test_worker and self.speed_test_worker.isRunning():
            self.speed_test_worker.terminate()
            self.speed_test_worker.wait()
        
        event.accept()
