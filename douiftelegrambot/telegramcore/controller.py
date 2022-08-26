from multiprocessing import Process, Queue
from threading import Thread
from time import sleep

from telegram.ext import CommandHandler, Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update


class TelegramController(Process):
    def __init__(self, __bot_request_queue: Queue, __bot_result_queue: Queue) -> None:
        super().__init__()
        self.__telegram_token = "5758390052:AAGiJesqjh9G_jkJtXo1zViMzoHdxmbg9ew"
        self.__request_queue = __bot_request_queue
        self.__result_queue = __bot_result_queue

    # MultiProcess start entry
    def run(self):
        self.__updater = Updater(self.__telegram_token)
        self.__command_dict = {
            "hello": self.__bot_command_hello,
        }
        self.__init_updater_command()
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

        # polling_thread.join()

    def __start_polling(self):
        self.__updater.start_polling()
        # self.__updater.idle()

    def __init_updater_command(self) -> None:
        for _command, _function in self.__command_dict.items():
            self.__updater.dispatcher.add_handler(CommandHandler(_command, _function))

    def __bot_command_hello(self, update: Update, callback_context: CallbackContext) -> None:
        user_name = update.message.from_user.first_name
        update.message.reply_text(f"Hello {user_name}, how can I help you?")
