# Copyright (c) 2015-2016 Truveris, Inc. All Rights Reserved.
# See included LICENSE file.

from trac.core import Component
from trac.core import implements
from trac.wiki.api import IWikiChangeListener

from base import TracMattermostComponent


class WikiNotifications(Component, TracMattermostComponent):

    implements(IWikiChangeListener)

    def format_page(self, page, version):
        fmt = u"[{name}]({link}) v{version}"

        return fmt.format(
            name=page.name,
            version=version,
            link=self.env.abs_href.wiki(page.name),
        )

    def wiki_page_added(self, page):
        pass

    def wiki_page_changed(self, page, version, t, comment, author, ipnr):
        fmt = u"@{author} edited {page}"
        if comment:
            fmt = fmt + ": {comment}"
        text = fmt.format(
            author=author,
            page=self.format_page(page, version),
            comment=comment,
        )
        self.send_notification(text)

    def wiki_page_deleted(self, page):
        pass

    def wiki_page_version_deleted(self, page):
        pass

    def wiki_page_renamed(self, page, old_name):
        pass
