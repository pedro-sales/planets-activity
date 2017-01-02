#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sugargame
import sugargame.canvas
import gtk

from gettext import gettext as _

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.graphics.toolbutton import ToolButton
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton

import game

class PlanetsActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        # Change the following number to change max participants
        self.max_participants = 1
        self.activity = game.PlanetsGame()
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()
        self._pygamecanvas.run_pygame(self.activity.run)

    def read_file(self, file_path):
        self.activity.read_file(file_path)
        
    def write_file(self, file_path):
        self.activity.write_file(file_path)

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        centerBut = ToolButton('view-radial')
        centerBut.set_tooltip(_("Center view on planet"))
        centerBut.connect('clicked', self.activity.center_button_pressed)
        toolbar_box.toolbar.insert(centerBut, -1)
        centerBut.show()

        showBut = ToolButton('toolbar-view')
        showBut.set_tooltip(_("Show selected planet"))
        showBut.connect('clicked', self.activity.show_button_pressed)
        toolbar_box.toolbar.insert(showBut, -1)
        showBut.show()


        delBut = ToolButton('edit-delete')
        delBut.set_tooltip(_("Delete selected planet"))
        delBut.connect('clicked', self.activity.del_button_pressed)
        toolbar_box.toolbar.insert(delBut, -1)
        delBut.show()

        pauseBut = ToolButton('media-playback-pause')
        pauseBut.connect('clicked', self.activity.pause_button_pressed)
        toolbar_box.toolbar.insert(pauseBut, -1)
        pauseBut.show()
        self.activity.pauseBut = pauseBut


        resBut = ToolButton('system-restart')
        resBut.set_tooltip(_("Restart game"))
        resBut.connect('clicked', self.activity.restart_button_pressed)
        toolbar_box.toolbar.insert(resBut, -1)
        resBut.show()

        helpBut = ToolButton('toolbar-help')
        helpBut.connect('clicked', self.activity.help_button_pressed)
        toolbar_box.toolbar.insert(helpBut, -1)
        helpBut.show()
        
        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)

        toolbar_box.toolbar.insert(separator, -1)
        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show_all()




