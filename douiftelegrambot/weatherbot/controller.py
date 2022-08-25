from dataclasses import dataclass, field

from .data_crawler import DataCrawler


@dataclass
class WeatherDataController:
    __data_crawler: DataCrawler = DataCrawler()

    def get_36hour_forecast(self, **kwargs) -> dict:
        data = self.__data_crawler.get_36hour_forecast(**kwargs)
