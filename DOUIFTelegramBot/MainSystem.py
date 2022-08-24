from dataclasses import dataclass, field
import sys

from .WeatherBot import Controller as WC


class MainSystem:
    __weather_controller: WC.WeatherDataController = WC.WeatherDataController()

    def __post_init__(self):
        print(f"{self.__weather_controller=}")

    def __call__(self):
        return self

    def start_system(self):
        self.__weather_controller.get_36hour_forecast(locationName="高雄市")


sys.modules[__name__] = MainSystem()
