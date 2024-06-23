from time import perf_counter
from functools import wraps
from typing import Callable, Any


def tempo_execucao(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        time_inicio: float = perf_counter()
        result: Any = func(*args, **kwargs)
        time_fim: float = perf_counter()

        print(f'"{func.__name__}()" levou {time_fim - time_inicio:.3f} segundos para executar.')
        return result

    return wrapper
