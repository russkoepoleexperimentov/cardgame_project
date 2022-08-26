show_warning_messages = True


def _show_warning_messages():
    return show_warning_messages


def obsolete(func):
    def wrapper(*args, **kwargs):
        if _show_warning_messages():
            print(f'[WARNING] Function {func.__name__} is obsolete.')
        return func(*args, **kwargs)
    return wrapper
