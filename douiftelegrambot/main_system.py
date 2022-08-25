from dataclasses import dataclass, field
import sys

from . import weatherbot
from . import telegramcore


@dataclass
class MainSystem:
    __weather_controller: weatherbot.WeatherDataController = field(default_factory=weatherbot.WeatherDataController, init=False)
    __telegram_controller: telegramcore.TelegramController = field(default_factory=telegramcore.TelegramController, init=False)

    def __post_init__(self):
        print(f"{self.__weather_controller=}")

    def start_system(self):
        self.__weather_controller.get_36hour_forecast(locationName="高雄市")
