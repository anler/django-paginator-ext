# -*- coding: utf-8 -*-
import pytest

from django_paginator_ext import PartialPaginator as Paginator, EmptyPage


def test_offset():
    assert Paginator(['lorem'], per_page=1, total=3).page().number == 1
    assert Paginator(['lorem'], per_page=1, total=3, offset=1).page().number == 2
    assert Paginator(['lorem'], per_page=1, total=3, offset=2).page().number == 3

    assert Paginator(['lorem', 'ipsum'], per_page=2, total=5).page().number == 1
    assert Paginator(['lorem', 'ipsum'], per_page=2, total=5, offset=2).page().number == 2
    assert Paginator(['lorem', 'ipsum'], per_page=2, total=5, offset=4).page().number == 3


def test_empty_page_allowed():
    assert Paginator((), per_page=2, total=0, allow_empty_first_page=True).page().number == 1


def test_empty_page_not_allowed():
    with pytest.raises(EmptyPage):
        Paginator((), per_page=2, total=0, allow_empty_first_page=False).page()


def test_page_has_next():
    page = Paginator(['ipsum'], per_page=2, total=3).page()
    assert page.has_next()
    assert page.next_page_number() == 2
    assert page.start_index() == 1
    assert page.end_index() == 2
    assert not page.has_previous()


def test_page_has_previous():
    page = Paginator(['ipsum'], per_page=2, total=3, offset=3).page()
    assert page.has_previous()
    assert page.previous_page_number() == 1
    assert page.start_index() == 3
    assert page.end_index() == 3
    assert not page.has_next()


def test_page_has_other_pages():
    page = Paginator(['lorem', 'ipsum'], per_page=2, total=5, offset=3).page()
    assert page.has_other_pages()
    assert page.next_page_number() == 3
    assert page.previous_page_number() == 1


def test_page_window_beginning():
    page = Paginator(['lorem'], per_page=1, total=5).page()
    assert page.window() == [1, 2, 3, 4, 5]


def test_page_window_end():
    page = Paginator(['lorem'], per_page=1, total=5, offset=3).page()
    assert page.window() == [1, 2, 3, 4, 5]


def test_page_window_middle():
    page = Paginator(['lorem'], per_page=1, total=10, offset=4).page()
    assert page.window() == [3, 4, 5, 6, 7]


def test_page_window_close_beginning():
    page = Paginator(['lorem'], per_page=1, total=10, offset=1).page()
    assert page.window() == [1, 2, 3, 4, 5]


def test_page_window_close_end():
    page = Paginator(['lorem'], per_page=1, total=10, offset=8).page()
    assert page.window() == [6, 7, 8, 9, 10]
