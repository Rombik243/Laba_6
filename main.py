from functools import wraps

class Schuffle_str_ret:
    def __init__(self, string: str):
        self.string = list(string)
        self.strcpy = list(string)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            length = len(self.string)
            if length == 0:
                return ''
            for i in range(length-1, -1, -1):
                rand = func(*args, **kwargs)
                rand_index = next(rand) % (i + 1)
                self.strcpy[i], self.strcpy[rand_index] = self.strcpy[rand_index], self.strcpy[i]
            return ''.join(self.strcpy)
        return wrapper

