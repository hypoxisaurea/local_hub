#!/usr/bin/env python3
"""Generate English companion data files for Seoul tourism JSON data.

The source files are Korean public tourism datasets. This script keeps the
original files unchanged and creates local, deterministic English variants.
It uses rule-based address conversion and Revised Romanization for names, with
small dictionaries for common Seoul place/category terms.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

TOUR_FILES = [
    "서울_관광지.json",
    "서울_레포츠.json",
    "서울_문화시설.json",
    "서울_쇼핑.json",
    "서울_숙박.json",
    "서울_여행코스.json",
    "서울_축제공연행사.json",
]

CONTENT_TYPE_EN = {
    "관광지": "Attractions",
    "레포츠": "Leisure Sports",
    "문화시설": "Cultural Facilities",
    "쇼핑": "Shopping",
    "숙박": "Accommodation",
    "여행코스": "Travel Courses",
    "축제공연행사": "Festivals & Performances",
    "맛집": "Restaurants",
    "음식점": "Restaurants",
}

SEOUL_DISTRICTS = {
    "강남구": "Gangnam-gu",
    "강동구": "Gangdong-gu",
    "강북구": "Gangbuk-gu",
    "강서구": "Gangseo-gu",
    "관악구": "Gwanak-gu",
    "광진구": "Gwangjin-gu",
    "구로구": "Guro-gu",
    "금천구": "Geumcheon-gu",
    "노원구": "Nowon-gu",
    "도봉구": "Dobong-gu",
    "동대문구": "Dongdaemun-gu",
    "동작구": "Dongjak-gu",
    "마포구": "Mapo-gu",
    "서대문구": "Seodaemun-gu",
    "서초구": "Seocho-gu",
    "성동구": "Seongdong-gu",
    "성북구": "Seongbuk-gu",
    "송파구": "Songpa-gu",
    "양천구": "Yangcheon-gu",
    "영등포구": "Yeongdeungpo-gu",
    "용산구": "Yongsan-gu",
    "은평구": "Eunpyeong-gu",
    "종로구": "Jongno-gu",
    "중구": "Jung-gu",
    "중랑구": "Jungnang-gu",
}

KNOWN_NAMES = {
    "서울": "Seoul",
    "남산": "Namsan",
    "한강": "Hangang",
    "청계천": "Cheonggyecheon",
    "경복궁": "Gyeongbokgung Palace",
    "창덕궁": "Changdeokgung Palace",
    "창경궁": "Changgyeonggung Palace",
    "덕수궁": "Deoksugung Palace",
    "종묘": "Jongmyo Shrine",
    "광화문": "Gwanghwamun",
    "동대문": "Dongdaemun",
    "남대문": "Namdaemun",
    "명동": "Myeong-dong",
    "이태원": "Itaewon",
    "홍대": "Hongdae",
    "잠실": "Jamsil",
    "여의도": "Yeouido",
    "북촌": "Bukchon",
    "서촌": "Seochon",
    "성수": "Seongsu",
    "강남": "Gangnam",
    "인사동": "Insadong",
    "대학로": "Daehak-ro",
    "국립": "National",
    "서울역": "Seoul Station",
}

TERM_SUFFIXES = [
    ("한강공원", "Hangang Park"),
    ("공원", "Park"),
    ("근린공원", "Neighborhood Park"),
    ("생태공원", "Ecological Park"),
    ("체험공원", "Experience Park"),
    ("박물관", "Museum"),
    ("미술관", "Art Museum"),
    ("도서관", "Library"),
    ("공연장", "Performance Hall"),
    ("문화원", "Cultural Center"),
    ("문화센터", "Cultural Center"),
    ("전시관", "Exhibition Hall"),
    ("기념관", "Memorial Hall"),
    ("역사관", "History Museum"),
    ("수목원", "Arboretum"),
    ("식물원", "Botanical Garden"),
    ("동물원", "Zoo"),
    ("시장", "Market"),
    ("백화점", "Department Store"),
    ("아울렛", "Outlet"),
    ("쇼핑몰", "Shopping Mall"),
    ("면세점", "Duty Free Shop"),
    ("호텔", "Hotel"),
    ("게스트하우스", "Guesthouse"),
    ("호스텔", "Hostel"),
    ("캠핑장", "Campground"),
    ("야영장", "Campground"),
    ("축제", "Festival"),
    ("페스티벌", "Festival"),
    ("공연", "Performance"),
    ("전시", "Exhibition"),
    ("코스", "Course"),
    ("길", "Trail"),
    ("거리", "Street"),
    ("마을", "Village"),
    ("사찰", "Temple"),
    ("성당", "Cathedral"),
    ("교회", "Church"),
    ("사", "Temple"),
]

TIME_REPLACEMENTS = {
    "월요일": "Monday",
    "화요일": "Tuesday",
    "수요일": "Wednesday",
    "목요일": "Thursday",
    "금요일": "Friday",
    "토요일": "Saturday",
    "일요일": "Sunday",
    "월": "Mon",
    "화": "Tue",
    "수": "Wed",
    "목": "Thu",
    "금": "Fri",
    "토": "Sat",
    "일": "Sun",
    "평일": "Weekdays",
    "주말": "Weekends",
    "공휴일": "Holidays",
    "매일": "Daily",
    "브레이크타임": "break time",
    "라스트오더": "last order",
    "다음날": "next day",
    "재료 소진 시": "until sold out",
    "조기 마감": "early closing",
    "오전": "AM",
    "오후": "PM",
}

SUBWAY_REPLACEMENTS = {
    "지하철": "Subway",
    "호선": "Line",
    "역": "Station",
    "번 출구": " Exit",
    "번출구": " Exit",
    "출구": "Exit",
    "버스": "bus",
    "환승": "transfer",
    "정류장": "stop",
    "하차": "get off",
    "도보": "walk",
}

LANGUAGE_REPLACEMENTS = {
    "한국어": "Korean",
    "영어": "English",
    "일어": "Japanese",
    "일본어": "Japanese",
    "중국어": "Chinese",
    "간체": "Simplified",
    "번체": "Traditional",
}


LEADS = (
    "g",
    "kk",
    "n",
    "d",
    "tt",
    "r",
    "m",
    "b",
    "pp",
    "s",
    "ss",
    "",
    "j",
    "jj",
    "ch",
    "k",
    "t",
    "p",
    "h",
)
VOWELS = (
    "a",
    "ae",
    "ya",
    "yae",
    "eo",
    "e",
    "yeo",
    "ye",
    "o",
    "wa",
    "wae",
    "oe",
    "yo",
    "u",
    "wo",
    "we",
    "wi",
    "yu",
    "eu",
    "ui",
    "i",
)
TAILS = (
    "",
    "k",
    "k",
    "ks",
    "n",
    "nj",
    "nh",
    "t",
    "l",
    "lk",
    "lm",
    "lb",
    "ls",
    "lt",
    "lp",
    "lh",
    "m",
    "p",
    "ps",
    "t",
    "t",
    "ng",
    "t",
    "t",
    "k",
    "t",
    "p",
    "t",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def romanize_char(ch: str) -> str:
    code = ord(ch) - 0xAC00
    if code < 0 or code > 11171:
        return ch
    lead = code // 588
    vowel = (code % 588) // 28
    tail = code % 28
    return LEADS[lead] + VOWELS[vowel] + TAILS[tail]


def romanize_korean(text: str) -> str:
    if not text:
        return ""
    pieces: list[str] = []
    current = []

    for ch in text.strip():
        if "가" <= ch <= "힣":
            current.append(romanize_char(ch))
            continue
        if current:
            pieces.append("".join(current).capitalize())
            current = []
        pieces.append(ch)

    if current:
        pieces.append("".join(current).capitalize())

    result = "".join(pieces)
    result = re.sub(r"\s+", " ", result).strip()
    result = re.sub(r"\s+([),./])", r"\1", result)
    result = re.sub(r"([(])\s+", r"\1", result)
    return result


def title_case_ascii_words(text: str) -> str:
    words = []
    for word in text.split(" "):
        if not word or re.search(r"[A-Z]{2,}|\d", word):
            words.append(word)
        else:
            words.append(word[:1].upper() + word[1:])
    return " ".join(words)


def translate_name(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""

    for ko, en in sorted(KNOWN_NAMES.items(), key=lambda item: len(item[0]), reverse=True):
        if text == ko:
            return en

    for suffix, en_suffix in TERM_SUFFIXES:
        if text.endswith(suffix) and len(text) > len(suffix):
            stem = text[: -len(suffix)].strip()
            stem_en = translate_name(stem)
            if stem_en:
                return f"{stem_en} {en_suffix}"

    translated = text
    for ko, en in sorted(KNOWN_NAMES.items(), key=lambda item: len(item[0]), reverse=True):
        translated = translated.replace(ko, en)

    translated = romanize_korean(translated)
    return title_case_ascii_words(translated)


def romanize_road(road: str) -> str:
    road = road.strip()
    for suffix, suffix_en in (("대로", "daero"), ("로", "ro"), ("길", "gil")):
        if suffix not in road:
            continue
        base, rest = road.split(suffix, 1)
        base_en = romanize_korean(base).capitalize()
        rest_en = romanize_road(rest) if rest else ""
        return " ".join(part for part in [f"{base_en}-{suffix_en}", rest_en] if part)
    return romanize_korean(road)


def translate_building_detail(text: str) -> str:
    if not text:
        return ""
    replacements = {
        "지하": "B",
        "층": "F",
        "호": "",
        "신관": "New Wing",
        "본관": "Main Building",
    }
    result = text
    for ko, en in replacements.items():
        result = result.replace(ko, en)
    return romanize_korean(result)


def translate_address(addr: str) -> str:
    addr = (addr or "").strip()
    if not addr:
        return ""

    zipcode = ""
    zip_match = re.match(r"^(\d{5,6})\s+", addr)
    if zip_match:
        zipcode = zip_match.group(1)
        addr = addr[zip_match.end() :]

    addr = addr.replace("서울특별시", "서울")
    parens = re.findall(r"\(([^)]*)\)", addr)
    addr_no_parens = re.sub(r"\s*\([^)]*\)", "", addr).strip()
    tokens = addr_no_parens.split()

    district = ""
    if tokens and tokens[0] == "서울":
        tokens = tokens[1:]
    if tokens and tokens[0] in SEOUL_DISTRICTS:
        district = SEOUL_DISTRICTS[tokens.pop(0)]

    detail_parts: list[str] = []
    road_part = ""
    number_part = ""

    if tokens:
        road_part = romanize_road(tokens.pop(0))
    if tokens:
        number_part = tokens.pop(0)
    if tokens:
        detail_parts.extend(tokens)

    for detail in parens:
        if re.search(r"(동|가)$", detail.strip()):
            continue
        detail_parts.append(detail)

    street = " ".join(part for part in [number_part, road_part] if part).strip()
    detail_en = translate_building_detail(" ".join(detail_parts).strip())

    parts = [part for part in [detail_en, street, district, "Seoul", zipcode] if part]
    return romanize_korean(", ".join(parts))


def replace_many(text: str, replacements: dict[str, str]) -> str:
    if not text:
        return ""
    result = text
    for ko, en in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        result = result.replace(ko, en)
    return romanize_korean(result)


def translate_menu(text: str | None) -> str | None:
    if text is None:
        return None
    replacements = {
        "파스타": "pasta",
        "스테이크": "steak",
        "치킨": "chicken",
        "샐러드": "salad",
        "커피": "coffee",
        "케이크": "cake",
        "마늘빵": "garlic bread",
        "떡볶이": "tteokbokki",
        "김밥": "gimbap",
        "칼국수": "kalguksu",
        "버섯": "mushroom",
        "양갈비": "lamb ribs",
        "정식": "set meal",
        "탕": "stew",
        "원": "KRW",
        "개입": "pieces",
        "세트": "set",
        "기본": "basic",
        "다크": "dark",
        "달콤": "sweet",
    }
    return replace_many(text, replacements)


def translate_tour_file(path: Path) -> tuple[dict[str, Any], list[dict[str, str]]]:
    payload = read_json(path)
    category = payload.get("contentType") or path.stem.replace("서울_", "")
    content_type_en = CONTENT_TYPE_EN.get(category, translate_name(str(category)))
    translated = dict(payload)
    translated["region"] = "Seoul"
    translated["contentType"] = content_type_en
    translated["lang"] = "en"
    translated["sourceLang"] = "ko"

    translation_rows: list[dict[str, str]] = []
    items = []
    for item in payload.get("items", []):
        out = dict(item)
        out["title"] = translate_name(str(item.get("title") or ""))
        out["addr1"] = translate_address(str(item.get("addr1") or ""))
        out["addr2"] = translate_building_detail(str(item.get("addr2") or ""))
        if str(out.get("zipcode") or "").startswith("우편번호"):
            out["zipcode"] = str(out["zipcode"]).replace("우편번호", "Postal code ")
        out["contentType"] = content_type_en
        items.append(out)

        contentid = str(item.get("contentid") or "").strip()
        if contentid:
            translation_rows.append(
                {
                    "category": str(category),
                    "contentid": contentid,
                    "lang": "en",
                    "title": out["title"],
                    "addr1": out["addr1"],
                    "addr2": out["addr2"],
                    "contentType": content_type_en,
                }
            )

    translated["items"] = items
    return translated, translation_rows


def translate_restaurants(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    descriptions = dict(payload.get("DESCRIPTION", {}))
    descriptions.update(
        {
            "NEW_ADDRESS": "New address",
            "SUBWAY_INFO": "Transportation information",
            "POST_SN": "ID",
            "CMMN_HMPG_URL": "Website",
            "CMMN_TELNO": "Phone number",
            "POST_URL": "Content URL",
            "CMMN_HMPG_LANG": "Homepage language",
            "ADDRESS": "Address",
            "FD_REPRSNT_MENU": "Representative menu",
            "CMMN_USE_TIME": "Opening hours",
            "POST_SJ": "Name",
            "LANG_CODE_ID": "Language",
        }
    )

    data = []
    for row in payload.get("DATA", []):
        out = dict(row)
        out["new_address"] = translate_address(str(row.get("new_address") or ""))
        out["address"] = translate_address(str(row.get("address") or ""))
        out["post_sj"] = translate_name(str(row.get("post_sj") or ""))
        out["fd_reprsnt_menu"] = translate_menu(row.get("fd_reprsnt_menu"))
        out["subway_info"] = replace_many(str(row.get("subway_info") or ""), SUBWAY_REPLACEMENTS) or row.get("subway_info")
        out["cmmn_use_time"] = replace_many(str(row.get("cmmn_use_time") or ""), TIME_REPLACEMENTS) or row.get("cmmn_use_time")
        if row.get("cmmn_hmpg_lang"):
            out["cmmn_hmpg_lang"] = replace_many(str(row["cmmn_hmpg_lang"]), LANGUAGE_REPLACEMENTS)
        out["lang_code_id"] = "en"
        data.append(out)

    return {
        "DESCRIPTION": descriptions,
        "DATA": data,
        "region": "Seoul",
        "contentType": CONTENT_TYPE_EN["맛집"],
        "lang": "en",
        "sourceLang": "ko",
        "total": len(data),
    }


def main() -> None:
    all_translation_rows: list[dict[str, str]] = []

    for filename in TOUR_FILES:
        translated, translation_rows = translate_tour_file(DATA_DIR / filename)
        output_name = filename.replace(".json", "_en.json")
        write_json(DATA_DIR / output_name, translated)
        all_translation_rows.extend(translation_rows)

    restaurants = translate_restaurants(DATA_DIR / "서울_맛집.json")
    write_json(DATA_DIR / "서울_맛집_en.json", restaurants)

    write_json(
        DATA_DIR / "tour_item_translations.json",
        {
            "lang": "en",
            "sourceLang": "ko",
            "generator": "scripts/generate_english_data.py",
            "items": all_translation_rows,
        },
    )

    print(f"Wrote {len(TOUR_FILES) + 2} generated files.")
    print(f"Wrote {len(all_translation_rows)} tour item translation rows.")


if __name__ == "__main__":
    main()
