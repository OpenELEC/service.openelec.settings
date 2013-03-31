# -*- coding: utf-8 -*-
import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('/var/run/service.openelec.settings.sock')
sock.send('openConfigurationWindow')
sock.close()
