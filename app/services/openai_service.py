"""
OpenAI 서비스
"""
from openai import OpenAI
from app.schemas.models import Scene
from app.core.config import settings    

# OpenAI API 키 가져오기
api_key = settings.OPENAI_API_KEY
if not api_key:
    raise ValueError("OPENAI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)


class OpenAIService:
    """OpenAI API를 활용하여 이미지 프롬프트를 생성하는 서비스"""
    
    @staticmethod
    async def generate_image_prompt(scene: Scene) -> str:
        """
        장면 정보를 바탕으로 DALL·E에 사용할 이미지 프롬프트를 생성합니다.
        
        Args:
            scene: 장면 정보
            
        Returns:
            생성된 이미지 프롬프트
        """
        # 프롬프트 생성을 위한 컨텍스트 구성
        context = {
            "title": scene.script_metadata.title,
            "characters": [],
            "audios": []
        }
        
        # 등장인물 정보 추가
        for character in scene.script_metadata.characters:
            character_info = {
                "name": character.name,
                "gender": "남자" if character.gender == 1 else "여자",
                "description": character.description
            }
            context["characters"].append(character_info)
        
        # 오디오 정보 추가
        for audio in scene.audios:
            audio_info = {
                "type": audio.type,
                "text": audio.text
            }
            
            if audio.type == "dialogue" and audio.character:
                audio_info["character"] = audio.character
                audio_info["emotion"] = audio.emotion if audio.emotion else "neutral"
                
            context["audios"].append(audio_info)
        
        # GPT에 전송할 프롬프트 구성
        prompt = f"""
장면 제목: {context['title']}
장면 ID: {scene.scene_id}

등장인물:
"""
        
        for char in context["characters"]:
            prompt += f"- {char['name']} ({char['gender']}): {char['description']}\n"
            
        prompt += "\n장면 내용:\n"
        
        for audio in context["audios"]:
            if audio["type"] == "narration":
                prompt += f"[내레이션] {audio['text']}\n"
            elif audio["type"] == "dialogue":
                emotion = audio.get("emotion", "")
                emotion_text = f" ({emotion})" if emotion else ""
                prompt += f"[대사] {audio.get('character', '알 수 없음')}{emotion_text}: {audio['text']}\n"
            elif audio["type"] == "sound":
                prompt += f"[효과음] {audio['text']}\n"
        
        prompt += "\n위 장면을 시각화하는 고품질 이미지를 생성하기 위한 디테일한 프롬프트를 작성해주세요. 장면의 분위기, 등장인물의 특징, 배경 등을 자세히 묘사해주세요. 영어로 작성해주세요."
        
        try:
            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 이미지 생성 프롬프트를 작성하는 전문가입니다. 주어진 장면을 시각적으로 묘사하는 상세한 영어 프롬프트를 작성해주세요."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # 생성된 프롬프트 반환
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # 오류 발생 시 기본 프롬프트 반환
            print(f"OpenAI API 오류: {str(e)}")
            
            # 기본 프롬프트 생성
            default_prompt = f"A scene from the story '{context['title']}', showing "
            
            # 등장인물 정보 추가
            characters_str = ", ".join([f"{c['name']}" for c in context["characters"]])
            default_prompt += f"{characters_str}. "
            
            # 첫 번째 나레이션이나 대화 내용 추가
            for audio in context["audios"]:
                if audio["type"] in ["narration", "dialogue"]:
                    default_prompt += f"{audio['text']}"
                    break
            
            return default_prompt

# 서비스 인스턴스 생성
openai_service = OpenAIService() 