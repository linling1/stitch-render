import os


def remove_file(fn) -> None:
    if fn and os.path.exists(fn):
        os.remove(fn)