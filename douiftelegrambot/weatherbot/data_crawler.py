import json
from dataclasses import dataclass, field

import requests
from .apis import APIs as API_URL
from pathlib import Path


@dataclass
class DataCrawler:
    __api_token: str = "CWB-79DFE6D9-0EFB-4F48-947B-01982F16C096"
    __api_url: API_URL = API_URL()

    def get_36hour_forecast(self, **kwargs) -> dict:
        print(kwargs)
        url = self.__api_url.get_url("36HOUR_FORECAST")
        self.__get_data_from_url(url, kwargs)

    def __get_data_from_url(self, url: str, param: dict) -> dict:
        param["Authorization"] = self.__api_token
        data = requests.get(url=url, params=param)
        if data.status_code == 200:
            print(json.loads(data.text))

        else:
            print("Fetching data failed.")


if __name__ == "__main__":
    pass
