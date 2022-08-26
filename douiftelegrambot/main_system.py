import sys
from dataclasses import dataclass, field
from multiprocessing import Queue

from . import telegramcore, weatherbot


@dataclass
class MainSystem:
    __weather_controller: weatherbot.WeatherDataController = field(default=None, init=False)
    __telegram_controller: telegramcore.TelegramController = field(default=None, init=False)
    __telegram_request_queue: Queue = field(default_factory=Queue, init=False)
    __telegram_result_queue: Queue = field(default_factory=Queue, init=False)
    __weather_request_queue: Queue = field(default_factory=Queue, init=False)
    __weather_result_queue: Queue = field(default_factory=Queue, init=False)

    def __post_init__(self):
        print("Init class: weather_controller...")
        self.__weather_controller = weatherbot.WeatherDataController(
            self.__weather_request_queue,
            self.__weather_result_queue,
        )
        print("Init class: telegram_controller...")
        self.__telegram_controller = telegramcore.TelegramController(
            self.__telegram_request_queue,
            self.__telegram_result_queue,
        )

    def __read_command(self):
        while True:
            command = input("Enter command: ")
            if command == "stop":
                self.__telegram_result_queue.put({"command": "stop"})
                self.__weather_request_queue.put({"command": "stop"})
                break
        self.__telegram_controller.join()
        self.__weather_controller.join()
        print("Main system shut down. All Process are joined.")

    def start_system(self):
        print("Start process: weather_controller...")
        self.__weather_controller.start()
        print("Start process: telegram_controller...")
        self.__telegram_controller.start()

        # self.__weather_controller.get_36hour_forecast(locationName="高雄市")

        self.__read_command()
