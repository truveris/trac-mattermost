# Copyright (c) 2015-2016 Truveris, Inc. All Rights Reserved.
# See included LICENSE file.

from trac.core import Component, implements
from trac.config import Option
from trac.ticket.api import ITicketChangeListener, TicketSystem
import requests



class TicketNotifications(Component):

    implements(ITicketChangeListener)

    webhook_url = Option("mattermost", "webhook_url",
                         doc="Preconfigured Incoming Webhook URL")
    icon_url = Option("mattermost", "icon_url",
                      doc="Icon URL to be used in notifications")
    username = Option("mattermost", "username",
                      doc="Username displayed in notifications")

    # ITicketChangeListener methods
    def get_payload(self, text):
        payload = {}
        if self.icon_url:
            payload["icon_url"] = self.icon_url
        if self.username:
            payload["username"] = self.username
        payload["text"] = text
        return payload

    def format_ticket(self, ticket):
        return (
            "[#{ticket_id}. {summary}]({link})"
            .format(
                ticket_id=ticket.id,
                link=self.env.abs_href.ticket(ticket.id),
                summary=ticket["summary"],
            )
        )

    def format_changes(self, ticket, old_values):
        field_labels = TicketSystem(self.env).get_ticket_field_labels()

        formatted = []
        for k, v in old_values.items():
            # No changes occurred, this sometimes happens when the user clicks
            # on a field but doesn't change anything.
            if v == ticket[k]:
                continue

            if not v:
                f = "* **{}** set to _{}_".format(field_labels[k], ticket[k])
            elif not ticket[k]:
                f = "* **{}** unset".format(field_labels[k])
            else:
                if len(v) > 100 or len(ticket[k]) > 100:
                    f = "* **{}** changed".format(field_labels[k])
                else:
                    f = (
                        "* **{}** changed from _{}_ to _{}_"
                        .format(field_labels[k], v, ticket[k])
                    )
            formatted.append(f)

        return "\n".join(formatted)

    def ticket_created(self, ticket):
        text = (
            "New ticket: {ticket} by @{username}"
        ).format(
            ticket=self.format_ticket(ticket),
            username=ticket["reporter"],
        )

        requests.post(self.webhook_url, json=self.get_payload(text))

    def ticket_changed(self, ticket, comment, author, old_values):
        if len(comment) > 100:
            comment = comment[:97] + "..."

        if old_values:
            fmt = (
                "@{username} changed {ticket}:\n"
                "{changes}\n\n"
                "{comment}"
            )
        else:
            fmt = (
                "@{username} commented on {ticket}:\n"
                "{comment}"
            )

        text = fmt.format(
            ticket=self.format_ticket(ticket),
            username=author,
            comment=comment,
            changes=self.format_changes(ticket, old_values),
        ).strip()

        requests.post(self.webhook_url, json=self.get_payload(text))
