# -*- coding: utf-8 -*-
import oe
import xbmc
import time
import threading
import socket
import os


class service_thread(threading.Thread):

    def __init__(self, oeMain):
        try:

            oeMain.dbg_log('_service_::__init__', 'enter_function', 0)

            self.oe = oeMain
            self.socket_file = '/var/run/service.openelec.settings.sock'

            self.sock = socket.socket(socket.AF_UNIX,
                    socket.SOCK_STREAM)
            self.sock.setblocking(1)

            if os.path.exists(self.socket_file):
                os.remove(self.socket_file)

            self.sock.bind(self.socket_file)
            self.sock.listen(1)

            self.stopped = False

            threading.Thread.__init__(self)

            self.oe.dbg_log('_service_::__init__', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('_service_::__init__', 'ERROR: (' + repr(e)
                            + ')')

    def stop(self):
        try:

            self.oe.dbg_log('_service_::stop', 'enter_function', 0)

            self.stopped = True

            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.socket_file)
            sock.send('exit')
            sock.close()
            self.sock.close()

            self.oe.dbg_log('_service_::stop', 'enter_function', 0)
        except Exception, e:

            self.oe.dbg_log('_service_::stop', 'ERROR: (' + repr(e)
                            + ')')

    def run(self):
        try:

            self.oe.dbg_log('_service_::run', 'enter_function', 0)

            while self.stopped == False:

                (conn, addr) = self.sock.accept()
                message = conn.recv(1024)
                self.oe.dbg_log('_service_::run', 'MESSAGE:'
                                + repr(message), 1)
                conn.close()

                if message == 'openConfigurationWindow':
                    self.oe.openConfigurationWindow()

                if message == 'exit':
                    self.stopped = True

            self.oe.dbg_log('_service_::run', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('_service_::run', 'ERROR: (' + repr(e) + ')'
                            )


oe.start_service()

monitor = service_thread(oe.__oe__)
monitor.start()

while not xbmc.abortRequested:
    time.sleep(0.2)

oe.stop_service()
monitor.stop()
