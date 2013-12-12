# -*- coding: utf-8 -*-

from django.core.paginator import Paginator as DjangoPaginator, Page as DjangoPage, EmptyPage


class Page(DjangoPage):

    def window(self, width=2):
        current = self.number
        left = current - 1
        right = current + 1
        window = [current]
        is_valid_window = lambda: len(window) <= width * 2 + 1

        while width:
            if self.paginator.has_page(left):
                window.insert(0, left)
                left -= 1
            elif self.paginator.has_page(right) and is_valid_window():
                width += 1

            if self.paginator.has_page(right):
                window.append(right)
                right += 1
            elif self.paginator.has_page(left):
                width += 1

            width -= 1

        return window


class Paginator(DjangoPaginator):

    def _get_page(self, *args, **kwargs):
        return Page(*args, **kwargs)

    def has_page(self, page):
        return 0 < page <= self.num_pages


class PartialPaginator(Paginator):

    def __init__(self, object_list, per_page,  count, page=1, *args, **kwargs):
        super(PartialPaginator, self).__init__(object_list, per_page, *args, **kwargs)
        self._count = count
        self._current_page = page

    def page(self):
        if not self.allow_empty_first_page and not self.object_list:
            raise EmptyPage('That page contains no results')
        num_pages = self.num_pages
        current_page = self._current_page if self._current_page <= num_pages else num_pages
        return self._get_page(self.object_list, current_page, self)

    def _get_num_pages(self):
        try:
            num_pages = sum(divmod(self.count, self.per_page)) if self.count > self.per_page else 1
        except ZeroDivisionError:
            num_pages = 0
        return num_pages
    num_pages = property(_get_num_pages)

    def _get_count(self):
        return self._count
    count = property(_get_count)
