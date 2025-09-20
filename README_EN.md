# Apple App Bundle Finder

[English](./README_EN.md) | [简体中文](./README.md)

A GUI application based on Python and PySide6 for querying Apple App Store app information.

## Features

- Query app information through Apple's official API
- Support for multiple countries/regions
- Graphical user interface
- Modular code structure

## Installation

```bash
uv sync
```

## Usage

### Launch Application
```bash
uv run main.py
```

### Instructions

1. Enter the App ID in the interface (e.g., WeChat ID `414478124`)
2. Select country/region (default is China)
3. Click the "Search" button to get app information

## Project Structure

```
AppleAppBundleFinder/
├── main.py              # Application entry point
├── pyproject.toml       # Project configuration and dependencies
├── examples.txt         # App ID examples
├── README.md            # Project documentation
├── api/                 # API related modules
├── config/              # Configuration files
├── models/              # Data models
├── ui/                  # User interface components
└── utils/               # Utility functions
```

## API Information

Uses Apple's official API: `https://itunes.apple.com/lookup`

## Example App IDs

- WeChat: 414478124
- Alipay: 333206289
- TikTok: 1142110895
- Taobao: 387682726

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Snake-Konginchrist/apple-app-bundle-finder&type=Date)](https://www.star-history.com/#Snake-Konginchrist/apple-app-bundle-finder&Date)

## License

MIT License