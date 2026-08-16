import time
from functools import wraps
from threading import Thread


def threaded(func):
    """
    Runs function in a fake separate thread.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_thread = Thread(target=func, args=args, kwargs=kwargs)
        func_thread.daemon = True
        func_thread.start()
        return func_thread

    return wrapper


def debug(verbose=False, stopwatch=False):
    """
    Debug tool. By default does nothing.
        verbose
            Prints out func name, arguments and result.
        stopwatch
            Prints function execution time.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if verbose:
                print("[DEBUG] Calling {}".format(func.__name__))
                print("[DEBUG] With args: {}; kwargs: {}".format(args, kwargs))
            if stopwatch:
                execution_time = time.perf_counter()
            result = func(*args, **kwargs)
            if stopwatch:
                execution_time = round(time.perf_counter() - execution_time, 6)
            if verbose:
                print("[DEBUG] {} returned: {}".format(func.__name__, result))
            if stopwatch:
                print("[DEBUG] Execution time: {} seconds".format(execution_time))
            return result

        return wrapper

    return decorator
