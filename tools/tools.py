import os
import shutil


def remove_file(fn:str) -> None:
    try :
        if fn and os.path.exists(fn):
            os.remove(fn)
    except :
        pass


def remove_dir(dir:str) -> None :
    try :
        if dir and os.path.exists(dir):
            shutil.rmtree(dir)
    except :
        pass