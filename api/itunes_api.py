#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iTunes API接口模块
提供与Apple iTunes API交互的功能
"""

import requests
from typing import Optional, List, Dict, Any
from models.app_info import AppInfo


class iTunesAPI:
    """iTunes API客户端类"""
    
    BASE_URL = "https://itunes.apple.com"
    LOOKUP_ENDPOINT = "/lookup"
    SEARCH_ENDPOINT = "/search"
    
    def __init__(self, timeout: int = 10):
        """
        初始化API客户端
        
        Args:
            timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.session = requests.Session()
        # 设置User-Agent
        self.session.headers.update({
            'User-Agent': 'AppleAppBundleFinder/1.0.0'
        })
    
    def lookup_by_id(self, app_id: str, country: str = "cn") -> Optional[AppInfo]:
        """
        根据应用ID查询应用信息
        
        Args:
            app_id: 应用ID（可以是trackId或bundleId）
            country: 国家代码，默认为中国(cn)
            
        Returns:
            AppInfo对象或None（如果查询失败）
        """
        try:
            # 构建请求参数
            params = {
                'id' if app_id.isdigit() else 'bundleId': app_id,
                'country': country,
                'entity': 'software'
            }
            
            # 发送请求
            response = self.session.get(
                f"{self.BASE_URL}{self.LOOKUP_ENDPOINT}",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # 解析响应
            data = response.json()
            
            if data.get('resultCount', 0) > 0:
                app_data = data['results'][0]
                return AppInfo.from_api_response(app_data)
            else:
                return None
                
        except requests.RequestException as e:
            print(f"API请求错误: {e}")
            return None
        except Exception as e:
            print(f"数据解析错误: {e}")
            return None
    
    def search_apps(self, term: str, country: str = "cn", limit: int = 10) -> List[AppInfo]:
        """
        搜索应用
        
        Args:
            term: 搜索关键词
            country: 国家代码，默认为中国(cn)
            limit: 返回结果数量限制
            
        Returns:
            AppInfo对象列表
        """
        try:
            # 构建请求参数
            params = {
                'term': term,
                'country': country,
                'entity': 'software',
                'limit': limit
            }
            
            # 发送请求
            response = self.session.get(
                f"{self.BASE_URL}{self.SEARCH_ENDPOINT}",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # 解析响应
            data = response.json()
            
            apps = []
            for app_data in data.get('results', []):
                app_info = AppInfo.from_api_response(app_data)
                apps.append(app_info)
            
            return apps
            
        except requests.RequestException as e:
            print(f"API请求错误: {e}")
            return []
        except Exception as e:
            print(f"数据解析错误: {e}")
            return []
    
    def get_app_details(self, app_id: str, country: str = "cn") -> Dict[str, Any]:
        """
        获取应用的原始详细信息（用于调试）
        
        Args:
            app_id: 应用ID
            country: 国家代码
            
        Returns:
            原始API响应数据
        """
        try:
            params = {
                'id' if app_id.isdigit() else 'bundleId': app_id,
                'country': country,
                'entity': 'software'
            }
            
            response = self.session.get(
                f"{self.BASE_URL}{self.LOOKUP_ENDPOINT}",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"获取详细信息错误: {e}")
            return {}