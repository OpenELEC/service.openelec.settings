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
import os

################################################################################
# Base 
################################################################################
XBMC_USER_HOME = os.environ.get('XBMC_USER_HOME', '/storage/.xbmc')
CONFIG_CACHE = os.environ.get('CONFIG_CACHE', '/storage/.cache')
USER_CONFIG = os.environ.get('USER_CONFIG', '/storage/.config')

################################################################################
# Connamn Module
################################################################################
connman = \
    {
        'CONNMAN_DAEMON'  : "/usr/sbin/connmand",
        'WAIT_CONF_FILE'  : '%s/openelec/network_wait' % CONFIG_CACHE,
        'VPN_PLUGINS_DIR' : '/usr/lib/connman/plugins-vpn',
        'VPN_CONF_DIR'    : '%s/vpn-config/' % USER_CONFIG,
        'ENABLED'         : lambda:(True if os.path.exists(connman['CONNMAN_DAEMON']) else False),
    }

################################################################################
# Bluez Module
################################################################################
bluetooth = \
    {
        'BLUETOOTH_DAEMON' : '/usr/lib/bluetooth/bluetoothd',
        'OBEX_DAEMON'      : '/usr/lib/bluetooth/obexd',
        'BLUETOOTH_INIT'   : '/etc/init.d/54_bluez',
        'OBEX_INIT'        : '/etc/init.d/55_obexd',       
        'OBEX_ROOT'        : '/storage/downloads',
        'ENABLED'          : lambda:(True if os.path.exists(connman['BLUETOOTH_DAEMON']) else False),
    }

################################################################################
# Service Module
################################################################################    
services = \
    {
        'ENABLED'       : True,
                
      #SAMBA
        'KERNEL_CMD'    : '/proc/cmdline',
        'SAMBA_NMDB'    : '/usr/bin/nmbd',
        'SAMBA_SMDB'    : '/usr/bin/smbd',
        'SAMBA_INIT'    : '/etc/init.d/52_samba',
        'NMDB_PARM'     : '--daemon --configfile=',
        'SMDB_PARM'     : '--daemon --configfile=',
        
      #SSH
        'SSH_DAEMON'    : '/usr/sbin/sshd',
        'SSH_INIT'      : '/etc/init.d/51_sshd',
        'SSH_PARM'      : '',
        
      #AVAHI
        'AVAHI_DAEMON'  : '/usr/sbin/avahi-daemon',
        'AVAHI_INIT'    : '/etc/init.d/53_avahi',
        'AVAHI_PARM'    : '--syslog',
        
      #CRON
        'CRON_DAEMON'   : '/sbin/crond',
        'CRON_INIT'     : '/etc/init.d/09_crond',
        'CRON_PARM'     : '-b',

      #SYSLOG
        'SYSLOG_DAEMON' : '/sbin/syslogd',
        'SYSLOG_INIT'   : '/etc/init.d/05_syslogd',  
        'SYSLOG_PARM'   : '-L',
    }
    
system = \
    {
        'ENABLED'             : True,
        'KERNEL_CMD'          : '/proc/cmdline',
        
      #CLOCK
        'SET_CLOCK_CMD'       : '/sbin/hwclock --systohc --utc',
        
      #LCD
        'LCD_DRIVER_DIR'      : '/usr/lib/lcdproc/',

      #UPDATE
        'UPDATE_REQUEST_URL'  : 'http://update.openelec.tv/updates.php',
        'UPDATE_DOWNLOAD_URL' : 'http://%s.openelec.tv/%s',
        'LOCAL_UPDATE_DIR'    : '/storage/.update/',
        'GET_CPU_FLAG'        : 'cat /proc/cpuinfo | grep -q "flags.* lm " && echo "1" || echo "0"',
        
      #RESET
        'XBMC_RESET_FILE'     : '%s/reset_xbmc' % CONFIG_CACHE,
        'OPENELEC_RESET_FILE' : '%s/reset_oe' % CONFIG_CACHE,

      #KEYBOARD
        'KEYBOARD_INFO'       : '/usr/share/X11/xkb/rules/base.xml',
        'UDEV_KEYBOARD_INFO'  : '%s/xkb/layout' % CONFIG_CACHE,
        'RPI_KEYBOARD_INFO'   : '/usr/lib/keymaps',
            
      #BACKUP / RESTORE
        'BACKUP_DIRS'         : [XBMC_USER_HOME, USER_CONFIG, CONFIG_CACHE],
        'BACKUP_DESTINATION'  : '/storage/backup/',
        'RESTORE_DIR'         : '/storage/.restore/',
    }
    
about = \
    {
        'ENABLED' : True
    }    
    
xdbus = \
    {
        'ENABLED' : True
    }    