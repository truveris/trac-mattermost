# Copyright (c) 2015-2016 Truveris, Inc. All Rights Reserved.
# See included LICENSE file.

from trac.core import Component
from trac.core import implements
from trac.ticket.api import ITicketChangeListener, TicketSystem

from trac_mattermost.base import TracMattermostComponent
from trac_mattermost.utils import extract_mentions


def format_comment(comment):
    if not comment:
        return ""

    all_mentions = extract_mentions(comment)

    if len(comment) > 100:
        comment = comment[:97] + "..."
        # Figure out who was left out of mentions so we can add them at
        # the end and trigger highlights and notifications.
        other_mentions = all_mentions - extract_mentions(comment)
        if other_mentions:
            comment += (
                "\n\n**Other mentions:** {}"
                .format(", ".join(other_mentions))
            )

    return "\n".join("> " + l for l in comment.splitlines())


class TicketNotifications(Component, TracMattermostComponent):

    implements(ITicketChangeListener)

    def format_ticket(self, ticket):
        return (
            u"[#{ticket_id}. {summary}]({link})"
            .format(
                ticket_id=ticket.id,
                link=self.env.abs_href.ticket(ticket.id),
                summary=ticket["summary"],
            )
        )

    def format_change(self, key, old_value, new_value, formatted):
        # No changes occurred, this sometimes happens when the user clicks
        # on a field but doesn't change anything.
        if (old_value or "") == (new_value or ""):
            return

        if not old_value:
            f = u"**{0}** set to *{1}*".format(key, new_value)
        elif not new_value:
            f = u"**{0}** unset".format(key)
        else:
            if len(old_value) > 100 or len(new_value) > 100:
                f = u"**{0}** changed".format(key)
            else:
                f = (
                    u"**{0}** changed from *{1}* to *{2}*"
                    .format(key, old_value, new_value)
                )
        formatted.append(f)

    def format_changes(self, ticket, old_values):
        field_labels = TicketSystem(self.env).get_ticket_field_labels()

        formatted = []
        for k, v in old_values.items():
            self.format_change(field_labels[k], v, ticket[k], formatted)

        return u"\n".join(formatted)

    def format_old_changes(self, changes):
        field_labels = TicketSystem(self.env).get_ticket_field_labels()

        formatted = []
        for k, (old_value, new_value) in changes.items():
            self.format_change(field_labels[k], old_value, new_value, formatted)

        return u"\n".join(formatted)

    def ticket_created(self, ticket):
        text = (
            u"New ticket: {ticket} by @{username}"
        ).format(
            ticket=self.format_ticket(ticket),
            username=ticket["reporter"],
        )

        self.send_notification(text)

    def ticket_changed(self, ticket, comment, author, old_values):
        comment = format_comment(comment)

        if old_values:
            fmt = (
                u"@{username} changed {ticket}:\n"
                "{changes}\n"
                "{comment}"
            )
        else:
            fmt = (
                u"@{username} commented on {ticket}:\n"
                "{comment}"
            )

        text = fmt.format(
            ticket=self.format_ticket(ticket),
            username=author,
            comment=comment,
            changes=self.format_changes(ticket, old_values),
        ).strip()

        self.send_notification(text)

    def ticket_deleted(self, ticket):
        text = (
            u"Ticket #{ticket_id}. {summary} deleted"
        ).format(
                ticket_id=ticket.id,
                summary=ticket["summary"],
        )

        self.send_notification(text)

    def ticket_comment_modified(self, ticket, cdate, author, comment, old_comment):
        comment = format_comment(comment)
        old_comment = format_comment(old_comment)

        fmt = (
            u"@{username} modifed comment on {ticket} from:\n"
            "{old_comment}\n\n"
            "to:\n"
            "{comment}"
        )

        text = fmt.format(
            ticket=self.format_ticket(ticket),
            username=author,
            comment=comment,
            old_comment=old_comment,
        ).strip()

        self.send_notification(text)

    def ticket_change_deleted(self, ticket, cdate, changes):
        fmt = (
            u"a change of {ticket} was deleted:\n"
            "{changes}"
        )

        text = fmt.format(
            ticket=self.format_ticket(ticket),
            changes=self.format_old_changes(changes),
        ).strip()

        self.send_notification(text)
