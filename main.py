from functools import wraps
from generator import MyPRNG  # Предполагаем, что MyPRNG доступен
from typing import Optional, Callable, Any
import sys
import datetime

class Schuffle_str_ret:
    def __init__(self, string: str, prng: MyPRNG, log_file: Optional[str] = None):
        self.string = list(string)
        self.strcpy = list(string)
        self.prng = prng
        self.log_file = log_file

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            call_time = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
            log_msg = f"{call_time} {func.__name__}(args={args}, kwargs={kwargs}) -> "
            length = len(self.string)
            if length == 0:
                log_msg += "''"
                if self.log_file:
                    with open(self.log_file, 'a') as f:
                        f.write(log_msg + '\n')
                else:
                    print(log_msg, file=sys.stderr)
                return ''
            original_arg = ''.join(self.string)
            for i in range(length-1, -1, -1):
                rand_index = self.prng.next_int() % (i + 1)
                self.strcpy[i], self.strcpy[rand_index] = self.strcpy[rand_index], self.strcpy[i]
            result = ''.join(self.strcpy)
            log_msg += f"\n{call_time} {func.__name__}: аргумент {original_arg} (args[0]) заменен на {result}"
            if self.log_file:
                with open(self.log_file, 'a') as f:
                    f.write(log_msg + '\n')
            else:
                print(log_msg, file=sys.stderr)
            return result
        return wrapper