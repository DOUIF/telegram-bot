import douiftelegrambot
import json
from pathlib import Path

TOKEN_FILEPATH = f"{Path(__file__).parent}/token.json"


def main() -> None:
    print("Start System.")
    token = read_token()
    main_system = douiftelegrambot.MainSystem(token)
    print("Initial finish.")
    main_system.start_system()


def read_token() -> dict:
    result = json.load(open(TOKEN_FILEPATH, mode="r", encoding="utf8"))
    return result


if __name__ == "__main__":
    main()
