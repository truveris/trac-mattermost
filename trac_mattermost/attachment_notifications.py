# Copyright (c) 2021 RISC Software GmbH. All Rights Reserved.
# See included LICENSE file.

from trac.core import Component
from trac.core import implements
from trac.attachment import IAttachmentChangeListener

from trac_mattermost.base import TracMattermostComponent


class AttachmentNotifications(Component, TracMattermostComponent):

    implements(IAttachmentChangeListener)

    def format_attachment(self, attachment):
        return (
            u"[{filename}]({link})"
            .format(
                filename=attachment.filename,
                link=self.env.abs_href.attachment(attachment.parent_realm, attachment.parent_id, attachment.filename),
            )
        )

    def format_parent(self, realm, id):
        if realm == 'wiki':
            return (
                u"wiki page [{name}]({link})"
                .format(
                    name=id,
                    link=self.env.abs_href.wiki(id),
                )
            )
        elif realm == 'ticket':
            return (
                u"ticket [#{ticket_id}]({link})"
                .format(
                    ticket_id=id,
                    link=self.env.abs_href.ticket(id),
                )
            )
        elif realm == 'milestone':
            return (
                u"milestone [{name}]({link})"
                .format(
                    name=id,
                    link=self.env.abs_href.milestone(id),
                )
            )
        else:
            return u"<unknown>"

    def attachment_added(self, attachment):
        text = (
            u"@{author} attached {attachment} to {parent}"
        ).format(
            attachment=self.format_attachment(attachment),
            parent=self.format_parent(attachment.parent_realm, attachment.parent_id),
            author=attachment.author,
        )

        self.send_notification(text)

    def attachment_deleted(self, attachment):
        text = (
            u"{attachment} deleted from {parent}"
        ).format(
            attachment=attachment.filename,
            parent=self.format_parent(attachment.parent_realm, attachment.parent_id),
        )

        self.send_notification(text)

    def attachment_moved(self, attachment, old_parent_realm, old_parent_id, old_filename):
        if attachment.parent_realm == old_parent_realm and attachment.parent_id == old_parent_id:
            fmt = u"attachment {old_filename} in {parent} renamed to {attachment}"
        else:
            fmt = u"attachment {attachment} moved from {old_parent} to {parent}"
            if attachment.filename != old_filename:
                fmt = fmt + u" (was {old_filename})"
            self.move_called = True # skip redundant reparented notification
        
        text = fmt.format(
            attachment=self.format_attachment(attachment),
            parent=self.format_parent(attachment.parent_realm, attachment.parent_id),
            old_filename=old_filename,
            old_parent=self.format_parent(old_parent_realm, old_parent_id),
        )

        self.send_notification(text)

    # attachment_reparented is here to support Trac older than version 1.4
    def attachment_reparented(self, attachment, old_parent_realm, old_parent_id):
        if self.move_called:
            self.move_called = False
            return

        fmt = u"attachment {attachment} moved from {old_parent} to {parent}"
        
        text = fmt.format(
            attachment=self.format_attachment(attachment),
            parent=self.format_parent(attachment.parent_realm, attachment.parent_id),
            old_parent=self.format_parent(old_parent_realm, old_parent_id),
        )

        self.send_notification(text)
