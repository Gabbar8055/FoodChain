﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Lionel Laské 


from gi.repository import Gtk
import logging
import os

from gettext import gettext as _

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ShareButton
from sugar3.activity.widgets import DescriptionItem
from sugar3.presence import presenceservice

from gi.repository import WebKit
import logging
import gconf

from datetime import date

from enyo import Enyo


class FoodChainActivity(activity.Activity):
    """EnyoActivity class as specified in activity.info"""

    def __init__(self, handle):
        """Set up the activity."""
        activity.Activity.__init__(self, handle)

        self.max_participants = 1

        self.make_toolbar()
        self.make_mainview()

    def alert(self, msg):
        """Display a message dialog"""
        messagedialog = Gtk.MessageDialog(self, type=1, buttons=1,  message_format=msg)
        messagedialog.run()
        messagedialog.destroy()

    def display_message(self, param):
        """A message was received from JavaScript, display it"""
        # Display as a JSON string to see structure
        self.alert("Python received "+self.enyo.json_encode(param))

    def console_message(self, message):
        self.console.set_text(self.console.get_text(self.console.get_start_iter(), self.console.get_end_iter(), True)+message+"\n")

    def init_context(self, args):
        """Init Javascript context sending buddy information"""
        # Get XO colors
        buddy = {}
        client = gconf.client_get_default()
        colors = client.get_string("/desktop/sugar/user/color")
        buddy["colors"] = colors.split(",")

        # Get XO name
        presenceService = presenceservice.get_instance()
        buddy["name"] = presenceService.get_owner().props.nick

        self.enyo.send_message("buddy", buddy)

    def make_mainview(self):
        """Create the activity view"""
        # Create global box
        vbox = Gtk.VBox(False)

        # Create webview
        self.webview = webview = WebKit.WebView()
        webview.show()
        vbox.pack_start(webview, True, True, 0)

        # Create console for debug (set to True)
        if False:
            sw = Gtk.ScrolledWindow()
            textview = Gtk.TextView()
            self.console = console = textview.get_buffer()
            sw.add(textview)
            sw.show()
            textview.show()
            sw.set_size_request(800, 100)
            vbox.pack_end(sw, True, True, 0)
        vbox.show()

        # Activate Enyo interface
        self.enyo = Enyo(webview)
        self.enyo.connect("ready", self.init_context)
        self.enyo.connect("console-message", self.console_message)

        # Go to first page
        web_app_page = os.path.join(activity.get_bundle_path(), "html/index.html")
        self.webview.load_uri('file://' + web_app_page)

        # Display all
        self.set_canvas(vbox)
        vbox.show()

    def make_toolbar(self):
        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        description_item = DescriptionItem(self)
        toolbar_box.toolbar.insert(description_item, -1)
        description_item.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
