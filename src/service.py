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

import oe
import xbmc
import xbmcgui
import time
import threading
import socket
import os
import xbmcaddon


class service_thread(threading.Thread):

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('_service_::__init__', 'enter_function', 0)
            self.oe = oeMain
            self.wait_evt = threading.Event()
            self.socket_file = '/var/run/service.openelec.settings.sock'
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.setblocking(1)
            if os.path.exists(self.socket_file):
                os.remove(self.socket_file)
            self.sock.bind(self.socket_file)
            self.sock.listen(1)
            self.stopped = False
            threading.Thread.__init__(self)
            self.daemon = True
            self.oe.dbg_log('_service_::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('_service_::__init__', 'ERROR: (' + repr(e) + ')')

    def stop(self):
        try:
            self.oe.dbg_log('_service_::stop', 'enter_function', 0)
            self.stopped = True
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.socket_file)
            sock.send('exit')
            sock.close()
            self.sock.close()
            self.oe.dbg_log('_service_::stop', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('_service_::stop', 'ERROR: (' + repr(e) + ')')

    def run(self):
        try:
            self.oe.dbg_log('_service_::run', 'enter_function', 0)
            if self.oe.read_setting('openelec', 'wizard_completed') == None:
                threading.Thread(target=self.oe.openWizard).start()
            while self.stopped == False:
                self.oe.dbg_log('_service_::run', 'WAITING:', 1)
                (conn, addr) = self.sock.accept()
                message = conn.recv(1024)
                self.oe.dbg_log('_service_::run', 'MESSAGE:' + repr(message), 1)
                conn.close()
                if message == 'openConfigurationWindow':
                    if not hasattr(self.oe, 'winOeMain'):
                        threading.Thread(target=self.oe.openConfigurationWindow).start()
                    else:
                        if self.oe.winOeMain.visible != True:
                            threading.Thread(target=self.oe.openConfigurationWindow).start()
                if message == 'exit':
                    self.stopped = True
            self.oe.dbg_log('_service_::run', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('_service_::run', 'ERROR: (' + repr(e) + ')')


class cxbmcm(xbmc.Monitor):

    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onScreensaverActivated(self):
        oe.__oe__.dbg_log('c_xbmcm::onScreensaverActivated', 'enter_function', 0)
        if 'bluetooth' in oe.__oe__.dictModules:
            oe.__oe__.dictModules['bluetooth'].standby_devices()
        oe.__oe__.dbg_log('c_xbmcm::onScreensaverActivated', 'exit_function', 0)

    def onAbortRequested(self):
        pass


xbmcm = cxbmcm()
oe.load_modules()
oe.start_service()
monitor = service_thread(oe.__oe__)
monitor.start()

xbmcm.waitForAbort()

if hasattr(oe, 'winOeMain'):
    if oe.winOeMain.visible == True:
        oe.winOeMain.close()

oe.stop_service()
monitor.stop()
