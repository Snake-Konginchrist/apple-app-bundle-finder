#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
提供各种辅助功能函数
"""

import re
from typing import Optional
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl, QEventLoop


def is_valid_app_id(app_id: str) -> bool:
    """
    验证应用ID是否有效
    
    Args:
        app_id: 应用ID字符串
        
    Returns:
        是否为有效的应用ID
    """
    if not app_id or not app_id.strip():
        return False
    
    app_id = app_id.strip()
    
    # 检查是否为数字ID（trackId）
    if app_id.isdigit():
        return len(app_id) >= 6  # trackId通常至少6位数
    
    # 检查是否为Bundle ID格式
    bundle_id_pattern = r'^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$'
    return bool(re.match(bundle_id_pattern, app_id))


def format_number(number: Optional[int]) -> str:
    """
    格式化数字显示（添加千位分隔符）
    
    Args:
        number: 要格式化的数字
        
    Returns:
        格式化后的字符串
    """
    if number is None:
        return "未知"
    
    return f"{number:,}"


def truncate_text(text: Optional[str], max_length: int = 100) -> str:
    """
    截断文本到指定长度
    
    Args:
        text: 要截断的文本
        max_length: 最大长度
        
    Returns:
        截断后的文本
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def load_image_from_url(url: str) -> Optional[QPixmap]:
    """
    从URL加载图片
    
    Args:
        url: 图片URL
        
    Returns:
        QPixmap对象或None
    """
    if not url:
        return None
    
    try:
        import requests
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        return pixmap if not pixmap.isNull() else None
        
    except Exception as e:
        print(f"加载图片失败: {e}")
        return None


import json
import os


def load_country_mapping() -> dict:
    """
    从配置文件加载国家代码映射
    
    Returns:
        国家代码映射字典
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'countries.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"警告: 配置文件 {config_path} 不存在，使用默认国家映射")
        return {
            'cn': '中国',
            'us': '美国',
            'jp': '日本',
            'kr': '韩国',
            'gb': '英国',
            'de': '德国',
            'fr': '法国',
            'ca': '加拿大',
            'au': '澳大利亚',
            'in': '印度'
        }
    except Exception as e:
        print(f"加载国家配置错误: {e}")
        return {}


def get_country_name(country_code: str) -> str:
    """
    根据国家代码获取国家名称
    
    Args:
        country_code: 国家代码
        
    Returns:
        国家名称
    """
    country_map = load_country_mapping()
    return country_map.get(country_code.lower(), country_code.upper())


def validate_url(url: str) -> bool:
    """
    验证URL是否有效
    
    Args:
        url: 要验证的URL
        
    Returns:
        是否为有效URL
    """
    if not url:
        return False
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))