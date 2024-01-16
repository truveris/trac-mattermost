trac-mattermost - Trac notifications in Mattermost
==================================================

trac-mattermost is a Trac plugin publishing Trac events to Mattermost using
webhooks.

Configuration
-------------
To enable and configure trac-mattermost, you need to create an "Incoming
Webhook" in Mattermost (Account Settings, Integrations, Incoming Webhooks),
then you need to add the following to your Trac configuration file::

    [components]
    trac_mattermost.ticket_notifications.* = enabled
    trac_mattermost.wiki_notifications.* = enabled
    trac_mattermost.repository_notifications.* = enabled
    trac_mattermost.milestone_notifications.* = enabled
    trac_mattermost.attachment_notifications.* = enabled

    [mattermost]
    username = Trac
    webhook_url = https://mattermost.example.com/hooks/q9w8jq9wdw89sd7agf7sq7qweh
    icon_url = https://s3.amazonaws.com/truveris-mattermost-icons/trac.png
    channel = dev

Installation
------------
Build an .egg file and drop it in the plugins directory of your Trac
installation::

    python setup.py bdist_egg
