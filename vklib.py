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
        self.from_id = event.message['from_id']
        self.peer_id = event.message['peer_id']
        self.is_dm = event.message['from_id'] == event.message['peer_id']
        self.time = event.message['date']

    def answer(self, text, reply=False, dm=False):
        chat = self.event.message['peer_id']
        if dm:
            chat = self.from_id
            reply = False

        kwargs = {"reply_to": self.message_id} if reply else {}
        self.bot.vk.messages.send(
            peer_id=chat,
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
        self.working = True

        self.commands: list[Command] = []
        self.default_command = None
        self.admin_check = None

    def set_config(self, config):
        self.token = config.token
        self.group_id = config.group_id

    def stop(self):
        self.working = False

    def auth(self):
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, self.group_id)

    def command(self, name: str, aliases=None, enable_dm=True, enable_gm=True, regex=False, admin=False):
        if aliases is None:
            aliases = []

        args = name

        def wrapper(func):
            self.commands.append(Command(name=args,
                                         aliases=aliases,
                                         enable_dm=enable_dm,
                                         enable_gm=enable_gm,
                                         regex=regex,
                                         handler=func,
                                         admin=admin
                                         )
                                 )

        return wrapper

    def start(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = Message(self, event)
                cmd = None

                for cmd in self.commands:
                    is_dm = msg.is_dm

                    if is_dm and not cmd.enable_dm:
                        continue
                    if not is_dm and not cmd.enable_gm:
                        continue

                    if cmd.is_call(msg.text):
                        break
                else:
                    if not msg.is_dm:
                        continue
                    if self.default_command is not None:
                        cmd: Command = self.default_command

                if cmd is None:
                    continue

                if cmd.admin:
                    if not self.admin_check(msg):
                        continue

                cmd.handler(msg)


class Command:
    def __init__(self, name, handler, aliases=None, enable_dm=True, enable_gm=True, regex=False, admin=False):
        if aliases is None:
            aliases = []
        self.names = [name] + aliases
        self.handler = handler
        self.regex = regex
        self.enable_dm = enable_dm
        self.enable_gm = enable_gm
        self.admin = admin

    def is_call(self, text):
        if not self.regex:
            return text.split()[0] in self.names
        else:
            for name in self.names:
                if re.match(name, text):
                    return True
            return False
