import pytest
from prg6avtN3151_subst import MyPRNG, Schuffle_str_ret
from prg6avtN3151_rnd import LFG_cache
import os

# Фикстура для создания MyPRNG с фиксированным генератором
@pytest.fixture
def prng():
    """Фикстура для создания MyPRNG с LFG_cache."""
    gen = LFG_cache(j=5, k=3, Mod=100, initial_seed=1)
    return MyPRNG(gen)

# Фикстура для декоратора с тестовыми параметрами
@pytest.fixture
def decorator(prng):
    """Фикстура для создания декоратора с PRNG и лог-файлом."""
    return Schuffle_str_ret("abcd", prng, log_file="test.log")

# Фикстура для декоратора без лог-файла
@pytest.fixture
def decorator_no_log(prng):
    """Фикстура для создания декоратора без лог-файла."""
    return Schuffle_str_ret("abcd", prng)

def test_decorator_initialization(decorator):
    """Проверяет корректность инициализации декоратора."""
    assert decorator.string == list("abcd"), "Исходная строка не совпадает"
    assert len(decorator.string) == 4, "Неверная длина строки"
    assert isinstance(decorator.prng, MyPRNG), "PRNG должен быть экземпляром MyPRNG"

def test_shuffle_string(decorator):
    """Проверяет перемешивание строки."""
    @decorator
    def dummy_func():
        pass
    result = dummy_func()
    assert len(result) == 4
    assert sorted(result) == sorted("abcd")
    assert result != "abcd", "Строка должна быть перемешана"

def test_empty_string(decorator):
    """Проверяет обработку пустой строки."""
    empty_decorator = Schuffle_str_ret("", decorator.prng, log_file="test.log")
    @empty_decorator
    def dummy_func():
        pass
    result = dummy_func()
    assert result == "", "Для пустой строки должен возвращаться пустой результат"
    with open("test.log", "r") as f:
        log = f.read()
    assert "dummy_func(args=(), kwargs={}) -> ''" in log, "Лог для пустой строки отсутствует"

def test_logging_to_file(decorator):
    """Проверяет логирование в файл."""
    @decorator
    def dummy_func():
        pass
    result = dummy_func()
    with open("test.log", "r") as f:
        log = f.read()
    assert "dummy_func(args=(), kwargs={})" in log, "Лог вызова отсутствует"
    assert "аргумент abcd (args[0]) заменен" in log, "Лог замены отсутствует"

def test_logging_to_stderr(decorator_no_log, capsys):
    """Проверяет логирование в stderr."""
    @decorator_no_log
    def dummy_func():
        pass
    result = dummy_func()
    captured = capsys.readouterr()
    assert "dummy_func(args=(), kwargs={})" in captured.err, "Лог вызова отсутствует"
    assert "аргумент abcd (args[0]) заменен" in captured.err, "Лог замены отсутствует"

def test_function_metadata(decorator):
    """Проверяет сохранение метаданных функции с wraps."""
    def original_func():
        """Оригинальная функция."""
        pass
    wrapped_func = decorator(original_func)
    assert wrapped_func.__name__ == "original_func", "Имя функции не сохранено"
    assert wrapped_func.__doc__ == "Оригинальная функция.", "Документация не сохранена"

def test_cleanup():
    """Удаляет тестовый лог-файл после тестов."""
    if os.path.exists("test.log"):
        os.remove("test.log")