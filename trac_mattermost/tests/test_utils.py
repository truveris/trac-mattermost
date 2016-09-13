# Copyright (c) 2016 Truveris, Inc. All Rights Reserved.
# See included LICENSE file.

import unittest


class UtilsTests(unittest.TestCase):

    def test_extract_mentions(self):
        from trac_mattermost.utils import extract_mentions

        self.assertEquals(extract_mentions(""), set())
        self.assertEquals(extract_mentions("nothing to say"), set())
        self.assertEquals(extract_mentions("nothing to say to @jcarmack"),
                          set(["@jcarmack"]))
        self.assertEquals(extract_mentions("""
            nothing to say to @jcarmack, @jcarmack
            or @sjobs, but @jcarmack!"""), set(["@jcarmack", "@sjobs"]))
