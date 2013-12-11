# -*- coding: utf-8 -*-

from django.core.paginator import Paginator as DjangoPaginator, Page as DjangoPage, EmptyPage


class Page(DjangoPage):

    def window(self, width=2):
        current = self.number
        left = current - 1
        right = current + 1
        window = [current]

        while width:
            if self.paginator.has_page(left):
                window.insert(0, left)
                left -= 1
            elif self.paginator.has_page(right):
                width += 1

            if self.paginator.has_page(right):
                window.append(right)
                right += 1
            elif self.paginator.has_page(left):
                width += 1

            width -= 1

        return window


class Paginator(DjangoPaginator):

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        super(Paginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)

    def get_navigation(self, current_page=1):
        return self.layout.get_navigation(paginator=self, current_page=self.page(current_page))

    def _get_page(self, *args, **kwargs):
        return Page(*args, **kwargs)

    def has_page(self, page):
        return 0 < page <= self.num_pages


class PartialPaginator(Paginator):

    def __init__(self, object_list, per_page, total, offset=0, orphans=0,
                 allow_empty_first_page=True):
        super(PartialPaginator, self).__init__(object_list, per_page, orphans,
                                               allow_empty_first_page)
        self.total = total
        self.offset = offset

    def page(self):
        if not self.count:
            if not self.allow_empty_first_page:
                raise EmptyPage('That page contains no results')
            return self._get_page(self.object_list, 1, self)
        return self._get_page(self.object_list, self.page_number, self)

    def get_navigation(self):
        return self.layout.get_navigation(paginator=self, current_page=self.page())

    @property
    def page_number(self):
        try:
            page = sum(divmod(self.offset + 1, self.per_page)) if self.offset else 1
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
