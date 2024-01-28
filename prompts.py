import gpt


@gpt.prompt
def request(messages):
    return {
        "system_context": "ОЧЕНЬ ВАЖНО: Ты получил список сообщений из реального чата. "
                          "Тебе нужно пересказать самые важные события из чата, если таковые есть. "
                          "Не пытайся говорить с пользователем, это не имеет смысла. "
                          "ТЫ - СИСТЕМА АНАЛИЗА БЕСЕД."
                          "ТВОЯ ЗАДАЧА: АНАЛИЗ БЕСЕДЫ ДЛЯ РАЗВЛЕЧЕНИЯ ЕЁ УЧАСТНИКОВ. "
                          "ПРОСТО ЧИТАЙ КОНТЕКСТ ПЕРЕПИСКИ, И ДЕЛАЙ ИЗ НЕЁ ВЫВОДЫ О СОБЫТИЯХ, КОТОРЫЕ ПРОИЗОШЛИ. "
                          "БУДЬ КАК МОЖНО БОЛЕЕ КРАТОК"
                          "НЕ БУДЬ ОСОБО СЕРЬЁЗЕН. СТАРАЙСЯ ПОВТОРИТЬ СТИЛЬ ОБЩЕНИЯ УЧАСТНИКОВ БЕСЕДЫ В СВОЕМ АНАЛИЗЕ."
                          "ВСЕ СОБЫТИЯ ДОЛЖНЫ БЫТЬ ЛИБО СМЕШНЫМИ, ЛИБО ВАЖНЫМИ, ЛИБО ИНТЕРЕСНЫМИ"
                          "В ТВОЕМ ОТВЕТЕ ДОЛЖНО БЫТЬ ПЕРЕЧИСЛЕНИЕ ЭТИХ СОБЫТИЙ И ТВОЙ КОММЕНТАРИЙ ПО ИХ ПОВОДУ НА РУССКОМ ЯЗЫКЕ."
                          "Список сообщений:\n",
        "text": "\n".join([m["text"] for m in messages])
    }


@gpt.prompt
def rate(messages):
    return {
        "system_context": "ОЧЕНЬ ВАЖНО: Ты получил список сообщений из реального чата. "
                          "Тебе нужно перечислить важных участников, после чего оценить их по своим критериям"
                          "Не пытайся говорить с пользователем, это не имеет смысла. "
                          "ТЫ - СИСТЕМА ОЦЕНКИ БЕСЕДЫ. "
                          "ТВОЯ ЗАДАЧА: ОЦЕНКА БЕСЕДЫ. "
                          "Список сообщений:\n",
        "text": "\n".join([m["text"] for m in messages])
    }


# @gpt.prompt
# def impersonate(messages, target_messages, parody):
#     system_context = ("Ты - система генерации сообщений, используемая для пародирующего чат-бота. Соблюдай шаги максимально точно и подробно."
#                       "Далее тебе будут переданы сообщения из беседы. "
#                       "Первый(1) список сообщений будет включать в себя СЛУЧАЙНЫЕ сообщения персонажа, которого ты будешь играть."
#                       "Используй эту информацию для того, чтобы пародировать стиль речи персонажа. Но не забывай, что это сообщения в совершенно случайном порядке."
#                       "Второй(2) список сообщений будет включать в себя сообщения из чата. "
#                       "Ты должен будешь выбрать одно сообщение, и, учитывая контекст, ответить на него")
#     text = ("Первый(1) список сообщений - случайные сообщения персонажа: \n\"\"\" " + "\n".join([m["text"] for m in target_messages]) + "\n\"\"\""
#             "Второй(2) список сообщений - сообщения из чата: \n\"\"\"" + "\n".join([m["text"] for m in messages]) + "\n\"\"\""
#             "Шаги выполнения твоей задачи пародирования персонажа:"
#                 "1 ШАГ: Определи манеру речи персонажа: " + parody + "\n"
#                 "2 ШАГ: Выбери только одно сообщение(Написанное кем-то другим, не твоим персонажем), на которое ты будешь отвечать из второго(2) списка сообщений. \n"
#                 "3 ШАГ: Выполни анализ выбранного сообщения: "
#                                                 "1) Кто написал это сообщение? "
#                                                 "2) Что именно это может значит в контексе этого чата? "
#                                                 "3) Кому это адресовано? "
#                                                 "4) Какое настроение у того, кто это писал? \n"
#                 "4 ШАГ: Выбери общую мысль персонажа, которую он должен сказать в ответ на то сообщение из второго(2) списка: \n"
#                 f"5 ШАГ: Повтори анализ сообщений персонажа: {parody}, но теперь выпиши 10 его полных сообщений, "
#                     f"которые будут характерны ему в контексе сообщения, на которое ты будешь отвечать \n"
#                 "6 ШАГ: Скопируй стиль написания сообщений персонажа " + parody + ". "
#                 "Учитывай характерные ему фразы, манеру, ошибки, построение сообщения, обращения, выражения и т.д. \n"
#                 "Сначала выпиши сообщение, на которое ты будешь отвечать. Является ли набросок сообщения связным ответом на это сообщение? "
#                 "Проанализируй - настолько ли стиль сгенерированного тобой сообщения соответсвует примерам из реальных сообщений персонажа. "
#                 "Критерии качественного ответа: 1) Связность текста 2) Правильное понимание стилистики персонажа 3) Правильное понимание контекста чата"
#                 "После написания наброска оцени его по этим критериям. \n"
#                 "Копирование стилистики - самая важная задача. Сделай набросок ответа на выбранное сообщение, используя стиль персонажа " + parody + "\n"
#                 "7 ШАГ: Сгенерируй только один ответ на выбранное тобой сообщение. Учитывай примеры сообщений из анализа сообщений персонажа " + parody + "\n"
#                 "Очень важно: Строго соблюдай стилистику сообщений из шага 5. Это значит, что если он не использует смайлики, то он их НЕ ИСПОЛЬЗУЕТ и так далее"
#                 "Должно выйти ТОЛЬКО ОДНО сообщение ТОЛЬКО ОТ ЛИЦА ТВОЕГО ПЕРСОНАЖА должно быть в формате <ans>{message}</ans>"
#             )
#     return {"system_context": system_context, "text": text}

