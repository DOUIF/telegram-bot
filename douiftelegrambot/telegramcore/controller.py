from dataclasses import dataclass, field
from telegram.ext import Updater, CommandHandler
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext


@dataclass
class TelegramController:
    __telegram_token: str = field(default="5758390052:AAGiJesqjh9G_jkJtXo1zViMzoHdxmbg9ew", init=False)
    __updater: Updater = field(init=False)
    __command_dict: dict = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.__updater = Updater(self.__telegram_token)
        self.__init_updater_command()
        self.__updater.start_polling()
        self.__updater.idle()

    def __init_updater_command(self) -> None:
        self.__command_dict = {
            "hello": self.__bot_command_hello,
        }
        for _command, _function in self.__command_dict.items():
            self.__updater.dispatcher.add_handler(CommandHandler(_command, _function))

    def __bot_command_hello(self, update: Update, callback_context: CallbackContext) -> None:
        user_name = update.message.from_user.first_name
        update.message.reply_text(f"Hello {user_name}, how can I help you?")
