# Apple App Bundle Finder

一个基于Python和PySide6的GUI应用，用于查询Apple App Store应用信息。

## 功能特点

- 通过Apple官方API查询应用信息
- 支持多国家/地区查询
- 图形化用户界面
- 模块化代码结构

## 安装依赖

```bash
pip install -e .
```

## 使用方法

### 启动应用
```bash
python main.py
```

### 使用说明

1. 在界面中输入应用ID（如：微信ID `414478124`）
2. 选择国家/地区（默认为中国）
3. 点击"查询"按钮获取应用信息

## 项目结构

```
AppleAppBundleFinder/
├── main.py              # 应用入口点
├── pyproject.toml       # 项目配置和依赖
├── examples.txt         # 应用ID示例
├── README.md            # 项目说明
├── api/                 # API相关模块
├── config/              # 配置文件
├── models/              # 数据模型
├── ui/                  # 用户界面组件
└── utils/               # 工具函数
```

## API说明

使用Apple官方API：`https://itunes.apple.com/lookup`

## 示例应用ID

- 微信: 414478124
- 支付宝: 333206289
- 抖音: 1142110895
- 淘宝: 387682726

## Star History

[![Star History Chart](https://api.star-history.com/svg?ref=Snake-Konginchrist/apple-app-bundle-finder&type=Date)](https://star-history.com/#Snake-Konginchrist/apple-app-bundle-finder&Date)

## 许可证

MIT License