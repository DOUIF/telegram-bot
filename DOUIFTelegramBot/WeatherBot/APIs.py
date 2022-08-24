from dataclasses import dataclass, field
import json
from pathlib import Path

CURRENT_PATH = Path(__file__).parent
API_JSON_FILE = f"{CURRENT_PATH}\\APIs.json"


@dataclass
class APIs:
    __HOST_URL: str = field(init=False)
    __API_URL: dict = field(init=False)

    def __post_init__(self):
        api_json = json.load(open(API_JSON_FILE, "r"))
        self.__HOST_URL = api_json["HOST_URL"]
        self.__API_URL = api_json["API_URL"]

    def get_url(self, api_name: str) -> str:
        if api_name in self.__API_URL:
            return f"{self.__HOST_URL}/{self.__API_URL[api_name]}"
        else:
            return None
