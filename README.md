# NPM源管理器

一个功能完善、界面现代化的NPM源管理应用程序，使用Python和PySide6开发。

## 功能特性

### 🚀 核心功能
- **一键切换NPM源** - 支持国内主流镜像源，快速切换
- **源速度测试** - 实时测试各源的响应速度，找到最快源
- **自定义源管理** - 添加和管理个人自定义NPM源
- **配置持久化** - 自动保存用户配置和使用历史
- **智能路径检测** - 自动查找NPM安装路径，解决环境问题

### 🎨 界面特性
- **现代化UI设计** - 基于PySide6的美观界面，卡片式布局
- **响应式布局** - 适配不同屏幕尺寸，支持窗口缩放
- **实时状态反馈** - 清晰的操作状态提示和进度显示

### 📊 数据管理
- **使用历史记录** - 记录源切换历史，可追溯操作
- **速度统计** - 保存历史测速数据，提供平均速度
- **智能推荐** - 基于速度数据推荐最优源

## 预置源列表

| 源名称 | URL | 说明 |
|--------|-----|------|
| 淘宝源 | https://registry.npmmirror.com/ | 阿里巴巴镜像 |
| 腾讯源 | https://mirrors.cloud.tencent.com/npm/ | 腾讯云镜像 |
| 华为源 | https://mirrors.huaweicloud.com/repository/npm/ | 华为云镜像 |
| 网易源 | https://mirrors.163.com/npm/ | 网易镜像 |
| 中科大源 | https://npmreg.proxy.ustclug.org/ | 中科大镜像 |
| 官方源 | https://registry.npmjs.org/ | NPM官方源 |

## 安装要求

### 系统要求
- Windows 10/11
- Python 3.8+
- Node.js 和 NPM

### Python依赖
```
PySide6>=6.5.0
requests>=2.31.0
configparser>=5.3.0
```

## 安装步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd npm-registry-manage
```

### 2. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 3. 确保NPM可用
```bash
npm --version
```

### 4. 运行应用程序
```bash
python main.py
```

## 使用指南

### 启动应用
双击 `main.py` 或在命令行中运行：
```bash
python main.py
```

### 基本操作

#### 查看当前源
- 应用启动后，左侧面板显示当前NPM源信息
- 状态栏显示当前使用的源名称

#### 切换源
1. 在右侧源列表中选择目标源
2. 点击源卡片上的"切换"按钮
3. 等待切换完成提示

#### 测试源速度
1. 点击工具栏的"测试速度"按钮
2. 应用将测试所有源的响应速度
3. 结果显示在各源卡片上

#### 添加自定义源
1. 在左侧面板的"快速操作"区域
2. 输入源名称和URL
3. 点击"添加"按钮

#### 重置为官方源
- 点击左侧面板的"重置为官方源"按钮

## 项目结构

```
npm-registry-manage/
├── main.py                 # 主入口文件
├── main_window.py          # 主窗口界面
├── npm_manager.py          # NPM源管理核心模块
├── config_manager.py       # 配置管理模块
├── ui_components.py        # UI组件模块
├── diagnose.py            # 环境诊断工具
├── test_npm.py            # NPM环境测试脚本
├── requirements.txt        # Python依赖列表
└── README.md              # 项目说明文档
```

## 配置文件

应用程序会在用户目录下创建配置文件夹：
```
~/.npm-registry-manager/
├── config.json            # 应用配置
└── history.json           # 使用历史
```

### 配置选项
- `auto_test_speed`: 自动测试速度
- `test_timeout`: 测试超时时间 (秒)
- `remember_last_registry`: 记住最后使用的源
- `custom_registries`: 自定义源列表
- `show_speed_in_list`: 在源列表中显示速度

## 开发说明

### 模块说明

#### npm_manager.py
- `NPMRegistryManager`: 核心管理类
- 提供源切换、速度测试、信息获取等功能

#### config_manager.py
- `ConfigManager`: 配置管理类
- 处理配置文件读写和历史记录

#### ui_components.py
- 自定义UI组件
- 现代化的按钮、卡片、输入框等

#### main_window.py
- `MainWindow`: 主窗口类
- 整合所有功能模块的用户界面

#### diagnose.py
- NPM环境诊断工具
- 自动检测Node.js和NPM安装
- 提供详细的修复建议

### 扩展开发

#### 添加新的源
在 `npm_manager.py` 的 `CHINA_REGISTRIES` 字典中添加：
```python
"新源名称": "https://new-registry-url/"
```

#### 自定义UI样式
修改 `ui_components.py` 中的样式表定义

#### 添加新功能
1. 在对应模块中实现功能逻辑
2. 在 `main_window.py` 中添加UI交互
3. 更新配置管理支持新选项

## 故障排除

### 常见问题

#### NPM命令未找到
**问题**: 启动时提示"未找到NPM命令"
**解决**: 
1. 运行诊断工具：`python diagnose.py`
2. 确保已安装Node.js并添加到PATH
3. 重新安装Node.js时勾选"Add to PATH"选项
4. 重启计算机后重试

#### 源切换失败
**问题**: 点击切换后提示失败
**解决**:
1. 检查网络连接和防火墙设置
2. 确认目标源URL有效性
3. 尝试使用代理服务器
4. 以管理员权限运行应用程序

#### 界面显示异常
**问题**: UI界面显示不正常
**解决**:
1. 更新PySide6到最新版本
2. 在设置中调整字体大小
3. 切换主题或重置窗口配置
4. 检查系统显示缩放设置

#### 速度测试失败
**问题**: 源速度测试总是失败
**解决**:
1. 在设置中增加测试超时时间
2. 减少并发测试数量
3. 检查网络连接稳定性
4. 配置代理服务器

#### 配置文件损坏
**问题**: 应用启动时配置加载失败
**解决**:
1. 删除配置文件夹 `~/.npm-registry-manager`
2. 重启应用程序自动重建配置
3. 从备份导入配置文件

### 环境诊断工具
运行诊断工具检查NPM环境：
```bash
python diagnose.py
```

### 测试NPM环境
运行简单测试脚本：
```bash
python test_npm.py
```

### 调试模式
启用调试模式获取详细信息：
1. 打开设置 → 高级 → 启用调试模式
2. 或在命令行中设置环境变量：
```bash
set DEBUG=1
python main.py
```

## 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置
1. Fork项目
2. 创建功能分支
3. 安装开发依赖
4. 进行开发和测试
5. 提交Pull Request

### 代码规范
- 遵循PEP 8代码风格
- 添加适当的注释和文档
- 确保代码通过测试

## 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## 更新日志

### v1.0.0 (2024-09-14)
- 🎉 初始版本发布
- ✨ 支持主流中国NPM镜像源
- ✨ 现代化PySide6界面
- ✨ 源速度测试功能
- ✨ 自定义源管理
- ✨ 配置持久化
- ✨ 使用历史记录

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 项目讨论区

---

**感谢使用NPM源管理器！** 🚀
