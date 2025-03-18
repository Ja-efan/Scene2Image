# Image Generation Service

Scene 기반 이미지 생성 - Spring Boot 백엔드와 연동하여 Scene 기반 이미지를 생성합니다.

## 개요

이 서비스는 스크립트 기반 이미지 생성 자동화를 위한 FastAPI 기반 마이크로서비스입니다. Spring Boot 백엔드로부터 장면(scene) 정보를 받아 자연어 처리를 통해 이미지 프롬프트를 생성하고, 해당 프롬프트를 기반으로 AI 이미지를 생성합니다.

## 주요 기능

- 장면 정보 기반 이미지 프롬프트 자동 생성 (OpenAI API)
- 생성된 프롬프트 기반 이미지 생성 (KLING AI API)
- 로컬 저장소 및 AWS S3 스토리지 연동
- RESTful API 인터페이스

## 기술 스택

- **Backend**: FastAPI
- **AI APIs**: OpenAI API, KLING AI API
- **스토리지**: AWS S3, 로컬 파일 시스템
- **개발 언어**: Python 3.12+

## 설치 및 실행

### 환경 설정

1. 저장소 클론
```
git clone [repository-url]
cd Image-Generation
```

2. 가상 환경 생성 및 활성화
```
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 또는
.venv\Scripts\activate  # Windows
```

3. 의존성 설치
```
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 프로젝트 루트에 생성하고 다음 변수를 설정합니다:
```
# KLING AI
KLING_ACCESS_KEY=your_kling_access_key
KLING_SECRET_KEY=your_kling_secret_key

# OPENAI
OPENAI_API_KEY=your_openai_api_key

# AWS S3
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
S3_BUCKET_NAME=your_bucket_name
AWS_REGION=ap-northeast-2
```

### 실행

```
python main.py
```

서버는 기본적으로 `http://0.0.0.0:8000`에서 실행됩니다.

## API 엔드포인트

### 이미지 생성 

**엔드포인트**: `POST /api/v1/images/generate-image`

**요청 본문**:
```json
{
  "script_metadata": {
    "title": "스크립트 제목",
    "script_id": 1,
    "characters": [
      {
        "name": "캐릭터명",
        "gender": 1,  // 1: 남성, 2: 여성
        "description": "캐릭터 설명"
      }
    ]
  },
  "scene_id": 1,
  "audios": [
    {
      "type": "narration",
      "text": "나레이션 텍스트"
    },
    {
      "type": "dialogue",
      "character": "캐릭터명",
      "text": "대사 내용",
      "emotion": "감정 상태"
    }
  ]
}
```

**응답**:
```json
{
  "scene_id": 1,
  "image_prompt": "생성된 이미지 프롬프트",
  "image_s3url": "생성된 이미지의 S3 URL"
}
```

## 파일 구조

```
Image-Generation/
├── app/
│   ├── api/
│   │   └── routes/       # API 라우터
│   ├── core/             # 설정 및 유틸리티
│   ├── schemas/          # 데이터 모델
│   └── services/         # 비즈니스 로직
├── images/               # 로컬 이미지 저장소
├── static/               # 정적 파일
├── .env                  # 환경 변수
├── main.py               # 애플리케이션 진입점
└── requirements.txt      # 의존성 목록
```