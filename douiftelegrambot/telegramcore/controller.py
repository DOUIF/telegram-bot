from multiprocessing import Process, Queue
from threading import Thread
from time import sleep

from telegram.ext import CommandHandler, Updater, CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from .basic_command import BasicCommand
from .weather_command import WeatherCommand


class TelegramController(Process):
    def __init__(self, __bot_request_queue: Queue, __bot_result_queue: Queue) -> None:
        super().__init__()
        self.__telegram_token = "5758390052:AAGiJesqjh9G_jkJtXo1zViMzoHdxmbg9ew"
        self.__request_queue = __bot_request_queue
        self.__result_queue = __bot_result_queue

    # MultiProcess start entry
    def run(self):
        self.__process_init()

        polling_thread = Thread(target=self.__start_polling)
        polling_thread.start()

        while True:
            sleep(0.1)
            if not self.__result_queue:
                sleep(0.1)
                continue
            result = self.__result_queue.get()
            if result["command"] == "stop":
                print("Close process: telegram_controller")
                self.__updater.stop()
                break

        polling_thread.join()

    def __process_init(self):
        self.__updater = Updater(self.__telegram_token)

        self.__weather_command = WeatherCommand(self.__request_queue, self.__result_queue)
        self.__basic_command = BasicCommand(self.__request_queue, self.__result_queue)

        self.__call_back_query_function_dict = {
            "basic": self.__basic_command.call_back_query_handler,
            "weather": self.__weather_command.call_back_query_handler,
        }
        self.__init_command_dispatcher()

    def __start_polling(self):
        self.__updater.start_polling()

    def __init_command_dispatcher(self) -> None:
        all_command_dict = dict()
        all_command_dict.update(self.__basic_command.get_all_command())
        all_command_dict.update(self.__weather_command.get_all_command())

        for _command, _function in all_command_dict.items():
            self.__updater.dispatcher.add_handler(CommandHandler(_command, _function))

        self.__updater.dispatcher.add_handler(CallbackQueryHandler(self.__call_back_query_handler))

    def __call_back_query_handler(self, update: Update, context: CallbackContext):
        data = eval(update.callback_query.data)
        command_type = data["command_type"]
        if command_type in self.__call_back_query_function_dict:
            self.__call_back_query_function_dict[command_type](update, data)
