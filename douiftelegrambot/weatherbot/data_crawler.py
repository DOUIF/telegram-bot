import json
from dataclasses import dataclass, field

import requests

from .apis import APIs as API_URL


@dataclass
class DataCrawler:
    __api_token: str = field(default="CWB-79DFE6D9-0EFB-4F48-947B-01982F16C096", init=False)
    __api_url: API_URL = field(default_factory=API_URL, init=False)

    def get_today_forecast(self, location: str) -> dict:
        param = {
            "locationName": location,
            "elementName": "WeatherDescription",
        }
        url = self.__api_url.get_url("WEEK_FORECAST", location=location)
        return self.__get_data_from_url(url, param)

    def __get_data_from_url(self, url: str, param: dict) -> dict:
        param.update({"Authorization": self.__api_token})
        result = requests.get(url=url, params=param)
        if result.status_code == 200:
            result_json = json.loads(result.text)
            data = result_json["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][:2]
            return {"result": data}
        else:
            print("Fetching data failed.")


if __name__ == "__main__":
    pass