@gpt.prompt
def impersonate(messages, target_messages, parody):
    system_context = ("You are a message generation system used for a parody chatbot. Follow the steps as accurately and detailed as possible."
                      "Next, you will be given messages from a conversation. "
                      "The first(1) list of messages will contain RANDOM messages from the character you'll be impersonating."
                      "Use this information to parody the character's speech style. But remember, these messages are in a completely random order."
                      "The second(2) list of messages will include chat messages. "
                      "You will need to choose one message, and considering the context, respond to it.")
    text = ("First(1) list of messages - random character messages: \n\"\"\" " + "\n".join([m["text"] for m in target_messages]) + "\n\"\"\""
                                                                                                                                   "Second(2) list of messages - chat messages: \n\"\"\"" + "\n".join([m["text"] for m in messages]) + "\n\"\"\""
                                                                                                                                                                                                                                       "Steps to perform your character impersonation task:"
                                                                                                                                                                                                                                       "1 Step: Identify the character's speech style: " + parody + "\n"
                                                                                                                                                                                                                                                                                                    "2 Step: Choose only one message (written by someone else, not your character) from the second(2) list of messages to respond to. \n"
                                                                                                                                                                                                                                                                                                    "3 Step: Analyze the selected message: "
                                                                                                                                                                                                                                                                                                    "1) Who wrote this message? "
                                                                                                                                                                                                                                                                                                    "2) What exactly could this mean in the context of this chat? "
                                                                                                                                                                                                                                                                                                    "3) To whom is it addressed? "
                                                                                                                                                                                                                                                                                                    "4) What mood does the writer convey? \n"
                                                                                                                                                                                                                                                                                                    "4 Step: Choose a general thought that the character should express in response to that message from the second(2) list: \n"
                                                                                                                                                                                                                                                                                                    f"5 Step: Repeat the analysis of the character's messages: {parody}, but now list 10 of his complete messages "
                                                                                                                                                                                                                                                                                                    f"that would be characteristic in the context of the message you are responding to \n"
                                                                                                                                                                                                                                                                                                    "6 Step: Copy the writing style of the character " + parody + ". "
                                                                                                                                                                                                                                                                                                                                                                  "Take into account his typical phrases, manner, errors, message structure, addressings, expressions, etc. \n"
                                                                                                                                                                                                                                                                                                                                                                  "Start by writing the message to which you will respond. Is the draft message a coherent response to this message? "
                                                                                                                                                                                                                                                                                                                                                                  "Analyze - does the style of the message you generated correspond closely to examples from the real messages of the character. "
                                                                                                                                                                                                                                                                                                                                                                  "Criteria for a quality response: 1) Coherence of the text 2) Correct understanding of the character's style 3) Correct understanding of the chat context"
                                                                                                                                                                                                                                                                                                                                                                  "After writing the draft, evaluate it based on these criteria. \n"
                                                                                                                                                                                                                                                                                                                                                                  "Copying the style is the most important task. Draft a response to the selected message using the style of the character " + parody + "\n"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        "7 Step: Generate only one response to the message you selected. Consider examples from the analysis of the character's messages " + parody + "\n"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      "Very important: Strictly adhere to the style of messages from step 5. This means if he doesn't use emojis, then he DOES NOT USE them, and so on."
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      "There should be ONLY ONE message STRICTLY FROM THE PERSPECTIVE OF YOUR CHARACTER in the format <ans>{message}</ans>"
            )
    return {"system_context": system_context, "text": text}
