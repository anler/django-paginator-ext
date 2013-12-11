# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.paginator import Paginator as DjangoPaginator, EmptyPage

from .layout import SimpleLayout


class Paginator(DjangoPaginator):

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, layout=None):
        super(Paginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)
        if layout is None:
            layout = getattr(settings, 'PAGINATOR_LAYOUT', SimpleLayout())
        self.layout = layout

    def get_navigation(self, current_page=1):
        return self.layout.get_navigation(paginator=self, current_page=current_page)


class PartialPaginator(Paginator):

    def __init__(self, object_list, per_page, total, offset=0, orphans=0,
                 allow_empty_first_page=True, layout=None):
        super(PartialPaginator, self).__init__(object_list, per_page, orphans,
                                               allow_empty_first_page, layout)
        self.total = total
        self.offset = offset

    def page(self):
        if not self.count:
            if not self.allow_empty_first_page:
                raise EmptyPage('That page contains no results')
            return self._get_page(self.object_list, 1, self)
        return self._get_page(self.object_list, self.page_number, self)

    @property
    def page_number(self):
        try:
            page = sum(divmod(self.offset, self.per_page)) if self.offset else 1
        except ZeroDivisionError:
            page = 0
        return page

    def _get_num_pages(self):
        try:
            num_pages = sum(divmod(self.total, self.per_page))
        except ZeroDivisionError:
            num_pages = 0
        return num_pages
    num_pages = property(_get_num_pages)

    def _get_count(self):
        return self.total
    count = property(_get_count)
