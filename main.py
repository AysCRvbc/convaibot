import os
import json


def start():
    if not os.path.exists("config"):
        os.mkdir("config")
    if not os.path.exists("config/config.json"):
        config = {
            "token": None,
        }
        json.dump(config, open("config/config.json", "w"))

    config = json.load(open("config/config.json", "r"))

    if config["token"] is None:
        print("Please set your token in config/config.json")


if __name__ == "__main__":
    start()
