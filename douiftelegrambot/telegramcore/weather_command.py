from copy import deepcopy
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
            "weather": self.__command_weather,
        }

    def get_all_command(self) -> dict:
        return self.__command_dict

    def __command_weather(self, update: Update, context: CallbackContext) -> None:
        context.user_data["command_type"] = "weather"
        context.user_data["command"] = []
        _reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("天氣", callback_data="forecast"),
                    InlineKeyboardButton("紫外線", callback_data="uvi"),
                ]
            ]
        )
        update.message.reply_text(f"想查詢哪種天氣功能？", reply_markup=_reply_markup)

    def call_back_query_handler(self, update: Update, context: CallbackContext) -> None:
        command = context.user_data.get("command")
        if command[0] == "forecast":
            self.__call_back_forecast(update, context)
        elif command[0] == "uvi":
            pass

    def __call_back_forecast(self, update: Update, context: CallbackContext) -> None:
        command = context.user_data.get("command")
        if len(command) == 1:
            _reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("今日", callback_data="today"),
                        InlineKeyboardButton("本周", callback_data="week"),
                    ]
                ]
            )
            update.callback_query.edit_message_text("想瞭解甚麼時候的天氣預報？", reply_markup=_reply_markup)
        elif len(command) == 2:
            location = [
                ["基隆市", "新北市", "臺北市"],
                ["宜蘭縣", "花蓮縣", "臺東縣"],
                ["桃園市", "新竹縣", "新竹市"],
                ["苗栗縣", "臺中市", "南投縣"],
                ["彰化縣", "雲林縣"],
                ["嘉義市", "嘉義市"],
                ["臺南市", "高雄市", "屏東縣"],
                ["澎湖縣", "連江縣", "金門縣"],
            ]
            inline_button = []
            for loca_area in location:
                button_row = []
                for loca in loca_area:
                    button_row.append(InlineKeyboardButton(loca, callback_data=loca))
                inline_button.append(button_row)

            _reply_markup = InlineKeyboardMarkup(inline_button)
            update.callback_query.edit_message_text("請選擇想查詢的區域？", reply_markup=_reply_markup)
        elif len(command) == 3:
            request = {
                "command_type": "weather",
                "command": context.user_data.get("command"),
                "user_id": update.callback_query.from_user.id,
                "chat_id": update.callback_query.message.chat_id,
            }
            self.__request_queue.put(request)
            location = context.user_data.get("command")[2]
            update.callback_query.edit_message_text(f"查詢 {location} 的天氣預報", reply_markup=None)

    def __call_back_uvi(self) -> None:
        pass
