from dataclasses import dataclass
from pathlib import Path

CURRENT_PATH = Path(__file__).parent
API_JSON_FILE = f"{CURRENT_PATH}\\APIs.json"


@dataclass
class APIs:
    __HOST_URL: str = "https://opendata.cwb.gov.tw/api"
    __API_URL: dict = {
        "36HOUR_FORECAST": "v1/rest/datastore/F-C0032-001",
    }

    def get_url(self, api_name: str) -> str:
        if api_name in self.__API_URL:
            return f"{self.__HOST_URL}/{self.__API_URL[api_name]}"
        else:
            return None
