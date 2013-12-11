# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _


class SimpleLayout(object):

    def get_navigation(self, paginator, current_page):
        return _("Page %s of %s") % (current_page.number, paginator.num_pages)
