from time import sleep
from multiprocessing import Process, Queue

from .data_crawler import DataCrawler


class WeatherDataController(Process):
    def __init__(self, __bot_request_queue: Queue, __bot_result_queue: Queue) -> None:
        super().__init__()
        self.__request_queue = __bot_request_queue
        self.__result_queue = __bot_result_queue
        self.__data_crawler = DataCrawler()

    # MultiProcess start entry
    def run(self):
        while True:
            if not self.__request_queue:
                sleep(0.1)
                continue
            request = self.__request_queue.get()
            if request["command"] == "stop":
                print("Close process: weather_controller")
                break

    def get_36hour_forecast(self, **kwargs) -> dict:
        data = self.__data_crawler.get_36hour_forecast(**kwargs)
