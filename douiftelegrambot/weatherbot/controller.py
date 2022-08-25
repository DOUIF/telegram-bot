from dataclasses import dataclass, field

from .data_crawler import DataCrawler


@dataclass
class WeatherDataController:
    __data_crawler: DataCrawler = field(default_factory=DataCrawler, init=False)

    def get_36hour_forecast(self, **kwargs) -> dict:
        data = self.__data_crawler.get_36hour_forecast(**kwargs)
