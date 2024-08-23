import logging
import time
from typing import Any


def cost(func) :
    def wrapper(*args, **kwargs):
        start_t = time.time() * 1000
        try :
            ret = func(*args, **kwargs)
            return ret
        finally :
            end_t = time.time() * 1000
            logging.info(f"{func.__name__} cost : {'%.2f' % (end_t - start_t)}ms")
    return wrapper


def catch(default_ret:Any=None, exception:BaseException=BaseException, exception_pass:bool=False) :
    def inner(func) :
        def wrapper(*args, **kwargs):
            try :
                ret = func(*args, **kwargs)
                return ret
            except exception as e :
                if not exception_pass :
                    logging.exception(e)
                    pass
                return default_ret
        return wrapper
    return inner