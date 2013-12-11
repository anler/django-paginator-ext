# -*- coding: utf-8 -*-
import pytest

from pagination_again import PartialPaginator as Paginator, EmptyPage


def test_offset():
    assert Paginator(['lorem', 'ipsum'], per_page=2, total=3).page().number == 1
    assert Paginator(['lorem', 'ipsum'], per_page=2, total=7, offset=5).page().number == 3


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
