from DOUIFTelegramBot import MainSystem


def main():
    print("Start System.")
    main_system = MainSystem()
    print(f"{main_system=}")
    print("Initial finish.")
    main_system.start_system()


if __name__ == "__main__":
    main()
