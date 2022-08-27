from dataclasses import dataclass, field
from enum import Enum


class OpenDataInfo:
    api_host = "https://opendata.cwb.gov.tw/api/v1/rest/datastore"
    week_forecast_url = "F-D0047-091"
    T = "溫度"
    Td = "露點溫度"
    AT = "體感溫度"
    PoP = "降雨機率"
    RH = "相對濕度"
    WD = "風向"
    UVI = "紫外線指數"
    CI = "舒適度指數"
    Wx = "天氣現象"
    WeatherDescription = "天氣預報綜合描述"
    three_day_location_id: dict[str:str] = {
        "宜蘭縣": "F-D0047-001",
        "桃園市": "F-D0047-005",
        "新竹縣": "F-D0047-009",
        "苗栗縣": "F-D0047-013",
        "彰化縣": "F-D0047-017",
        "南投縣": "F-D0047-021",
        "雲林縣": "F-D0047-025",
        "嘉義縣": "F-D0047-029",
        "屏東縣": "F-D0047-033",
        "臺東縣": "F-D0047-037",
        "花蓮縣": "F-D0047-041",
        "澎湖縣": "F-D0047-045",
        "基隆市": "F-D0047-049",
        "新竹市": "F-D0047-053",
        "嘉義市": "F-D0047-057",
        "臺北市": "F-D0047-061",
        "高雄市": "F-D0047-065",
        "新北市": "F-D0047-069",
        "臺中市": "F-D0047-073",
        "臺南市": "F-D0047-077",
        "連江縣": "F-D0047-081",
        "金門縣": "F-D0047-085",
    }
    week_location_id: dict[str:str] = {
        "宜蘭縣": "F-D0047-003",
        "桃園市": "F-D0047-007",
        "新竹縣": "F-D0047-011",
        "苗栗縣": "F-D0047-015",
        "彰化縣": "F-D0047-019",
        "南投縣": "F-D0047-023",
        "雲林縣": "F-D0047-027",
        "嘉義縣": "F-D0047-031",
        "屏東縣": "F-D0047-035",
        "臺東縣": "F-D0047-039",
        "花蓮縣": "F-D0047-043",
        "澎湖縣": "F-D0047-047",
        "基隆市": "F-D0047-051",
        "新竹市": "F-D0047-055",
        "嘉義市": "F-D0047-059",
        "臺北市": "F-D0047-063",
        "高雄市": "F-D0047-067",
        "新北市": "F-D0047-071",
        "臺中市": "F-D0047-075",
        "臺南市": "F-D0047-079",
        "連江縣": "F-D0047-083",
        "金門縣": "F-D0047-087",
    }


@dataclass
class APIs:
    def __post_init__(self):
        pass

    def get_url(self, url_type: str, **kwargs) -> str:
        if url_type == "WEEK_FORECAST":
            location = kwargs["location"]
            url = f"{OpenDataInfo.api_host}/{OpenDataInfo.week_forecast_url}"
            return url
