import asyncio
import json

from fastapi import APIRouter, Request, Depends, HTTPException, Query
from typing import List, Optional
from ...crud import weather as crud_weather
from sse_starlette.sse import EventSourceResponse

router = APIRouter(prefix="/stream-weather", tags=["stream-weather"])

@router.get("")
async def stream_weather(request: Request):
    async def event_generator():
        while True:
            # 클라이언트가 연결을 끊었는지 확인
            if await request.is_disconnected():
                print("Client disconnected")
                break

            #  해결책: 변수명을 'weather'에서 'weather_data'로 변경합니다!
            weather_data = crud_weather.get_weather_data()
            
            # SSE 포맷으로 데이터 전송
            yield {
                "event": "weather_update",
                "id": "message_id",
                "retry": 15000, # 연결이 끊겼을 때 15초 후 재시도
                #  데이터를 직렬화할 때도 변경한 변수명을 사용합니다.
                "data": json.dumps(weather_data) 
            }
            
            # 10초마다 날씨 업데이트
            await asyncio.sleep(10)

    return EventSourceResponse(event_generator())

