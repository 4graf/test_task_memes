"""
Юнит-тесты объекта значения MemText.
"""

import pytest

from app.core.mem.domain.exceptions.mem_text_exceptions import MinLengthMemTextError, MaxLengthMemTextError, \
    MemTextTypeError
from app.core.mem.domain.value_objects.mem_text import MemText


class TestMemText:
    """
    Юнит-тесты для объекта значения :class:`MemText`
    """

    def test_create_valueobject_memtext(self):
        """
        Проверяет корректное создание объекта значения текста мема.
        """
        text_default = 'Колобок повесился.'
        text_min = 'К'*500
        text_max = 'К'*5
        mem_text_default = MemText(text=text_default)
        mem_text_min = MemText(text=text_min)
        mem_text_max = MemText(text=text_max)

        assert mem_text_default.text == text_default
        assert mem_text_min.text == text_min
        assert mem_text_max.text == text_max

    def test_text_non_str_type(self):
        """
        Проверяет выбрасывание исключения при попытке передачи некорректного типа данных для текста мема.
        """
        text = 322
        with pytest.raises(MemTextTypeError):
            MemText(text=text)

    def test_text_length_less_than_minimum(self):
        """
        Проверяет выбрасывание исключения при попытке передачи текста мема длиной меньше минимальной.
        """
        text = 'К'*4
        with pytest.raises(MinLengthMemTextError):
            MemText(text=text)

    def test_text_length_greater_than_maximum(self):
        """
        Проверяет выбрасывание исключения при попытке передачи текста мема длиной больше максимальной.
        """
        text = 'К'*501
        with pytest.raises(MaxLengthMemTextError):
            MemText(text=text)

    def test_memtexts_equality(self):
        """
        Проверяет равенство одинаковых текстов мемов.
        """
        text = 'Купец'
        mem_text1 = MemText(text=text)
        mem_text2 = MemText(text=text)

        assert mem_text1 == mem_text2

    def test_memtexts_inequality(self):
        """
        Проверяет неравенство разных текстов мемов.
        """
        mem_text1 = MemText(text='Купец')
        mem_text2 = MemText(text='Не купец')

        assert mem_text1 != mem_text2
