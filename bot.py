import vklib

vk = vklib.Bot()


def get_bot():
    return vk


email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


@vk.command(name=email_regex, regex=True)
def email(msg: vklib.Message):
    msg.answer("Вы отправили электронную почту: " + msg.text)
