import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import re
import random


class BotConfig:
    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id


class Message:
    def __init__(self, bot, event):
        self.bot = bot
        self.event = event

        self.text = event.message['text']
        self.message_id = event.message['id']

    def answer(self, text, reply=False):
        kwargs = {"reply_to": self.message_id} if reply else {}
        self.bot.vk.messages.send(
            peer_id=self.event.message['peer_id'],
            random_id=random.randint(-2147483648, 2147483647),
            message=text,
            **kwargs
        )


class Bot:
    def __init__(self):
        self.token = None
        self.group_id = None
        self.vk_session = None
        self.vk = None
        self.longpoll = None

        self.commands = []
        self.default_command = None

    def set_config(self, config):
        self.token = config.token
        self.group_id = config.group_id

    def auth(self):
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, self.group_id)

    def command(self, *args, **kwargs):
        def wrapper(func):
            self.commands.append(Command(*args, **kwargs, handler=func))

        return wrapper

    def start(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = Message(self, event)
                for cmd in self.commands:
                    if cmd.is_call(msg.text):
                        cmd.handler(msg)
                        break
                else:
                    if self.default_command is not None:
                        self.default_command(msg)


class Command:
    def __init__(self, name, handler, aliases=None, enable_dm=True, enable_gm=True, regex=False):
        if aliases is None:
            aliases = []
        self.names = [name] + aliases
        self.handler = handler
        self.regex = regex
        self.enable_dm = enable_dm
        self.enable_gm = enable_gm

    def is_call(self, text):
        if not self.regex:
            return text.split()[0] in self.names
        else:
            for name in self.names:
                if re.match(name, text):
                    return True
            return False
