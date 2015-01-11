################################################################################
#      This file is part of OpenELEC - http://www.openelec.tv
#      Copyright (C) 2009-2013 Stephan Raue (stephan@openelec.tv)
#      Copyright (C) 2013 Lutz Fiebach (lufie@openelec.tv)
#
#  This program is dual-licensed; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with OpenELEC; see the file COPYING.  If not, see
#  <http://www.gnu.org/licenses/>.
#
#  Alternatively, you can license this library under a commercial license,
#  please contact OpenELEC Licensing for more information.
#
#  For more information contact:
#  OpenELEC Licensing  <license@openelec.tv>  http://www.openelec.tv
################################################################################
# -*- coding: utf-8 -*-

import dbus
import gobject
import threading
import dbus.service
import dbus.mainloop.glib


class xdbus:

    ENABLED = False
    menu = {'99': {}}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('xdbus::__init__', 'enter_function', 0)
            self.oe = oeMain
            self.dbusSystemBus = self.oe.dbusSystemBus
            self.oe.dbg_log('xdbus::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('xdbus::__init__', 'ERROR: (' + repr(e) + ')', 4)

    def start_service(self):
        try:
            self.oe.dbg_log('xdbus::start_service', 'enter_function', 0)
            self.dbusMonitor = dbusMonitor(self.oe)
            self.dbusMonitor.start()
            self.oe.dbg_log('xdbus::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('xdbus::start_service', 'ERROR: (' + repr(e) + ')', 4)

    def stop_service(self):
        try:
            self.oe.dbg_log('xdbus::stop_service', 'enter_function', 0)
            if hasattr(self, 'dbusMonitor'):
                self.dbusMonitor.stop()
                del self.dbusMonitor
            self.oe.dbg_log('xdbus::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('xdbus::stop_service', 'ERROR: (' + repr(e) + ')')

    def exit(self):
        pass

    def restart(self):
        try:
            self.oe.dbg_log('xdbus::restart', 'enter_function', 0)
            self.stop_service()
            self.start_service()
            self.oe.dbg_log('xdbus::restart', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('xdbus::restart', 'ERROR: (' + repr(e) + ')')


class dbusMonitor(threading.Thread):

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('xdbus::dbusMonitor::__init__', 'enter_function', 0)
            self.monitors = []
            self.oe = oeMain
            self.dbusSystemBus = oeMain.dbusSystemBus
            self.mainLoop = gobject.MainLoop()
            gobject.threads_init()
            dbus.mainloop.glib.threads_init()
            threading.Thread.__init__(self)
            self.oe.dbg_log('xdbus::dbusMonitor::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('xdbus::dbusMonitor::__init__', 'ERROR: (' + repr(e) + ')', 4)

    def run(self):
        try:
            self.oe.dbg_log('xdbus::dbusMonitor::run', 'enter_function', 0)
            for strModule in sorted(self.oe.dictModules, key=lambda x: self.oe.dictModules[x].menu.keys()):
                module = self.oe.dictModules[strModule]
                if hasattr(module, 'monitor') and module.ENABLED:
                    monitor = module.monitor(self.oe, module)
                    monitor.add_signal_receivers()
                    self.monitors.append(monitor)
            try:
                self.oe.dbg_log('xdbus Monitor started.', '', 1)
                self.mainLoop.run()
                self.oe.dbg_log('xdbus Monitor stopped.', '', 1)
            except:
                pass
            self.oe.dbg_log('xdbus::dbusMonitor::run', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('xdbus::dbusMonitor::run', 'ERROR: (' + repr(e) + ')', 4)

    def stop(self):
        try:
            self.oe.dbg_log('xdbus::dbusMonitor::stop_service', 'enter_function', 0)
            self.mainLoop.quit()
            for monitor in self.monitors:
                monitor.remove_signal_receivers()
                monitor = None
            self.oe.dbg_log('xdbus::dbusMonitor::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('xdbus::dbusMonitor::stop_service', 'ERROR: (' + repr(e) + ')')


