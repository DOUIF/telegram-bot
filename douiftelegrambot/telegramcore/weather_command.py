from dataclasses import dataclass, field
from multiprocessing import Queue

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update


@dataclass
class WeatherCommand:
    __request_queue: Queue
    __result_queue: Queue
    __command_dict: dict = field(init=False)

    def __post_init__(self) -> None:
        self.__command_dict = {
            "weather": self.__command_weather_today,
        }

    def get_all_command(self) -> dict:
        return self.__command_dict

    def call_back_query_handler(self, update: Update, context: CallbackContext):
        message = update.callback_query.data
        print("weather:" + message)

    def __command_weather_today(self, update: Update, callback_context: CallbackContext) -> None:
        today_dict = {"command_type": "weather", "data": "1"}
        week_dict = {"command_type": "weather", "data": "2"}
        _reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Today", callback_data=str(today_dict)),
                    InlineKeyboardButton("Week", callback_data=str(week_dict)),
                ]
            ]
        )
        update.message.reply_text(f"What do you want to know about weather?", reply_markup=_reply_markup)
