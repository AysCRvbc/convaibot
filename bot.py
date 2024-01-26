import vklib
import db_worker

vk = vklib.Bot()
db = db_worker.BotDatabase("data/db.sqlite")


def get_bot():
    return vk


owner = 540888551


@vk.command("/беседа", enable_gm=True, enable_dm=False)
def conv_add(msg: vklib.Message):
    conv_name = msg.text.split(' ', 1)[1]
    db.add_conversation(msg.peer_id, msg.from_id, conv_name, "Здесь нет описания")
    msg.answer("Беседа " + conv_name + " добавлена!")


@vk.command("/беседы", enable_gm=True, enable_dm=True)
def conv_list(msg: vklib.Message):
    convs = db.get_conversations_by_bind_id(msg.from_id)

    if len(convs) == 0:
        msg.answer("У вас нет созданных бесед")
    else:
        msg.answer(f"Ваши беседы: {convs}")


@vk.command("/сообщения", enable_gm=True, enable_dm=False)
def conv_show(msg: vklib.Message):
    convs = db.get_all_messages_for_conversation(msg.peer_id)
    msg.answer(convs)


@vk.command("/стоп", enable_gm=True, enable_dm=True)
def stop(msg: vklib.Message):
    msg.answer("Бот остановлен")
    db.close()
    vk.stop()
    raise SystemExit


@vk.command(r".*", enable_gm=True, enable_dm=False, regex=True)
def conv_msg(msg: vklib.Message):
    peer_id = msg.peer_id
    if not db.exists_conversation_by_id(peer_id):
        return
    from_id = msg.from_id
    user_name = vk.vk.users.get(user_ids=from_id)[0]['first_name'] + ' ' + vk.vk.users.get(user_ids=from_id)[0][
        'last_name']

    message = {
        "text": user_name + ": " + msg.text,
        "date": msg.time
    }

    db.insert_json_message(peer_id, message)
