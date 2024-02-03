import g4f


def get_resp(system_context, text):
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[{"role": "user", "content": system_context}, {"role": "user", "content": text}],
    )
    return response


def ask(system_context, text):
    resp = get_resp(system_context, text)
    return resp


def prompt(fn):
    def wrapper(*args, **kwargs):
        form = fn(*args, **kwargs)
        return ask(form["system_context"], form["text"])

    return wrapper
