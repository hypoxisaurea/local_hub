import logging
import os
import requests
from dotenv import load_dotenv

# API 응답 로깅용 설정
logger = logging.getLogger(__name__)

# 🌟 .env 파일 로드하기 
# (프로젝트 루트에 있는 .env 파일을 찾아 자동으로 시스템 환경 변수에 등록해 줍니다)
load_dotenv()

# 이제 시스템 환경 변수에서 안전하게 키를 꺼내옵니다.
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_data():
    city = "Seoul"
    # metric: 화씨(F) 대신 우리에게 익숙한 섭씨(C) 온도를 받기 위한 옵션
    # lang=kr: 날씨 상태 메시지(예: '맑음', '튼구름')를 한국어로 받기 위한 옵션
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=kr"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # HTTP 에러(404, 500 등) 발생 시 예외 발생
        
        data = response.json()
        
        # OpenWeatherMap API가 반환하는 JSON 구조에서 필요한 값만 정제해서 반환
        return {
            "temp": round(data["main"]["temp"], 1),              # 현재 온도 (소수점 첫째 자리까지 반올림)
            "condition": data["weather"][0]["description"],      # 날씨 설명 (예: "실비", "맑음")
            "icon": data["weather"][0]["icon"]                   # 날씨 상태 아이콘 코드 (예: "01d")
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenWeatherMap API 호출 실패: {e}")
        # API 호출이 실패했을 때 임시로 내려줄 에러 기본값 (서버가 중단되지 않도록 방지)
        return {
            "temp": "N/A",
            "condition": "정보를 불러올 수 없음",
            "icon": "01d"
        }
