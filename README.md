# 收据生成器

基于Kivy的收据生成应用，支持在Android设备上运行。

## 功能特性

- 输入收据信息（日期、交款单位、收款方式、金额、收款事由等）
- 自动生成电子版收据图片
- 支持金额自动转换为中文大写
- 美观的用户界面

## 环境要求

- Python 3.8+
- 虚拟环境已配置

## 本地运行

1. 激活虚拟环境：
   ```bash
   .\venv\Scripts\activate
   ```

2. 运行应用：
   ```bash
   python main.py
   ```

## 打包APK

### 方法一：使用Buildozer（推荐）

1. 安装Buildozer：
   ```bash
   pip install buildozer
   ```

2. 初始化Buildozer（已配置buildozer.spec）：
   ```bash
   buildozer init
   ```

3. 打包APK：
   ```bash
   buildozer android debug
   ```

生成的APK文件位于 `bin/` 目录。

### 方法二：使用PyInstaller（Windows桌面版）

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## 注意事项

- 打包APK需要在Linux环境下进行（推荐使用WSL2或虚拟机）
- 首次打包需要下载Android SDK和NDK，时间较长
- 确保设备有足够的存储空间

## 项目结构

```
receipt/
├── main.py              # 主程序文件
├── buildozer.spec       # APK打包配置
├── requirements.txt     # 依赖列表
├── venv/               # 虚拟环境
└── README.md           # 说明文档
```
