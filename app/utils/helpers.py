"""
유틸리티 함수
"""
import os
from pathlib import Path
from typing import Dict, Any

def read_html_template(template_path: str) -> str:
    """
    HTML 템플릿 파일을 읽어 문자열로 반환합니다.
    
    Args:
        template_path: 템플릿 파일 경로
        
    Returns:
        HTML 템플릿 문자열
    """
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise Exception(f"템플릿 파일 읽기 오류: {str(e)}")

def validate_image_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    이미지 생성 파라미터를 검증하고 기본값을 설정합니다.
    
    Args:
        params: 이미지 생성 파라미터
        
    Returns:
        검증된 파라미터
    """
    # 너비와 높이 제한
    width = max(256, min(params.get("width", 512), 1024))
    height = max(256, min(params.get("height", 512), 1024))
    
    # 64의 배수로 조정
    width = (width // 64) * 64
    height = (height // 64) * 64
    
    return {
        **params,
        "width": width,
        "height": height
    } 