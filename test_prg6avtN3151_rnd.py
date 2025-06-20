import pytest
from prg6avtN3151_rnd import MyPRNG, LFG_cache, ValueError

# Фикстура для создания MyPRNG с фиксированным генератором
@pytest.fixture
def prng():
    """Фикстура для создания MyPRNG с LFG_cache."""
    gen = LFG_cache(j=5, k=3, Mod=100, initial_seed=1)
    return MyPRNG(gen)

def test_lfg_cache_values():
    """Проверяет, что генератор возвращает значения в диапазоне [0, Mod)."""
    gen = LFG_cache(j=5, k=3, Mod=100, initial_seed=1)
    values = [next(gen) for _ in range(10)]
    assert all(0 <= x < 100 for x in values), "Значения вне диапазона [0, Mod)"

def test_lfg_cache_invalid_parameters():
    """Проверяет обработку некорректных параметров."""
    with pytest.raises(ValueError, match="j > k >= 1, Mod > 1"):
        LFG_cache(j=3, k=5, Mod=100)  # j <= k
    with pytest.raises(ValueError, match="j > k >= 1, Mod > 1"):
        LFG_cache(j=5, k=0, Mod=100)  # k < 1
    with pytest.raises(ValueError, match="j > k >= 1, Mod > 1"):
        LFG_cache(j=5, k=3, Mod=1)  # Mod <= 1

def test_myprng_next_int(prng):
    """Проверяет метод next_int."""
    value = prng.next_int()
    assert isinstance(value, int), "next_int должен возвращать целое число"
    assert 0 <= value < 100, "next_int возвращает значение вне диапазона [0, Mod)"

def test_myprng_next_float(prng):
    """Проверяет метод next_float."""
    value = prng.next_float()
    assert isinstance(value, float), "next_float должен возвращать float"
    assert 0 <= value < 1, "next_float вне диапазона [0, 1)"

def test_myprng_type_annotations():
    """Проверяет аннотации типов."""
    prng = MyPRNG(LFG_cache(j=5, k=3, Mod=100, initial_seed=1))
    assert isinstance(prng.next_int(), int), "next_int не соответствует аннотации int"
    assert isinstance(prng.next_float(), float), "next_float не соответствует аннотации float"
