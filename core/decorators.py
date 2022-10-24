from functools import wraps
import timeit

def benchmark(func):
    @wraps(func)
    def with_benchmark(*args, **kwargs):
        starttime = timeit.default_timer()
        response = func(*args, **kwargs)
        print(f'{func.__name__} se completo en {timeit.default_timer() - starttime} segundos.')
        return response
    return with_benchmark
