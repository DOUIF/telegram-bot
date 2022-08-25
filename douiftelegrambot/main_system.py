from dataclasses import dataclass, field
import sys

from . import weatherbot


@dataclass
class MainSystem:
    __weather_controller: weatherbot.WeatherDataController = field(
        default_factory=weatherbot.WeatherDataController
    )

    def __post_init__(self):
        print(f"{self.__weather_controller=}")

    def start_system(self):
        self.__weather_controller.get_36hour_forecast(locationName="高雄市")
