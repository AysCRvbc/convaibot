import random

import vklib
import db_worker
import prompts

vk = vklib.Bot()
db = db_worker.BotDatabase("data/db.sqlite")


def get_bot():
    return vk


MESSAGES_SCAN_LIMIT = 100


def owner_check(msg: vklib.Message):
    return str(msg.from_id) in vk.owners


vk.admin_check = owner_check


@vk.command("=беседа", enable_gm=True, enable_dm=False, admin=True)
def conv_add(msg: vklib.Message):
    conv_name = msg.text.split(' ', 1)[1]
    db.add_conversation(msg.peer_id, msg.from_id, conv_name, "Здесь нет описания")
    msg.answer("Беседа " + conv_name + " добавлена!")


@vk.command("=беседы", enable_gm=True, enable_dm=True, admin=True)
def conv_list(msg: vklib.Message):
    convs = db.get_conversations_by_bind_id(msg.from_id)

    if len(convs) == 0:
        msg.answer("У вас нет созданных бесед")
    else:
        msg.answer(f"Ваши беседы: {''.join([str(c) for c in convs])} \n\nВсего бесед: {len(convs)}")


def get_messages(msg: vklib.Message, limit=MESSAGES_SCAN_LIMIT, minimum=10, arg_i=1):
    chat = msg.peer_id
    if msg.is_dm:
        chat = int(msg.text.split(' ', arg_i)[arg_i])
        if not db.exists_conversation_by_id(chat):
            msg.answer("Беседа не найдена")
            return False

    messages = db.get_all_messages_for_conversation(chat)
    messages.sort(key=lambda x: x['date'])
    messages = messages[1 - limit:]

    if len(messages) < minimum:
        msg.answer("Недостаточно сообщений", reply=True)
        return False

    messages_new = []

    for i, m in enumerate(messages):
        if i == 0:
            continue

        new_m = {
            "date": m['date'] - messages[i - 1]['date'],
            "text": m['text']
        }

        messages_new.append(new_m)

    messages_new.append(messages[-1])
    messages = messages_new

    return messages


@vk.command("=запрос", enable_gm=True, enable_dm=True, admin=True)
def conv_request(msg: vklib.Message):
    messages = get_messages(msg)
    if messages is False:
        return

    vk.vk.messages.setActivity(type='typing', user_id=msg.from_id)

    try:
        answer = prompts.request(messages)
    except:
        msg.answer("Мне лень читать, давайте позже")
        return

    msg.answer(answer, reply=True)


@vk.command("=опиши", enable_gm=True, enable_dm=True, admin=True)
def conv_description(msg: vklib.Message):
    messages = get_messages(msg)
    if messages is False:
        return

    vk.vk.messages.setActivity(type='typing', user_id=msg.from_id)
    try:
        answer = prompts.rate(messages)
    except:
        msg.answer("Мне лень читать, давайте позже")
        return

    msg.answer(answer, dm=True)


@vk.command("=ответ", enable_gm=True, enable_dm=True, admin=True)
def conv_answer(msg: vklib.Message):
    nickname = msg.text.split(' ', 3)
    nickname = f"{nickname[1]} {nickname[2]}".lower()
    if not nickname:
        msg.answer("Нужно указать имя \n(Пример - =ответь Стас Стасов)")
        return

    messages = get_messages(msg, limit=300, minimum=10, arg_i=3)
    if messages is False:
        return

    center = []

    for m in messages:
        text = m['text']
        nick = text.split(':', 1)[0].lower()
        if nick == nickname:
            center.append(m)

    random.shuffle(center)
    center = center[:20]
    messages = messages[-20:]

    if len(center) == 0:
        msg.answer("Пользователь не найден")
        return

    vk.vk.messages.setActivity(type='typing', user_id=msg.peer_id)

    try:
        answer = prompts.impersonate(messages, center, nickname)
    except:
        msg.answer("Мне лень читать, давайте позже")
        return

    if "<ans>" not in answer:
        msg.answer("Произошла ошибка. Попробуйте позже")

    answer = answer.split("<ans>", 1)[1].split("</ans>")[0]
    msg.answer(answer)


@vk.command("=стоп", enable_gm=True, enable_dm=True, admin=True)
def stop(msg: vklib.Message):
    msg.answer("Бот остановлен")
    db.close()
    vk.stop()
    raise SystemExit


@vk.command(r".*", enable_gm=True, enable_dm=False, regex=True)
def conv_msg(msg: vklib.Message):
    peer_id = msg.peer_id
    from_id = msg.from_id

    if not db.exists_conversation_by_id(peer_id) or from_id < 0 or not msg.text:
        return

    user_name = vk.vk.users.get(user_ids=from_id)[0]['first_name'] + ' ' + vk.vk.users.get(user_ids=from_id)[0][
        'last_name']

    message = {
        "text": user_name + ": " + msg.text[:255],
        "date": msg.time
    }

    db.insert_json_message(peer_id, message)
