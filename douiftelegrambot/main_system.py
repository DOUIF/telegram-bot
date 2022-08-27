from dataclasses import dataclass, field
from multiprocessing import Queue
from threading import Thread
from time import sleep
from . import telegramcore, weatherbot
from random import random


@dataclass
class MainSystem:
    __weather_controller: weatherbot.WeatherDataController = field(default=None, init=False)
    __telegram_controller: telegramcore.TelegramController = field(default=None, init=False)
    __telegram_request_queue: Queue = field(default_factory=Queue, init=False)
    __telegram_result_queue: Queue = field(default_factory=Queue, init=False)
    __weather_request_queue: Queue = field(default_factory=Queue, init=False)
    __weather_result_queue: Queue = field(default_factory=Queue, init=False)
    __system_running: str = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.__init_telegram_controller()
        self.__init_weather_controller()

    def __init_telegram_controller(self) -> None:
        print("Init class: telegram_controller...")
        self.__telegram_request_queue = Queue()
        self.__telegram_result_queue = Queue()
        self.__telegram_controller = telegramcore.TelegramController(
            self.__telegram_request_queue,
            self.__telegram_result_queue,
        )

    def __init_weather_controller(self) -> None:
        print("Init class: weather_controller...")
        self.__weather_request_queue = Queue()
        self.__weather_result_queue = Queue()
        self.__weather_controller = weatherbot.WeatherDataController(
            self.__weather_request_queue,
            self.__weather_result_queue,
        )

    def __read_command(self) -> None:
        while True:
            self.__weather_request_queue.put({"command": "hello"})
            command = input("Enter command: ")
            if command == "stop":
                self.stop_system()
                break
            elif command == "restart":
                self.restart_telegram()

    def stop_system(self) -> None:
        self.__system_running = False
        self.__telegram_result_queue.put({"command": ["stop"]})
        self.__weather_request_queue.put({"command": ["stop"]})
        self.__telegram_controller.join()
        self.__weather_controller.join()
        self.__queue_manager_thread.join()
        print("Main system shut down. All process are joined.")

    def restart_telegram(self) -> None:
        self.__telegram_result_queue.put({"command": ["stop"]})
        self.__weather_request_queue.put({"command": ["stop"]})
        self.__telegram_controller.join()
        self.__weather_controller.join()
        self.__init_telegram_controller()
        self.__start_telegram_controller()
        self.__init_weather_controller()
        self.__start_weather_controller()

    def start_system(self) -> None:
        self.__system_running = True
        self.__start_telegram_controller()
        self.__start_weather_controller()
        self.__start_queue_manager()
        self.__read_command()

    def __start_telegram_controller(self) -> None:
        print("Start process: telegram_controller...")
        self.__telegram_controller.start()

    def __start_weather_controller(self) -> None:
        print("Start process: weather_controller...")
        self.__weather_controller.start()

    def __start_queue_manager(self) -> None:
        self.__queue_manager_thread = Thread(target=self.__queue_manager_handler)
        self.__queue_manager_thread.start()

    def __queue_manager_handler(self) -> None:
        while self.__system_running:
            sleep(random())
            if not self.__telegram_request_queue.empty():
                print("detect telegram request")
                telegram_request = self.__telegram_request_queue.get()
                command_type = telegram_request["command_type"]
                if command_type == "weather":
                    self.__weather_request_queue.put(telegram_request)

            if not self.__weather_result_queue.empty():
                print("detect weather result")
                weather_result = self.__weather_result_queue.get()
                print(f"main system: {weather_result=}")
                command_type = weather_result["command_type"]
                if command_type == "telegram":
                    self.__telegram_result_queue.put(weather_result)
