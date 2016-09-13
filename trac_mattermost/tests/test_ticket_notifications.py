# Copyright (c) 2016 Truveris, Inc. All Rights Reserved.
# See included LICENSE file.

import unittest


class TicketNotificationsTests(unittest.TestCase):

    def test_format_comment(self):
        from trac_mattermost.ticket_notifications import format_comment

        self.assertEquals(format_comment(""), "")
        self.assertEquals(format_comment("o" * 90), "> " + "o" * 90)
        self.assertEquals(format_comment("o" * 200), "> " + "o" * 97 + "...")

        value = "@bjanin, you should fix that test"
        expected = "> " + value
        self.assertEquals(format_comment(value), expected)

        value = "@bjanin, you should fix that test" * 10
        expected = "> " + value[:97] + "..."
        self.assertEquals(format_comment(value), expected)

        value = "@bjanin, you should fix that test" * 10
        value = value + "and @jcarmack and @bgate"
        expected = (
            "> " + value[:97] + "..." +
            "\n> Other mentions: @jcarmack, @bgate"
        )
        self.assertEquals(format_comment(value), expected)
