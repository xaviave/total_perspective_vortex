import time
import logging
import functools


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        logging.debug(
            f"{func.__name__!r} finished in {time.perf_counter() - start:.4f} secs"
        )
        return value

    return wrapper
