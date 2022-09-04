from time import sleep
from multiprocessing import Process, Queue

from .data_crawler import DataCrawler
from datetime import datetime


class WeatherDataController(Process):
    def __init__(self, __token:str, __bot_request_queue: Queue, __bot_result_queue: Queue) -> None:
        super().__init__()
        self.__request_queue = __bot_request_queue
        self.__result_queue = __bot_result_queue
        self.__data_crawler = DataCrawler(__token)

    # MultiProcess start entry
    def run(self) -> None:
        while True:
            if self.__request_queue.empty():
                sleep(0.1)
                continue
            request = self.__request_queue.get()
            print(f"inside weather: {request=}")
            command = request["command"]
            if command[0] == "stop":
                print("Close process: weather_controller")
                break
            elif command[0] == "forecast":
                self.__get_forecast(request)

    def __return_weather_result(self, request: dict[str:any], result: str) -> None:
        return_dict = {
            "command_type": "telegram",
            "command": ["send"],
            "message": result,
            "chat_id": request["chat_id"],
        }
        self.__result_queue.put(return_dict)

    def __get_forecast(self, request: dict[str:any]) -> dict:
        search_type = request["command"][1]
        location = request["command"][2]
        if search_type == "today":
            data = self.__data_crawler.get_today_forecast(location)
            result = []
            for element in data["result"]:
                start_time = datetime.strptime(element["startTime"], "%Y-%m-%d %H:%M:%S")
                if 6 <= start_time.hour < 18:
                    start_time = start_time.strftime("%m月%d號 白天")
                else:
                    start_time = start_time.strftime("%m月%d號 晚間")
                description = element["elementValue"][0]["value"]
                result.append(f"{start_time}: {description}")

            self.__return_weather_result(request, "\n".join(result))

        elif search_type == "week":
            pass
