# -*- coding: utf-8 -*-


def get_offset(page, per_page, count):
    """Calculate the corresponding offset for a page.

    :param int page: Page number.
    :param int per_page: Number of items allowed per page.
    :param int count: Number of total items available.

    :return: Calculated offset.
    :rtype: int
    """
    return (page * per_page) - per_page


def get_page_number(page, default=1):
    """Tries to convert a text value into a valid page number.

    :param page: Value to convert in to a valid page number.
    :para default: Default value to return if the conversion fails.

    :return: The converted value as an :class:`int` instance or `default`.
    """
    try:
        page = int(page)
        if page < 0:
            raise ValueError('Invalid page value')
    except (ValueError, TypeError):
        page = default
    return page
