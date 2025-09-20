#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用信息数据模型
定义应用信息的数据结构和处理方法
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class AppInfo:
    """应用信息数据类"""
    
    # 基本信息
    track_id: Optional[int] = None
    track_name: Optional[str] = None
    bundle_id: Optional[str] = None
    artist_name: Optional[str] = None
    artist_id: Optional[int] = None
    
    # 描述信息
    description: Optional[str] = None
    short_description: Optional[str] = None
    release_notes: Optional[str] = None
    
    # 版本信息
    version: Optional[str] = None
    current_version_release_date: Optional[str] = None
    minimum_os_version: Optional[str] = None
    
    # 价格和货币
    price: Optional[float] = None
    currency: Optional[str] = None
    formatted_price: Optional[str] = None
    
    # 分类信息
    primary_genre_name: Optional[str] = None
    primary_genre_id: Optional[int] = None
    genres: Optional[List[str]] = None
    genre_ids: Optional[List[int]] = None
    
    # 评分信息
    average_user_rating: Optional[float] = None
    user_rating_count: Optional[int] = None
    average_user_rating_for_current_version: Optional[float] = None
    user_rating_count_for_current_version: Optional[int] = None
    
    # 图标和截图
    artwork_url_60: Optional[str] = None
    artwork_url_100: Optional[str] = None
    artwork_url_512: Optional[str] = None
    screenshot_urls: Optional[List[str]] = None
    ipad_screenshot_urls: Optional[List[str]] = None
    
    # 文件信息
    file_size_bytes: Optional[int] = None
    content_advisory_rating: Optional[str] = None
    
    # 支持信息
    supported_devices: Optional[List[str]] = None
    is_game_center_enabled: Optional[bool] = None
    
    # URL信息
    track_view_url: Optional[str] = None
    seller_url: Optional[str] = None
    support_url: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'AppInfo':
        """从API响应数据创建AppInfo实例"""
        return cls(
            track_id=data.get('trackId'),
            track_name=data.get('trackName'),
            bundle_id=data.get('bundleId'),
            artist_name=data.get('artistName'),
            artist_id=data.get('artistId'),
            description=data.get('description'),
            short_description=data.get('shortDescription'),
            release_notes=data.get('releaseNotes'),
            version=data.get('version'),
            current_version_release_date=data.get('currentVersionReleaseDate'),
            minimum_os_version=data.get('minimumOsVersion'),
            price=data.get('price'),
            currency=data.get('currency'),
            formatted_price=data.get('formattedPrice'),
            primary_genre_name=data.get('primaryGenreName'),
            primary_genre_id=data.get('primaryGenreId'),
            genres=data.get('genres'),
            genre_ids=data.get('genreIds'),
            average_user_rating=data.get('averageUserRating'),
            user_rating_count=data.get('userRatingCount'),
            average_user_rating_for_current_version=data.get('averageUserRatingForCurrentVersion'),
            user_rating_count_for_current_version=data.get('userRatingCountForCurrentVersion'),
            artwork_url_60=data.get('artworkUrl60'),
            artwork_url_100=data.get('artworkUrl100'),
            artwork_url_512=data.get('artworkUrl512'),
            screenshot_urls=data.get('screenshotUrls'),
            ipad_screenshot_urls=data.get('ipadScreenshotUrls'),
            file_size_bytes=data.get('fileSizeBytes'),
            content_advisory_rating=data.get('contentAdvisoryRating'),
            supported_devices=data.get('supportedDevices'),
            is_game_center_enabled=data.get('isGameCenterEnabled'),
            track_view_url=data.get('trackViewUrl'),
            seller_url=data.get('sellerUrl'),
            support_url=data.get('supportUrl')
        )
    
    def get_formatted_file_size(self) -> str:
        """获取格式化的文件大小"""
        if not self.file_size_bytes:
            return "未知"
        
        # 确保size是数字类型
        try:
            size = float(self.file_size_bytes)
        except (ValueError, TypeError):
            return "未知"
        
        units = ['B', 'KB', 'MB', 'GB']
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.1f} {units[unit_index]}"
    
    def get_formatted_release_date(self) -> str:
        """获取格式化的发布日期"""
        if not self.current_version_release_date:
            return "未知"
        
        try:
            # 解析ISO格式的日期时间
            dt = datetime.fromisoformat(self.current_version_release_date.replace('Z', '+00:00'))
            return dt.strftime('%Y年%m月%d日')
        except:
            return self.current_version_release_date
    
    def get_rating_stars(self) -> str:
        """获取星级评分显示"""
        if not self.average_user_rating:
            return "暂无评分"
        
        stars = "★" * int(self.average_user_rating)
        stars += "☆" * (5 - int(self.average_user_rating))
        return f"{stars} ({self.average_user_rating:.1f})"