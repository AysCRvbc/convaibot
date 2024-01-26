import os
import json
import bot
import vklib


def start():
    if not os.path.exists("config"):
        os.mkdir("config")
    if not os.path.exists("config/config.json"):
        config = {
            "token": None,
            "group_id": None
        }
        json.dump(config, open("config/config.json", "w"))

    config = json.load(open("config/config.json", "r"))

    if config["token"] is None:
        print("Please set your token in config/config.json")
        return

    if config["group_id"] is None:
        print("Please set your group id in config/config.json")
        return

    token = config["token"]
    group_id = config["group_id"]

    vk = bot.get_bot()
    bot_config = vklib.BotConfig(token, group_id)
    vk.set_config(bot_config)
    vk.auth()

    while True:
        try:
            vk.start()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    start()
