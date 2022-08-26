from dataclasses import dataclass, field
from multiprocessing import Queue

from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update


@dataclass
class BasicCommand:
    __request_queue: Queue
    __result_queue: Queue
    __command_dict: dict = field(init=False)

    def __post_init__(self) -> None:
        self.__command_dict = {
            "hello": self.__command_hello,
        }

    def get_all_command(self) -> dict:
        return self.__command_dict

    def __command_hello(self, update: Update, callback_context: CallbackContext) -> None:
        user_name = update.message.from_user.first_name
        update.message.reply_text(f"Hello {user_name}, how can I help you?")

    def call_back_query_handler(self, update: Update, context: CallbackContext):
        message = update.callback_query.data
        print("basic:" + message)
