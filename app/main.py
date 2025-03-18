"""
FastAPI 애플리케이션 메인 파일
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.api.routes import image_routes
from app.utils.helpers import read_html_template

# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# API 라우터 등록
app.include_router(image_routes.router, prefix=settings.API_V1_STR)  # 이미지 생성 라우터

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """메인 페이지 반환"""
    return read_html_template(f"{settings.STATIC_DIR}/index.html")

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"} 