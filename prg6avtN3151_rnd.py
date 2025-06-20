from abc import ABC, abstractmethod
from typing import Iterator


class ValueError(Exception):
    pass

class PRNGBase(ABC):

    @abstractmethod
    def next_float(self) -> float:
        pass

    @abstractmethod
    def next_int(self) -> int:
        pass

class MyPRNG(PRNGBase):

    def __init__(self, generator: Iterator[int]):
        self.generator = generator

    def next_int(self) -> int:
        return next(self.generator)

    def next_float(self) -> float:
        return self.next_int() / (1<<32)

def LFG_cache(j: int, k: int, Mod: int, initial_seed: int = 1) -> Iterator[int]:
    if not ((j > k) and (k >= 1) and (Mod > 1)):
        raise ValueError("Параметры должны удовлетворять условию: j > k >= 1, Mod > 1")

    cache = [initial_seed]
    def LFG():

        nonlocal cache
        while True:
            if len(cache) < max(j, k) + 1:
                app = [initial_seed + i for i in range(max(j, k) + 1 - len(cache))]
                cache += app
            cache.append((cache[-j] + cache[-k]) % Mod)
            yield (cache[-j] + cache[-k]) % Mod
    return LFG()