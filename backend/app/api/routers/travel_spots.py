from fastapi import APIRouter, Depends, Query
from typing import List, Optional

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
