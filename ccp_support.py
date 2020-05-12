#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#    Mar 06, 2020 06:04:40 PM +0200  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    w.update_output("Started")


def destroy_window():
    # Function which closes the window.
    print('A')
    global top_level
    top_level.destroy()
    top_level = None


def update_feedback(output):
    global w, root
    w.update_output(output)


def insert_bots(bots):
    global w, root
    w.insert_bots(bots)


if __name__ == '__main__':
    import ccp
    ccp.vp_start_gui()



