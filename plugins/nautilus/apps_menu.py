#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gi.repository import Nautilus as Explorer
from gi.repository import GObject

import os
from datetime import datetime
from subprocess import Popen, PIPE

LOG_PATH = "/tmp/phantasy_logs/"

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


class ColumnExtension(GObject.GObject, Explorer.MenuProvider):
    def __init__(self):
        super(self.__class__, self).__init__()

    def get_background_items(self, window, file):
        top_mitem = Explorer.MenuItem(
                name="AppsMenu::Physics Apps",
                label="Physics Apps",
                tip="Global Launcher for Physics Applications",
                icon="phantasy-al")

        top_mitem.connect('activate', self.start_app_launcher, file)

        return top_mitem,

    def start_app_launcher(self, menu, file):
        cmd = "app_launcher"
        fn = datetime.now().strftime('%Y%m%d_%H%M%S')
        logfile = os.path.join(LOG_PATH, fn)
        with open(logfile, 'w') as fid:
            p = Popen(cmd, shell=True,
                      stdin=PIPE, stdout=fid, stderr=fid,
                      close_fds=True)