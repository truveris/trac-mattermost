# Copyright (c) 2021 RISC Software GmbH. All Rights Reserved.
# See included LICENSE file.

from trac.core import Component
from trac.core import implements
from trac.versioncontrol.api import IRepositoryChangeListener

from base import TracMattermostComponent


def format_message(message):
    if not message:
        return ""
    return "\n".join("> " + l for l in message.splitlines())


class RepositoryNotifications(Component, TracMattermostComponent):

    implements(IRepositoryChangeListener)

    def format_changeset(self, changeset):
        if changeset.repos.reponame:
            link = self.env.abs_href.changeset(changeset.rev, changeset.repos.reponame)
        else:
            link = self.env.abs_href.changeset(changeset.rev)
        return (
            u"[&#91;{rev}&#93;]({link})"
            .format(
                rev=changeset.repos.display_rev(changeset.rev),
                link=link
            )
        )

    def changeset_added(self, repos, changeset):
        fmt = u"@{author} committed {changeset}"
        if repos.reponame:
            fmt = fmt + u" in {repos}"
        fmt = fmt + u":\n{message}"
        text = fmt.format(
            author=changeset.author,
            changeset=self.format_changeset(changeset),
            repos=repos.reponame,
            message=format_message(changeset.message),
        ).strip()

        self.send_notification(text)

    def changeset_modified(self, repos, changeset, old_changeset):
        fmt = u"@{author} modified {changeset}"
        if repos.reponame:
            fmt = fmt + u" in {repos}"
        fmt = fmt + u":\n{message}"
        if old_changeset and old_changeset.message:
            fmt = fmt + u"\nfrom\n{old_message}"
        text = fmt.format(
            author=changeset.author,
            changeset=self.format_changeset(changeset),
            repos=repos.reponame,
            message=format_message(changeset.message),
            old_message=format_message(old_changeset.message),
        ).strip()

        self.send_notification(text)
