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


@gpt.prompt
def impersonate(messages, target_messages, parody):
    system_context = ("Ты - система генерации сообщений, используемая для пародирующего чат-бота. Соблюдай шаги максимально точно и подробно."
                      "Далее тебе будут переданы сообщения из беседы. "
                      "Первый(1) список сообщений будет включать в себя СЛУЧАЙНЫЕ сообщения персонажа, которого ты будешь играть."
                      "Используй эту информацию для того, чтобы пародировать стиль речи персонажа. Но не забывай, что это сообщения в совершенно случайном порядке."
                      "Второй(2) список сообщений будет включать в себя сообщения из чата. "
                      "Ты должен будешь выбрать одно сообщение, и, учитывая контекст, ответить на него")
    text = ("Первый(1) список сообщений - случайные сообщения персонажа: \n\"\"\" " + "\n".join([m["text"] for m in target_messages]) + "\n\"\"\""
            "Второй(2) список сообщений - сообщения из чата: \n\"\"\"" + "\n".join([m["text"] for m in messages]) + "\n\"\"\""
            "Шаги выполнения твоей задачи пародирования персонажа:"
                "1 ШАГ: Определи манеру речи персонажа: " + parody + "\n"
                "2 ШАГ: Выбери только одно сообщение(Написанное кем-то другим, не твоим персонажем), на которое ты будешь отвечать из второго(2) списка сообщений. \n"
                "3 ШАГ: Выполни анализ выбранного сообщения: "
                                                "1) Кто написал это сообщение? "
                                                "2) Что именно это может значит в контексе этого чата? "
                                                "3) Кому это адресовано? "
                                                "4) Какое настроение у того, кто это писал? \n"
                "4 ШАГ: Выбери общую мысль персонажа, которую он должен сказать в ответ на то сообщение из второго(2) списка: \n"
                f"5 ШАГ: Повтори анализ сообщений персонажа: {parody}, но теперь выпиши 10 его полных сообщений, "
                    f"которые будут характерны ему в контексе сообщения, на которое ты будешь отвечать \n"
                "6 ШАГ: Скопируй стиль написания сообщений персонажа " + parody + ". "
                "Учитывай характерные ему фразы, манеру, ошибки, построение сообщения, обращения, выражения и т.д. \n"
                "Сначала выпиши сообщение, на которое ты будешь отвечать. Является ли набросок сообщения связным ответом на это сообщение? "
                "Проанализируй - настолько ли стиль сгенерированного тобой сообщения соответсвует примерам из реальных сообщений персонажа. "
                "Критерии качественного ответа: 1) Связность текста 2) Правильное понимание стилистики персонажа 3) Правильное понимание контекста чата"
                "После написания наброска оцени его по этим критериям. \n"
                "Копирование стилистики - самая важная задача. Сделай набросок ответа на выбранное сообщение, используя стиль персонажа " + parody + "\n"
                "7 ШАГ: Сгенерируй только один ответ на выбранное тобой сообщение. Учитывай примеры сообщений из анализа сообщений персонажа " + parody + "\n"
                "Очень важно: Строго соблюдай стилистику сообщений из шага 5. Это значит, что если он не использует смайлики, то он их НЕ ИСПОЛЬЗУЕТ и так далее"
                "Должно выйти ТОЛЬКО ОДНО сообщение ТОЛЬКО ОТ ЛИЦА ТВОЕГО ПЕРСОНАЖА должно быть в формате <ans>{message}</ans>"
            )
    return {"system_context": system_context, "text": text}


