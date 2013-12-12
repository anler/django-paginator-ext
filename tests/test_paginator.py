# -*- coding: utf-8 -*-
import pytest

from django_paginator_ext import (PartialPaginator as Paginator, EmptyPage, get_offset,
                                  get_page_number)


def test_current_page():
    assert Paginator(['lorem'], per_page=1, page=1, count=3).page().number == 1
    assert Paginator(['lorem'], per_page=1, page=2, count=3).page().number == 2
    assert Paginator(['lorem'], per_page=1, page=3, count=3).page().number == 3

    assert Paginator(['lorem', 'ipsum'], per_page=2, page=1, count=5).page().number == 1
    assert Paginator(['lorem', 'ipsum'], per_page=2, page=2, count=5).page().number == 2
    assert Paginator(['lorem', 'ipsum'], per_page=2, page=3, count=5).page().number == 3


def test_empty_page_allowed():
    paginator = Paginator((), per_page=2, page=2, count=0, allow_empty_first_page=True)
    assert paginator.page().number == 1


def test_empty_page_not_allowed():
    with pytest.raises(EmptyPage):
        Paginator((), per_page=2, count=0, allow_empty_first_page=False).page()


def test_page_has_next():
    page = Paginator(['ipsum'], per_page=2, count=3).page()
    assert page.has_next()
    assert page.next_page_number() == 2
    assert page.start_index() == 1
    assert page.end_index() == 2
    assert not page.has_previous()


def test_page_has_previous():
    page = Paginator(['ipsum'], per_page=2, count=3, page=2).page()
    assert page.has_previous()
    assert page.previous_page_number() == 1
    assert page.start_index() == 3
    assert page.end_index() == 3
    assert not page.has_next()


def test_page_has_other_pages():
    page = Paginator(['lorem', 'ipsum'], per_page=2, count=5, page=2).page()
    assert page.has_other_pages()
    assert page.next_page_number() == 3
    assert page.previous_page_number() == 1


def test_page_window_beginning():
    page = Paginator(['lorem'], per_page=1, count=10, page=1).page()
    assert page.window() == [1, 2, 3, 4, 5]


def test_page_window_end():
    page = Paginator(['lorem'], per_page=1, count=10, page=3).page()
    assert page.window() == [1, 2, 3, 4, 5]


def test_page_window_middle():
    page = Paginator(['lorem'], per_page=1, count=10, page=4).page()
    assert page.window() == [2, 3, 4, 5, 6]


def test_page_window_close_beginning():
    page = Paginator(['lorem'], per_page=1, count=10, page=2).page()
    assert page.window() == [1, 2, 3, 4, 5]


def test_page_window_close_end():
    page = Paginator(['lorem'], per_page=1, count=10, page=8).page()
    assert page.window() == [6, 7, 8, 9, 10]


def test_get_offset():
    assert get_offset(page=1, per_page=5, count=21) == 0
    assert get_offset(page=2, per_page=5, count=21) == 5
    assert get_offset(page=5, per_page=5, count=21) == 20


def test_get_page_number():
    assert get_page_number(None) == 1
    assert get_page_number('') == 1
    assert get_page_number('1') == 1
    assert get_page_number('-2') == 1
