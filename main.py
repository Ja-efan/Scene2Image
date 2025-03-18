"""
애플리케이션 실행 파일
"""
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
from dotenv import load_dotenv
import json
from typing import Optional
import uvicorn
import jwt
import time

# app 패키지에서 라우터 가져오기
from app.api.routes import image_routes

# 환경 변수 로드
load_dotenv()

app = FastAPI(title="Kling AI 이미지 생성 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 제공을 위한 디렉토리 생성
os.makedirs("static/images", exist_ok=True)
os.makedirs("images", exist_ok=True)

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# 이미지 라우터 등록
app.include_router(image_routes.router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 