"""
UI组件模块
定义应用程序的各种UI组件和样式
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class ModernButton(QPushButton):
    """现代化按钮组件"""
    
    def __init__(self, text="", icon=None, primary=False):
        super().__init__(text)
        self.primary = primary
        self.setup_style()
        
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(16, 16))
    
    def setup_style(self):
        """设置按钮样式"""
        if self.primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #007ACC;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 500;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #005A9E;
                }
                QPushButton:pressed {
                    background-color: #004578;
                }
                QPushButton:disabled {
                    background-color: #CCCCCC;
                    color: #666666;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #F3F3F3;
                    color: #333333;
                    border: 1px solid #CCCCCC;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #E8E8E8;
                    border-color: #999999;
                }
                QPushButton:pressed {
                    background-color: #DDDDDD;
                }
                QPushButton:disabled {
                    background-color: #F9F9F9;
                    color: #CCCCCC;
                    border-color: #E0E0E0;
                }
            """)


class RegistryCard(QFrame):
    """源信息卡片组件"""
    
    clicked = Signal(str)  # 发送源URL信号
    
    def __init__(self, name, url, is_current=False, speed=None):
        super().__init__()
        self.name = name
        self.url = url
        self.is_current = is_current
        self.speed = speed
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # 顶部行：名称和状态
        top_layout = QHBoxLayout()
        
        # 源名称
        name_label = QLabel(self.name)
        name_label.setStyleSheet("font-weight: 600; font-size: 14px; color: #333333;")
        top_layout.addWidget(name_label)
        
        top_layout.addStretch()
        
        # 当前源标识
        if self.is_current:
            current_label = QLabel("当前")
            current_label.setStyleSheet("""
                background-color: #28A745;
                color: white;
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 11px;
                font-weight: 500;
            """)
            top_layout.addWidget(current_label)
        
        layout.addLayout(top_layout)
        
        # URL
        url_label = QLabel(self.url)
        url_label.setStyleSheet("color: #666666; font-size: 12px;")
        url_label.setWordWrap(True)
        layout.addWidget(url_label)
        
        # 底部行：速度信息和操作按钮
        bottom_layout = QHBoxLayout()
        
        # 速度信息
        if self.speed is not None:
            if self.speed > 0:
                speed_text = f"响应时间: {self.speed}ms"
                color = "#28A745" if self.speed < 1000 else "#FFC107" if self.speed < 3000 else "#DC3545"
            else:
                speed_text = "连接失败"
                color = "#DC3545"
            
            speed_label = QLabel(speed_text)
            speed_label.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: 500;")
            bottom_layout.addWidget(speed_label)
        
        bottom_layout.addStretch()
        
        # 操作按钮
        if not self.is_current:
            switch_btn = ModernButton("切换", primary=True)
            switch_btn.clicked.connect(lambda: self.clicked.emit(self.url))
            switch_btn.setFixedSize(60, 28)
            bottom_layout.addWidget(switch_btn)
        
        layout.addLayout(bottom_layout)
    
    def setup_style(self):
        """设置卡片样式"""
        border_color = "#007ACC" if self.is_current else "#E0E0E0"
        background_color = "#F8F9FA" if self.is_current else "#FFFFFF"
        
        self.setStyleSheet(f"""
            RegistryCard {{
                background-color: {background_color};
                border: 2px solid {border_color};
                border-radius: 8px;
            }}
            RegistryCard:hover {{
                border-color: #007ACC;
                background-color: #F8F9FA;
            }}
        """)
        
        self.setCursor(Qt.PointingHandCursor)
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton and not self.is_current:
            self.clicked.emit(self.url)
        super().mousePressEvent(event)


class StatusBar(QFrame):
    """状态栏组件"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI布局"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        
        # 状态图标
        self.status_icon = QLabel()
        self.status_icon.setFixedSize(16, 16)
        layout.addWidget(self.status_icon)
        
        # 状态文本
        self.status_text = QLabel("就绪")
        self.status_text.setStyleSheet("color: #666666; font-size: 12px;")
        layout.addWidget(self.status_text)
        
        layout.addStretch()
        
        # 当前源信息
        self.current_registry_label = QLabel()
        self.current_registry_label.setStyleSheet("color: #333333; font-size: 12px; font-weight: 500;")
        layout.addWidget(self.current_registry_label)
    
    def setup_style(self):
        """设置状态栏样式"""
        self.setStyleSheet("""
            StatusBar {
                background-color: #F8F9FA;
                border-top: 1px solid #E0E0E0;
            }
        """)
        self.setFixedHeight(40)
    
    def set_status(self, text, status_type="info"):
        """设置状态信息"""
        self.status_text.setText(text)
        
        # 设置状态图标和颜色
        colors = {
            "info": "#17A2B8",
            "success": "#28A745",
            "warning": "#FFC107",
            "error": "#DC3545"
        }
        
        color = colors.get(status_type, "#17A2B8")
        self.status_text.setStyleSheet(f"color: {color}; font-size: 12px;")
        
        # 这里可以添加图标设置逻辑
    
    def set_current_registry(self, registry_name):
        """设置当前源信息"""
        self.current_registry_label.setText(f"当前源: {registry_name}")


class LoadingSpinner(QWidget):
    """加载动画组件"""
    
    def __init__(self, size=32):
        super().__init__()
        self.size = size
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.setFixedSize(size, size)
    
    def start(self):
        """开始动画"""
        self.timer.start(50)  # 50ms间隔
        self.show()
    
    def stop(self):
        """停止动画"""
        self.timer.stop()
        self.hide()
    
    def rotate(self):
        """旋转动画"""
        self.angle = (self.angle + 10) % 360
        self.update()
    
    def paintEvent(self, event):
        """绘制加载动画"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 设置画笔
        pen = QPen(QColor("#007ACC"))
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        # 绘制圆弧
        rect = QRect(3, 3, self.size - 6, self.size - 6)
        painter.drawArc(rect, self.angle * 16, 120 * 16)


class CustomComboBox(QComboBox):
    """自定义下拉框"""
    
    def __init__(self):
        super().__init__()
        self.setup_style()
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
                min-height: 20px;
            }
            QComboBox:hover {
                border-color: #007ACC;
            }
            QComboBox:focus {
                border-color: #007ACC;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                selection-background-color: #E3F2FD;
                outline: none;
            }
        """)


class CustomLineEdit(QLineEdit):
    """自定义输入框"""
    
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setup_style()
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:hover {
                border-color: #007ACC;
            }
            QLineEdit:focus {
                border-color: #007ACC;
                outline: none;
            }
        """)
