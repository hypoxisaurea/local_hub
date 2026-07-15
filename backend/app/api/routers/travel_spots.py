from fastapi import APIRouter, Depends, Query
from typing import List, Optional, Dict

from ..deps import get_db
from ...schemas import schemas
from ...crud import travel_spots as crud_travel_spots

router = APIRouter(prefix="/api", tags=["travel_spots"])

# 각 테이블의 전체 데이터를 가져오는 API (검색어 가능)
@router.get("/travel-spots/attractions", response_model=List[schemas.TourItem])
def read_travel_spots_attractions(q: Optional[str] = Query(None), lang: str = Query("ko", pattern="^(ko|en)$")):
    return crud_travel_spots._fetch_travel_spot_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["attractions"], q, lang=lang)

@router.get("/travel-spots/sports", response_model=List[schemas.TourItem])
def read_travel_spots_sports(q: Optional[str] = Query(None), lang: str = Query("ko", pattern="^(ko|en)$")):
    return crud_travel_spots._fetch_travel_spot_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["sports"], q, lang=lang)

@router.get("/travel-spots/culture", response_model=List[schemas.TourItem])
def read_travel_spots_culture(q: Optional[str] = Query(None), lang: str = Query("ko", pattern="^(ko|en)$")):
    return crud_travel_spots._fetch_travel_spot_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["culture"], q, lang=lang)

@router.get("/travel-spots/shopping", response_model=List[schemas.TourItem])
def read_travel_spots_shopping(q: Optional[str] = Query(None), lang: str = Query("ko", pattern="^(ko|en)$")):
    return crud_travel_spots._fetch_travel_spot_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["shopping"], q, lang=lang)

@router.get("/travel-spots/festivals", response_model=List[schemas.TourItem])
def read_travel_spots_festivals(q: Optional[str] = Query(None), lang: str = Query("ko", pattern="^(ko|en)$")):
    return crud_travel_spots._fetch_travel_spot_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["festivals"], q, lang=lang)

@router.get("/travel-spots", response_model=List[schemas.TourItem])
def read_all_travel_spots(q: Optional[str] = Query(None)):
    """
    관광지, 스포츠, 문화, 쇼핑 등 모든 카테고리의 데이터를 합쳐서 반환합니다.
    """
    all_spots = []
    
    # 1. 대상이 되는 카테고리 키 배열 생성
    categories = ["attractions", "sports", "culture", "shopping"]
    
    # 2. 반복문을 돌며 각 테이블의 데이터를 가져와서 하나의 리스트에 병합
    for category in categories:
        table = crud_travel_spots.TRAVEL_SPOT_TABLES[category]
        spots_data = crud_travel_spots._fetch_travel_spot_rows(table, q)
        
        # 데이터가 존재한다면 리스트에 추가
        if spots_data:
            all_spots.extend(spots_data)
            
    return all_spots

# id, 이미지, 이름, 주소 만 가져오는 간단한 조회용 API (검색어 가능)
@router.get("/travel-spots-simple/attractions", response_model=List[schemas.TravelSpotSummary])
def read_travel_spots_attractions(
    q: Optional[str] = Query(None, description="검색어"),
    lang: str = Query("ko", pattern="^(ko|en)$", description="콘텐츠 표시 언어"),
):
    return crud_travel_spots._fetch_travel_spot_simple_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["attractions"], q=q, lang=lang)

@router.get("/travel-spots-simple/sports", response_model=List[schemas.TravelSpotSummary])
def read_travel_spots_sports(
    q: Optional[str] = Query(None, description="검색어"),
    lang: str = Query("ko", pattern="^(ko|en)$", description="콘텐츠 표시 언어"),
):
    return crud_travel_spots._fetch_travel_spot_simple_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["sports"], q=q, lang=lang)

@router.get("/travel-spots-simple/culture", response_model=List[schemas.TravelSpotSummary])
def read_travel_spots_culture(
    q: Optional[str] = Query(None, description="검색어"),
    lang: str = Query("ko", pattern="^(ko|en)$", description="콘텐츠 표시 언어"),
):
    return crud_travel_spots._fetch_travel_spot_simple_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["culture"], q=q, lang=lang)

@router.get("/travel-spots-simple/shopping", response_model=List[schemas.TravelSpotSummary])
def read_travel_spots_shopping(
    q: Optional[str] = Query(None, description="검색어"),
    lang: str = Query("ko", pattern="^(ko|en)$", description="콘텐츠 표시 언어"),
):
    return crud_travel_spots._fetch_travel_spot_simple_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["shopping"], q=q, lang=lang)


@router.get("/travel-spots-simple/festivals", response_model=List[schemas.TravelSpotSummary])
def read_travel_spots_festivals_simple(
    q: Optional[str] = Query(None, description="검색어"),
    lang: str = Query("ko", pattern="^(ko|en)$", description="콘텐츠 표시 언어"),
):
    return crud_travel_spots._fetch_travel_spot_simple_rows(crud_travel_spots.TRAVEL_SPOT_TABLES["festivals"], q=q, lang=lang)
