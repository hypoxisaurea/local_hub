# TourAPI 4.0 Source Data Schema

Field definitions for the original JSON files collected from the Korea Tourism Organization TourAPI 4.0.

---

## Top-Level File Structure

| Field | Type | Description |
|------|------|-------------|
| `region` | string | Collected region name |
| `contentType` | string | Korean content type name |
| `contentTypeId` | string | Content type ID |
| `total` | integer | Total item count |
| `items` | object[] | POI item array |

## contentTypeId Codes

| ID | Type |
|----|------|
| 12 | Attractions |
| 14 | Cultural Facilities |
| 15 | Festivals & Performances |
| 25 | Travel Courses |
| 28 | Leisure Sports |
| 32 | Accommodation |
| 38 | Shopping |
| 39 | Restaurants |

---

## items[] Fields

| Field | Type | Description |
|------|------|-------------|
| `contentid` | string | Unique content ID |
| `contenttypeid` | string | Content type ID |
| `title` | string | Place name |
| `addr1` | string | Address, road-name or land-lot format |
| `addr2` | string | Detailed address, such as building name |
| `zipcode` | string | Postal code |
| `tel` | string | Phone number |
| `mapx` | string | Longitude (WGS84) |
| `mapy` | string | Latitude (WGS84) |
| `mlevel` | string | Map level |
| `areacode` | string | Area code |
| `sigungucode` | string | District/city/county code |
| `lDongRegnCd` | string | Legal-dong region code |
| `lDongSignguCd` | string | Legal-dong district code |
| `cat1` | string | Major category code |
| `cat2` | string | Middle category code |
| `cat3` | string | Subcategory code |
| `lclsSystm1` | string | Classification system 1 |
| `lclsSystm2` | string | Classification system 2 |
| `lclsSystm3` | string | Classification system 3 |
| `firstimage` | string | Main image URL |
| `firstimage2` | string | Thumbnail image URL |
| `cpyrhtDivCd` | string | Copyright division code |
| `createdtime` | string | Initial registration timestamp (YYYYMMDDHHmmss) |
| `modifiedtime` | string | Last modified timestamp (YYYYMMDDHHmmss) |

---

## Notes

- `mapx` and `mapy` are stored as strings and should be converted to floats when used.
- Empty `firstimage` values (`""`) mean no image is available.
- Empty `addr1` values mean address information was not provided.
- Category code definitions for `cat1~3` and `lclsSystm1~3` are available in the parent directory's `lclsSystemCode.json`.
