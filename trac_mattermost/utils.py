# Copyright (c) 2015-2016 Truveris, Inc. All Rights Reserved.
# See included LICENSE file.

import re


re_mention = re.compile(r"\B@[a-zA-Z0-9]{3,32}\b")


def extract_mentions(s):
    return set(re_mention.findall(s))
