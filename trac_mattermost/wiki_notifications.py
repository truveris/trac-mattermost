# Copyright (c) 2015-2016 Truveris, Inc. All Rights Reserved.
# See included LICENSE file.

from trac.core import Component
from trac.core import implements
from trac.wiki.api import IWikiChangeListener

from base import TracMattermostComponent


class WikiNotifications(Component, TracMattermostComponent):

    implements(IWikiChangeListener)

    def format_page(self, page, version=None):
        fmt = u"[{name}]({link})"
        if version:
            fmt = fmt + " [v{version}]({difflink})"

        return fmt.format(
            name=page.name,
            version=version,
            link=self.env.abs_href.wiki(page.name),
            difflink=self.env.abs_href.wiki(page.name, {
                "action": "diff",
                "version": version,
            }),
        )

    def wiki_page_added(self, page):
        fmt = u"@{author} created {page}"
        text = fmt.format(
            author=page.author,
            page=self.format_page(page),
        )
        self.send_notification(text)

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
        fmt = u"{page} was deleted"
        text = fmt.format(
            page=page.name,
        )
        self.send_notification(text)

    def wiki_page_version_deleted(self, page):
        fmt = u"version {version} of {page} was deleted"
        text = fmt.format(
            page=self.format_page(page),
            version=page.version,
        )
        self.send_notification(text)

    def wiki_page_renamed(self, page, old_name):
        fmt = u"{old_name} was renamed to {page}"
        text = fmt.format(
            old_name=old_name,
            page=self.format_page(page),
        )
        self.send_notification(text)

    def wiki_page_comment_modified(self, page, old_comment):
        fmt = (
            u"the change comment of {page} was changed from:\n"
            "{old_comment}\n"
            "to:\n"
            "{comment}"
        )
        text = fmt.format(
            page=self.format_page(page, page.version),
            comment=page.comment,
            old_comment=old_comment,
        )
        self.send_notification(text)
