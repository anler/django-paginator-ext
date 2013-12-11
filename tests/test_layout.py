# -*- coding: utf-8 -*-

from django_paginator_ext import PartialPaginator


def test_navigation():
    paginator = PartialPaginator(['lorem', 'ipsum'], per_page=2, total=3)
    assert paginator.get_navigation() == u"Page 1 of 2"
