# Copyright (c) 2021 RISC Software GmbH. All Rights Reserved.
# See included LICENSE file.

from trac.core import Component
from trac.core import implements
from trac.ticket.api import IMilestoneChangeListener

from base import TracMattermostComponent


class MilestoneNotifications(Component, TracMattermostComponent):

    implements(IMilestoneChangeListener)

    def format_milestone(self, milestone):
        return (
            u"[{name}]({link})"
            .format(
                name=milestone.name,
                link=self.env.abs_href.milestone(milestone.name),
            )
        )

    def format_changes(self, milestone, old_values):
        formatted = []
        for k, v in old_values.items():
            # No changes occurred, this sometimes happens when the user clicks
            # on a field but doesn't change anything.
            if (v or "") == (getattr(milestone, k) or ""):
                continue

            if not v:
                f = u"**{0}** set to *{1}*".format(k, getattr(milestone, k))
            elif not getattr(milestone, k):
                f = u"**{0}** unset".format(k)
            else:
                if len(v) > 100 or len(getattr(milestone, k)) > 100:
                    f = u"**{0}** changed".format(k)
                else:
                    f = (
                        u"**{0}** changed from *{1}* to *{2}*"
                        .format(k, v, getattr(milestone, k))
                    )
            formatted.append(f)

        return u"\n".join(formatted)

    def milestone_created(self, milestone):
        text = (
            u"New milestone: {milestone}"
        ).format(
            milestone=self.format_milestone(milestone),
        )

        self.send_notification(text)

    def milestone_changed(self, milestone, old_values):
        fmt = (
            u"Milestone {milestone} changed:\n"
            "{changes}"
        )

        text = fmt.format(
            milestone=self.format_milestone(milestone),
            changes=self.format_changes(milestone, old_values),
        ).strip()

        self.send_notification(text)

    def milestone_deleted(self, milestone):
        text = (
            u"Milestone {milestone} deleted"
        ).format(
            milestone=milestone.name,
        )

        self.send_notification(text)
