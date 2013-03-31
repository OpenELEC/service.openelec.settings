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
import xbmc
import xbmcgui
import os
import glob
import threading
import time
import re
import zipfile
import stat
import mimetypes
import httplib

from xml.dom import minidom


class system:

    oe = None
    menu = {'1': {
        'name': 32002,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 700,
        }}

    def __init__(self, oeMain):
        try:

            oeMain.dbg_log('system::__init__', 'enter_function', 0)

            self.oe = oeMain

            self.config = {
                'ident': {
                    'order': 1,
                    'name': 32189,
                    'not_supported': [],
                    'settings': {'hostname': {
                        'name': 32190,
                        'value': 'openelec',
                        'action': 'set_hostname',
                        'typ': 'text',
                        'validate': '^([a-zA-Z0-9](?:[a-zA-Z0-9-\.]*[a-zA-Z0-9]))$',
                        'InfoText': 710,
                        }},
                    },
                'keyboard': {
                    'order': 2,
                    'name': 32009,
                    'not_supported': ['RPi.arm'],
                    'settings': {'KeyboardLayout1': {
                        'name': 32010,
                        'value': 'us',
                        'action': 'set_keyboard_layout',
                        'typ': 'multivalue',
                        'values': [],
                        'InfoText': 711,
                        }, 'KeyboardLayout2': {
                        'name': 32010,
                        'value': 'us',
                        'action': 'set_keyboard_layout',
                        'typ': 'multivalue',
                        'values': [],
                        'InfoText': 712,
                        }, 'KeyboardType': {
                        'name': 32330,
                        'value': 'pc105',
                        'action': 'set_keyboard_layout',
                        'typ': 'multivalue',
                        'values': [],
                        'InfoText': 713,
                        }},
                    },
                'update': {
                    'order': 3,
                    'name': 32013,
                    'not_supported': [],
                    'settings': {'AutoUpdate': {
                        'name': 32014,
                        'value': 'manual',
                        'action': 'set_auto_update',
                        'typ': 'multivalue',
                        'values': ['manual', 'auto'],
                        'InfoText': 714,
                        }, 'UpdateNotify': {
                        'name': 32365,
                        'value': '1',
                        'action': 'set_value',
                        'typ': 'bool',
                        'InfoText': 715,
                        }, 'CheckUpdate': {
                        'name': 32362,
                        'value': '',
                        'action': 'manual_check_update',
                        'typ': 'button',
                        'parent': {'entry': 'AutoUpdate',
                                   'value': ['manual']},
                        'InfoText': 716,
                        }},
                    },
                'driver': {
                    'order': 4,
                    'name': 32007,
                    'not_supported': [],
                    'settings': {'lcd': {
                        'name': 32008,
                        'value': 'none',
                        'action': 'set_lcd_driver',
                        'typ': 'multivalue',
                        'values': [],
                        'InfoText': 717,
                        }},
                    },
                'power': {
                    'order': 5,
                    'name': 32011,
                    'not_supported': [],
                    'settings': {'enable_hdd_standby': {
                        'name': 32347,
                        'value': '0',
                        'action': 'set_hdd_standby',
                        'typ': 'bool',
                        'InfoText': 718,
                        }, 'hdd_standby': {
                        'name': 32012,
                        'value': '0',
                        'action': 'set_hdd_standby',
                        'typ': 'num',
                        'parent': {'entry': 'enable_hdd_standby',
                                   'value': ['1']},
                        'InfoText': 719,
                        }, 'disable_bt': {
                        'name': 32344,
                        'value': '0',
                        'action': 'init_bluetooth',
                        'typ': 'bool',
                        'InfoText': 720,
                        }},
                    },
                'support': {
                    'order': 6,
                    'name': 32359,
                    'not_supported': [],
                    'settings': {'upload': {
                        'name': 32214,
                        'value': '0',
                        'action': 'upload_logfiles',
                        'typ': 'button',
                        'InfoText': 721,
                        }},
                    },
                'backup': {
                    'order': 7,
                    'name': 32371,
                    'not_supported': [],
                    'settings': {'backup': {
                        'name': 32372,
                        'value': '0',
                        'action': 'do_backup',
                        'typ': 'button',
                        'InfoText': 722,
                        }, 'restore': {
                        'name': 32373,
                        'value': '0',
                        'action': 'do_restore',
                        'typ': 'button',
                        'InfoText': 723,
                        }},
                    },
                'reset': {
                    'order': 7,
                    'name': 32323,
                    'not_supported': [],
                    'settings': {'xbmc_reset': {
                        'name': 32324,
                        'value': '0',
                        'action': 'reset_xbmc',
                        'typ': 'button',
                        'InfoText': 724,
                        }, 'oe_reset': {
                        'name': 32325,
                        'value': '0',
                        'action': 'reset_oe',
                        'typ': 'button',
                        'InfoText': 725,
                        }},
                    },
                }

            self.lcd_dir = '/usr/lib/lcdproc/'
            self.envFile = '/storage/oe_environment'
            self.keyboard_layouts = False
            self.update_url_release = 'http://releases.openelec.tv'
            self.update_url_devel = 'http://snapshots.openelec.tv' #'http://update.openelec.tv'
            self.temp_folder = os.environ['HOME'] + '/.xbmc/temp/'
            self.update_folder = '/storage/.update/'
            self.last_update_check = 0
            self.xbmc_reset_file = '/storage/.cache/reset_xbmc'
            self.oe_reset_file = '/storage/.cache/reset_oe'

            self.keyboard_info = '/usr/share/X11/xkb/rules/base.xml'
            self.udev_keyboard_file = '/storage/.cache/xkb/layout'
            self.bt_daemon = '/usr/lib/bluetooth/bluetoothd'

            self.backup_dirs = ['/storage/.xbmc', '/storage/.config',
                                '/storage/.cache']
            self.backup_file = 'openelec_backup.zip'
            self.restore_path = '/storage/.restore/'

            oeMain.dbg_log('system::__init__', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::__init__', 'ERROR: (' + repr(e)
                            + ')')

    def start_service(self):
        try:

            self.oe.dbg_log('system::start_service', 'enter_function',
                            0)

            self.is_service = True

            self.load_values()
            self.set_hostname()
            self.set_keyboard_layout()
            self.set_lcd_driver()
            self.set_hdd_standby()
            self.set_hw_clock()
            self.set_cpupower()
            self.init_bluetooth()
            self.set_auto_update()

            self.oe.dbg_log('system::start_service', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::start_service', 'ERROR: ('
                            + repr(e) + ')')

    def stop_service(self):
        try:

            self.oe.dbg_log('system::stop_service', 'enter_function', 0)

            self.stop_bluetoothd()
            self.update_thread.stop()

            self.oe.dbg_log('system::stop_service', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::stop_service', 'ERROR: ('
                            + repr(e) + ')')

    def do_init(self):
        try:

            self.oe.dbg_log('system::do_init', 'enter_function', 0)
            self.oe.dbg_log('system::do_init', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::do_init', 'ERROR: (' + repr(e)
                            + ')')

    def exit(self):
        self.oe.dbg_log('system::exit', 'enter_function', 0)
        self.oe.dbg_log('system::exit', 'exit_function', 0)
        pass

    def load_values(self):
        try:

            self.oe.dbg_log('system::load_values', 'enter_function', 0)

            # Keyboard Layout
            (arrLayouts, arrTypes) = self.get_keyboard_layouts()
            arrLcd = self.get_lcd_drivers()

            self.arch = self.oe.load_file('/etc/arch')

            if not arrTypes is None:

                self.config['keyboard']['settings']['KeyboardType'
                        ]['values'] = arrTypes

                value = self.oe.read_setting('system', 'KeyboardType')
                if not value is None:
                    self.config['keyboard']['settings']['KeyboardType'
                            ]['value'] = value

            if not arrLayouts is None:

                self.config['keyboard']['settings']['KeyboardLayout1'
                        ]['values'] = arrLayouts
                self.config['keyboard']['settings']['KeyboardLayout2'
                        ]['values'] = arrLayouts

                value = self.oe.read_setting('system', 'KeyboardLayout1'
                        )
                if not value is None:
                    self.config['keyboard']['settings'
                            ]['KeyboardLayout1']['value'] = value

                value = self.oe.read_setting('system', 'KeyboardLayout2'
                        )
                if not value is None:
                    self.config['keyboard']['settings'
                            ]['KeyboardLayout2']['value'] = value

                self.keyboard_layouts = True

            # Hostname
            value = self.oe.read_setting('system', 'hostname')
            if not value is None:
                self.config['ident']['settings']['hostname']['value'] = \
                    value

            # LCD Driver
            if not arrLcd is None:
                self.config['driver']['settings']['lcd']['values'] = \
                    arrLcd

            value = self.oe.read_setting('system', 'lcd')
            if not value is None:
                self.config['driver']['settings']['lcd']['value'] = \
                    value

            # HDD Standby
            value = self.oe.read_setting('system', 'hdd_standby')
            if not value is None:
                self.config['power']['settings']['hdd_standby']['value'
                        ] = value

            # Disable Bluetooth
            value = self.oe.read_setting('system', 'disable_bt')
            if not value is None:
                self.config['power']['settings']['disable_bt']['value'
                        ] = value

            # AutoUpdate
            value = self.oe.read_setting('system', 'AutoUpdate')
            if not value is None:
                self.config['update']['settings']['AutoUpdate']['value'
                        ] = value

            value = self.oe.read_setting('system', 'UpdateNotify')
            if not value is None:
                self.config['update']['settings']['UpdateNotify'
                        ]['value'] = value

            # AutoUpdate File and URL
            value = self.oe.read_setting('system', 'update_file')
            if value != None and value != '':
                self.update_file = value
            value = self.oe.read_setting('system', 'update_url')
            if value != None and value != '':
                self.update_url = value

            self.oe.dbg_log('system::load_values', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::load_values', 'ERROR: (' + repr(e)
                            + ')')

    def load_menu(self, focusItem):

        try:

            self.oe.dbg_log('system::load_menu', 'enter_function', 0)

            selectedPos = \
                self.oe.winOeMain.getControl(self.oe.winOeMain.guiList).getSelectedPosition()

            for category in sorted(self.config, key=lambda x: \
                                   self.config[x]['order']):
                if 'not_supported' in self.config[category]:
                    if self.arch \
                        in self.config[category]['not_supported']:
                        continue

                self.oe.winOeMain.addConfigItem(self.oe._(self.config[category]['name'
                        ]), {'typ': 'separator'},
                        focusItem.getProperty('listTyp'))

                for setting in sorted(self.config[category]['settings'
                        ]):
                    dictProperties = {
                        'entry': setting,
                        'category': category,
                        'action': self.config[category]['settings'
                                ][setting]['action'],
                        'value': self.config[category]['settings'
                                ][setting]['value'],
                        'typ': self.config[category]['settings'
                                ][setting]['typ'],
                        }

                    if 'InfoText' in self.config[category]['settings'
                            ][setting]:
                        dictProperties['InfoText'] = \
                            self.oe._(self.config[category]['settings'
                                ][setting]['InfoText'])

                    if 'validate' in self.config[category]['settings'
                            ][setting]:
                        dictProperties['validate'] = \
                            self.config[category]['settings'
                                ][setting]['validate']

                    if 'values' in self.config[category]['settings'
                            ][setting]:
                        if len(self.config[category]['settings'
                               ][setting]['values']) > 0:
                            dictProperties['values'] = \
                                ','.join(self.config[category]['settings'
                                    ][setting]['values'])

                    if not 'parent' in self.config[category]['settings'
                            ][setting]:

                        self.oe.winOeMain.addConfigItem(self.oe._(self.config[category]['settings'
                                ][setting]['name']), dictProperties,
                                focusItem.getProperty('listTyp'))
                    else:

                        if self.config[category]['settings'
                                ][self.config[category]['settings'
                                  ][setting]['parent']['entry']]['value'
                                ] in self.config[category]['settings'
                                ][setting]['parent']['value']:

                            self.oe.winOeMain.addConfigItem(self.oe._(self.config[category]['settings'
                                    ][setting]['name']),
                                    dictProperties,
                                    focusItem.getProperty('listTyp'))

                if category == 'update':
                    if hasattr(self, 'update_file'):
                        if self.update_file != '':
                            if self.config['update']['settings'
                                    ]['AutoUpdate']['value'] == 'auto':

                                dictProperties = {
                                    'entry': 'do_autoupdate',
                                    'category': 'update',
                                    'action': 'do_autoupdate',
                                    'value': '',
                                    'typ': 'button',
                                    }

                                self.oe.winOeMain.addConfigItem(self.oe._(32197),
                                        dictProperties,
                                        focusItem.getProperty('listTyp'
                                        ))

            self.oe.winOeMain.getControl(self.oe.winOeMain.guiList).selectItem(selectedPos)

            self.oe.dbg_log('system::load_menu', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::loadSysMenu', 'ERROR: (' + repr(e)
                            + ')')

    def set_value(self, listItem):
        try:

            self.oe.dbg_log('system::set_value', 'enter_function', 0)

            self.config[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')

            self.oe.write_setting('system', listItem.getProperty('entry'
                                  ), str(listItem.getProperty('value')))

            self.oe.dbg_log('system::set_value', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::set_value', 'ERROR: (' + repr(e)
                            + ')')

    def init_bluetooth(self, listItem=None):
        try:

            self.oe.dbg_log('system::init_bluetooth', 'enter_function',
                            0)

            self.oe.set_busy(1)

            if not listItem == None:
                self.set_value(listItem)

            if self.config['power']['settings']['disable_bt']['value'] \
                == '0' or self.config['power']['settings']['disable_bt'
                    ]['value'] == None:

                pid = self.oe.execute('pidof %s'
                        % os.path.basename(self.bt_daemon)).split(' ')
                if pid[0] == '':
                    self.oe.dbg_log('system::init_bluetooth',
                                    'Starting Bluetooth Daemon.', 0)
                    os.system(self.bt_daemon + ' &')
                    time.sleep(1)
                else:

                    self.oe.dbg_log('system::init_bluetooth',
                                    'Bluetooth Daemon is always running.'
                                    , 0)

                if not hasattr(self, 'is_service'):
                    self.oe.dictModules['bluetooth'].exit()
                    self.oe.dictModules['bluetooth'].do_init()
            else:

                if 'bluetooth' in self.oe.dictModules \
                    and not hasattr(self, 'is_service'):
                    self.oe.dictModules['bluetooth'].exit()
                    self.oe.dictModules['bluetooth'].do_init()

                self.oe.dbg_log('bluetooth::do_init',
                                'exit_function (No Adapter Found)', 0)

                self.stop_bluetoothd()

            self.oe.set_busy(0)

            self.oe.dbg_log('system::init_bluetooth', 'exit_function',
                            0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::init_bluetooth', 'ERROR: ('
                            + repr(e) + ')', 4)

    def stop_bluetoothd(self):
        try:

            self.oe.dbg_log('system::stop_bluetoothd', 'enter_function'
                            , 0)

            pid = self.oe.execute('pidof %s'
                                  % os.path.basename(self.bt_daemon)).split(' '
                    )
            for p in pid:
                os.system('kill -9 ' + p.strip().replace('\n', ''))

            self.oe.dbg_log('system::stop_bluetoothd', 'exit_function',
                            0)
        except Exception, e:

            self.oe.dbg_log('system::stop_bluetoothd', 'ERROR: ('
                            + repr(e) + ')', 4)

    def set_keyboard_layout(self, listItem=None):
        try:

            self.oe.dbg_log('system::set_keyboard_layout',
                            'enter_function', 0)

            self.oe.set_busy(1)

            if self.keyboard_layouts == False:
                self.oe.set_busy(0)
                return

            if not listItem == None:
                self.set_value(listItem)

            self.oe.dbg_log('system::set_keyboard_layout',
                            str(self.config['keyboard']['settings'
                            ]['KeyboardLayout1']['value']) + ','
                            + str(self.config['keyboard']['settings'
                            ]['KeyboardLayout2']['value']) + ' '
                            + '-model ' + str(self.config['keyboard'
                            ]['settings']['KeyboardType']['value']), 1)

            if not os.path.exists(os.path.dirname(self.udev_keyboard_file)):
                os.makedirs(os.path.dirname(self.udev_keyboard_file))

            config_file = open(self.udev_keyboard_file, 'w')
            config_file.write('XKBMODEL="' + self.config['keyboard'
                              ]['settings']['KeyboardType']['value']
                              + '"\n')
            config_file.write('XKBVARIANT=""\n')
            config_file.write('XKBLAYOUT="' + self.config['keyboard'
                              ]['settings']['KeyboardLayout1']['value']
                              + ',' + self.config['keyboard']['settings'
                              ]['KeyboardLayout2']['value'] + '"\n')
            config_file.write('XKBOPTIONS="grp:alt_shift_toggle"\n')
            config_file.close()

            parameters = ['-display ' + os.environ['DISPLAY'],
                          '-layout ' + self.config['keyboard'
                          ]['settings']['KeyboardLayout1']['value']
                          + ',' + self.config['keyboard']['settings'
                          ]['KeyboardLayout2']['value'], '-model '
                          + str(self.config['keyboard']['settings'
                          ]['KeyboardType']['value']),
                          '-option "grp:alt_shift_toggle"']

            result = self.oe.execute('setxkbmap '
                    + ' '.join(parameters))

            self.oe.set_busy(0)

            self.oe.dbg_log('system::set_keyboard_layout',
                            'exit_function', 0)

            return result
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::set_keyboard_layout', 'ERROR: ('
                            + repr(e) + ')')

    def set_hostname(self, listItem=None):
        try:

            self.oe.dbg_log('system::set_hostname', 'enter_function', 0)

            self.oe.set_busy(1)

            if not listItem == None:
                self.set_value(listItem)

            if not self.config['ident']['settings']['hostname']['value'
                    ] is None and not self.config['ident']['settings'
                    ]['hostname']['value'] == '':

                self.oe.dbg_log('system::set_hostname',
                                self.config['ident']['settings'
                                ]['hostname']['value'], 1)

                hostname = open('/proc/sys/kernel/hostname', 'w')
                hostname.write(self.config['ident']['settings'
                               ]['hostname']['value'])
                hostname.close()

                hosts = open('/etc/hosts', 'w')
                user_hosts_file = os.environ['HOME'] \
                    + '/.config/hosts.conf'

                if os.path.isfile(user_hosts_file):
                    user_hosts = open(user_hosts_file, 'r')
                    hosts.write(user_hosts.read())
                    user_hosts.close()

                hosts.write('127.0.0.1\tlocalhost %s\n'
                            % self.config['ident']['settings'
                            ]['hostname']['value'])
                hosts.close()
            else:

                self.oe.dbg_log('system::set_hostname', 'is empty', 1)

            self.oe.set_busy(0)

            self.oe.dbg_log('system::set_hostname', 'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::set_hostname', 'ERROR: ('
                            + repr(e) + ')')

    def set_lcd_driver(self, listItem=None):
        try:

            self.oe.dbg_log('system::set_lcd_driver', 'enter_function',
                            0)

            self.oe.set_busy(1)

            if not listItem == None:
                self.set_value(listItem)

            if os.path.isfile('/storage/.config/LCDd.conf'):
                lcd_config_file = '/storage/.config/LCDd.conf'
            else:
                lcd_config_file = '/etc/LCDd.conf'

            if not self.config['driver']['settings']['lcd']['value'] \
                is None and not self.config['driver']['settings']['lcd'
                    ]['value'] == 'none':

                self.oe.dbg_log('system::set_lcd_driver',
                                self.config['driver']['settings']['lcd'
                                ]['value'], 1)

                parameters = ['-c ' + lcd_config_file, '-d '
                              + self.config['driver']['settings']['lcd'
                              ]['value'], '-s true']

                os.system('LCDd ' + ' '.join(parameters))
            else:

                self.oe.dbg_log('system::set_lcd_driver',
                                'no driver selected', 1)

            self.oe.set_busy(0)

            self.oe.dbg_log('system::set_lcd_driver', 'exit_function',
                            0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::set_lcd_driver', 'ERROR: ('
                            + repr(e) + ')')

    def set_hdd_standby(self, listItem=None):
        try:

            self.oe.dbg_log('system::set_hdd_standby', 'enter_function'
                            , 0)

            self.oe.set_busy(1)

            if not listItem == None:
                self.set_value(listItem)

            if self.config['power']['settings']['hdd_standby']['value'] \
                != None and self.config['power']['settings'
                    ]['hdd_standby']['value'] != '0' \
                and self.config['power']['settings'
                    ]['enable_hdd_standby']['value'] == '1':

                value = int(self.config['power']['settings'
                            ]['hdd_standby']['value']) * 12

                for device in glob.glob('/dev/sd?'):

                    self.oe.dbg_log('system::set_hdd_standby',
                                    str(value), 1)

                    parameters = ['-S ' + str(value), device]

                    os.system('hdparm ' + ' '.join(parameters))
            else:

                for device in glob.glob('/dev/sd?'):

                    self.oe.dbg_log('system::set_hdd_standby', '0 (off)'
                                    , 1)

                    parameters = ['-S 0 ', device]

                    os.system('hdparm ' + ' '.join(parameters))

            self.oe.set_busy(0)

            self.oe.dbg_log('system::set_hdd_standby', 'exit_function',
                            0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::set_lcd_driver', 'ERROR: ('
                            + repr(e) + ')')

    def manual_check_update(self, listItem=None):
        try:

            self.oe.dbg_log('system::manual_check_update',
                            'enter_function', 0)

            self.check_updates(True)

            self.oe.dbg_log('system::manual_check_update',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::manual_check_update', 'ERROR: ('
                            + repr(e) + ')')

    def set_auto_update(self, listItem=None):
        try:

            self.oe.dbg_log('system::set_auto_update', 'enter_function'
                            , 0)

            if not listItem == None:
                self.set_value(listItem)

            if not hasattr(self, 'update_thread'):
                self.update_thread = updateThread(self.oe)
                self.update_thread.start()

            self.update_thread.last_check = 0
            self.last_update_check = 0

            self.oe.dbg_log('system::set_auto_update',
                            str(self.config['update']['settings'
                            ]['AutoUpdate']['value']), 1)

            self.oe.dbg_log('system::set_auto_update', 'exit_function',
                            0)
        except Exception, e:

            self.oe.dbg_log('system::set_auto_update', 'ERROR: ('
                            + repr(e) + ')')

    def get_keyboard_layouts(self):
        try:

            self.oe.dbg_log('system::get_keyboard_layouts',
                            'enter_function', 0)

            arrLayouts = []
            arrTypes = []

            if not os.path.exists(self.keyboard_info):
                self.oe.dbg_log('system::get_keyboard_layouts',
                                'exit_function (xml not found. RPI ?)',
                                0)
                return (None, None)

            objXmlFile = open(self.keyboard_info, 'r')
            strXmlText = objXmlFile.read()
            objXmlFile.close()

            xml_conf = minidom.parseString(strXmlText)

            for xml_layout in xml_conf.getElementsByTagName('layout'):
                for subnode_1 in xml_layout.childNodes:
                    if subnode_1.nodeName == 'configItem':
                        for subnode_2 in subnode_1.childNodes:
                            if subnode_2.nodeName == 'name':
                                if hasattr(subnode_2.firstChild,
                                        'nodeValue'):
                                    value = \
    subnode_2.firstChild.nodeValue
                            if subnode_2.nodeName == 'description':
                                if hasattr(subnode_2.firstChild,
                                        'nodeValue'):
                                    arrLayouts.append(value + ':'
        + subnode_2.firstChild.nodeValue)

            for xml_layout in xml_conf.getElementsByTagName('model'):
                for subnode_1 in xml_layout.childNodes:
                    if subnode_1.nodeName == 'configItem':
                        for subnode_2 in subnode_1.childNodes:
                            if subnode_2.nodeName == 'name':
                                if hasattr(subnode_2.firstChild,
                                        'nodeValue'):
                                    value = \
    subnode_2.firstChild.nodeValue
                            if subnode_2.nodeName == 'description':
                                if hasattr(subnode_2.firstChild,
                                        'nodeValue'):
                                    arrTypes.append(value + ':'
        + subnode_2.firstChild.nodeValue)

            arrLayouts.sort()
            arrTypes.sort()

            self.oe.dbg_log('system::get_keyboard_layouts',
                            'exit_function', 0)

            return (arrLayouts, arrTypes)
        except Exception, e:

            self.oe.dbg_log('system::get_keyboard_layouts', 'ERROR: ('
                            + repr(e) + ')')

    def get_lcd_drivers(self):
        try:

            self.oe.dbg_log('system::get_lcd_drivers', 'enter_function'
                            , 0)

            if os.path.exists(self.lcd_dir):
                arrDrivers = ['none']

                for driver in glob.glob(self.lcd_dir + '*'):
                    arrDrivers.append(os.path.basename(driver).replace('.so'
                            , ''))
            else:

                arrDrivers = None

            self.oe.dbg_log('system::get_lcd_drivers', 'exit_function',
                            0)

            return arrDrivers
        except Exception, e:

            self.oe.dbg_log('system::get_lcd_drivers', 'ERROR: ('
                            + repr(e) + ')')

    def check_updates(self, force=False):
        try:

            self.oe.dbg_log('system::check_updates', 'enter_function',
                            0)

            value = self.oe.read_setting('system', 'AutoUpdate')
            if not value is None:
                if self.config['update']['settings']['AutoUpdate'
                        ]['value'] != value:
                    self.last_update_check = 0

                self.config['update']['settings']['AutoUpdate']['value'
                        ] = value

            if time.time() < self.last_update_check + 21600 \
                and not force:
                return

            self.oe.dbg_log('system::check_updates', 'enter_function', 0)

            self.oe.write_setting('system', 'update_file', '')
            self.oe.write_setting('system', 'update_url', '')

            self.last_update_check = time.time()

            auto_update = False
            manual_update = False

            distri = self.oe.load_file('/etc/distribution')
            arch = self.oe.load_file('/etc/arch')
            version = self.oe.load_file('/etc/version')
            update = ''

            if version.startswith('devel'):

                version = version.rsplit('-', 1)
                current_version = version[len(version) - 1].replace('r'
                        , '')

                release = distri + '-' + arch
                self.update_url = self.update_url_devel
                latest = self.oe.load_url(self.update_url + '/latest')

                for line in latest.splitlines():
                    if release.lower() in line.lower():
                        update = line.strip()
                        break

                if update == '':
                    self.oe.dbg_log('system::check_updates',
                                    'no update found', 1)
                    return

                line = line.rsplit('-', 1)
                latest_version = line[len(line) - 1].replace('r', '')

                if int(latest_version) > int(current_version):
                    auto_update = True
                    manual_update = True
            else:

                version = version.rsplit('-', 1)
                current_version = version[len(version) - 1].split('.')

                current_major = int(current_version[0])
                current_minor = int(current_version[1])
                current_patch = int(current_version[2])

                release = distri + '-' + arch
                self.update_url = self.update_url_release
                latest = self.oe.load_url(self.update_url + '/latest')

                for line in latest.splitlines():
                    if release.lower() in line.lower():
                        update = line.strip()
                        break

                if update == '':
                    self.oe.dbg_log('system::check_updates',
                                    'no update found', 1)
                    return

                line = line.rsplit('-', 1)
                latest_version = line[len(line) - 1].split('.')

                latest_major = int(latest_version[0])
                latest_minor = int(latest_version[1])
                latest_patch = int(latest_version[2])

                if current_major == latest_major and current_minor \
                    == latest_minor and current_patch < latest_patch:
                    auto_update = True

                if current_major == latest_major and current_minor \
                    < latest_minor and latest_minor < 90:
                    auto_update = True

                if current_major == latest_major and current_minor \
                    < latest_minor and latest_minor > 90 \
                    and current_minor > 90:
                    auto_update = True

                if current_minor > 90 and latest_minor < 90 \
                    and current_major == latest_major - 1:
                    auto_update = True

                if current_major == latest_major - 1 and latest_minor \
                    < 90 and auto_update == False:
                    manual_update = True

                current_version = '.'.join(current_version)
                latest_version = '.'.join(latest_version)

            if auto_update == True or manual_update == True:
                if self.config['update']['settings']['AutoUpdate'
                        ]['value'] == 'auto' or manual_update == True:
                    if self.config['update']['settings']['UpdateNotify'
                            ]['value'] == '1':
                        xbmc.executebuiltin('Notification('
                                + self.oe._(32363) + ', '
                                + self.oe._(32364) + ')')
            else:

                self.oe.dbg_log('system::check_updates',
                                'no update found', 0)
                self.oe.dbg_log('system::check_updates', 'latest :'
                                + str(latest_version), 0)
                self.oe.dbg_log('system::check_updates', 'current:'
                                + str(current_version), 0)

            if (self.config['update']['settings']['AutoUpdate']['value'
                ] == 'auto' or force) and auto_update == True:

                self.update_file = '-'.join(line) + '.tar.bz2'
                self.oe.write_setting('system', 'update_file',
                        self.update_file)
                self.oe.write_setting('system', 'update_url',
                        self.update_url)

                self.oe.dbg_log('system::check_updates',
                                'update available ' + self.update_file,
                                1)

                if not self.config['update']['settings']['AutoUpdate'
                        ]['value'] == 'auto':
                    xbmcDialog = xbmcgui.Dialog()
                    answer = xbmcDialog.yesno('OpenELEC Update',
                            self.oe._(32188) + ':  ' + current_version,
                            self.oe._(32187) + ':  ' + latest_version,
                            self.oe._(32180))
                    if answer == 1:
                        self.do_autoupdate()
                else:

                    self.do_autoupdate(None, True)

            self.oe.dbg_log('system::check_updates', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::check_updates', 'ERROR: ('
                            + repr(e) + ')')

    def do_autoupdate(self, listItem=None, silent=False):
        try:

            self.oe.dbg_log('system::do_autoupdate', 'enter_function',
                            0)

            if hasattr(self, 'update_url') and hasattr(self,
                    'update_file'):

                if not os.path.exists(self.update_folder):
                    os.makedirs(self.update_folder)

                downloaded = self.oe.download_file(self.update_url + '/'
                         + self.update_file, self.temp_folder + '/'
                        + self.update_file, silent)

                if not downloaded is None:

                    if self.config['update']['settings']['UpdateNotify'
                            ]['value'] == '1':
                        xbmc.executebuiltin('Notification('
                                + self.oe._(32363) + ', '
                                + self.oe._(32366) + ')')

                    if not os.path.exists(self.temp_folder
                            + 'oe_update/'):
                        os.makedirs(self.temp_folder + 'oe_update/')

                    extract_files = ['target/SYSTEM', 'target/KERNEL']
                    if self.oe.extract_file(downloaded, extract_files,
                            self.temp_folder + 'oe_update/', silent) \
                        == 1:

                        if self.config['update']['settings'
                                ]['UpdateNotify']['value'] == '1':
                            xbmc.executebuiltin('Notification('
                                    + self.oe._(32363) + ', '
                                    + self.oe._(32367) + ')')

                        self.oe.write_setting('system', 'update_file',
                                '')
                        self.oe.write_setting('system', 'update_url', ''
                                )

                        os.remove(downloaded)

                        for update_file in glob.glob(self.temp_folder
                                + 'oe_update/*'):
                            os.rename(update_file, self.update_folder
                                    + update_file.rsplit('/')[-1])

                        if silent == False:
                            self.oe.winOeMain.close()
                            time.sleep(1)
                            xbmc.executebuiltin('Reboot')

            self.oe.dbg_log('system::do_autoupdate', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::do_autoupdate', 'ERROR: ('
                            + repr(e) + ')')

    def hide_update_nofification(self):
        try:

            self.oe.dbg_log('system::hide_update_nofification',
                            'enter_function', 0)

            if hasattr(self, 'home_window'):

                if hasattr(self, 'nofify_image'):
                    self.home_window.removeControl(self.nofify_image)
                    del self.nofify_image

                if hasattr(self, 'notify_label'):
                    self.home_window.removeControl(self.notify_label)
                    del self.notify_label

                del self.home_window

            self.oe.dbg_log('system::hide_update_nofification',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::show_update_nofification',
                            'ERROR: (' + repr(e) + ')')

    def show_update_nofification(self):
        try:

            self.oe.dbg_log('system::show_update_nofification',
                            'enter_function', 0)

            self.update_available = True

            if not hasattr(self, 'home_window'):
                self.home_window = xbmcgui.Window(10000)

                if not hasattr(self, 'notify_image'):
                    self.nofify_image = xbmcgui.ControlImage(
                        500,
                        1,
                        270,
                        135,
                        aspectRatio=0,
                        filename=self.oe.__cwd__
                            + '/resources/skins/Default/media/OpenELEC_Logo.png'
                            ,
                        )

                    self.home_window.addControl(self.nofify_image)

                if not hasattr(self, 'notify_label'):
                    self.notify_label = xbmcgui.ControlLabel(
                        590,
                        90,
                        400,
                        75,
                        self.oe._(32179),
                        font='font12',
                        )

                    self.home_window.addControl(self.notify_label)

            self.oe.dbg_log('system::show_update_nofification',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::show_update_nofification',
                            'ERROR: (' + repr(e) + ')')

    def set_hw_clock(self):
        try:

            self.oe.dbg_log('system::set_hw_clock', 'enter_function', 0)

            os.system('/sbin/hwclock --systohc --utc')

            self.oe.dbg_log('system::set_hw_clock', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::set_hw_clock', 'ERROR: ('
                            + repr(e) + ')', 4)

    def set_cpupower(self):
        try:

            self.oe.dbg_log('system::set_cpupower', 'enter_function', 0)

            os.system('cpupower frequency-set -g ondemand')

            self.oe.dbg_log('system::set_cpupower', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::set_cpupower', 'ERROR: ('
                            + repr(e) + ')', 4)

    def reset_xbmc(self, listItem=None):
        try:

            self.oe.dbg_log('system::reset_xbmc', 'enter_function', 0)

            if self.ask_sure_reset('XBMC') == 1:

                self.oe.set_busy(1)

                reset_file = open(self.xbmc_reset_file, 'w')
                reset_file.write('reset')
                reset_file.close()

                time.sleep(1)
                xbmc.executebuiltin('Reboot')

            self.oe.set_busy(0)

            self.oe.dbg_log('system::reset_xbmc', 'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::reset_xbmc', 'ERROR: (' + repr(e)
                            + ')', 4)

    def reset_oe(self, listItem=None):
        try:

            self.oe.dbg_log('system::reset_oe', 'enter_function', 0)

            if self.ask_sure_reset('OpenELEC') == 1:

                self.oe.set_busy(1)

                reset_file = open(self.oe_reset_file, 'w')
                reset_file.write('reset')
                reset_file.close()

                time.sleep(1)
                xbmc.executebuiltin('Reboot')

                self.oe.set_busy(0)

            self.oe.dbg_log('system::reset_oe', 'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::reset_oe', 'ERROR: (' + repr(e)
                            + ')', 4)

    def ask_sure_reset(self, part):
        try:

            self.oe.dbg_log('system::ask_sure_reset', 'enter_function',
                            0)

            xbmcDialog = xbmcgui.Dialog()
            answer = xbmcDialog.yesno(part + ' reset',
                    self.oe._(32326), self.oe._(32328))

            if answer == 1:

                extract_dlg = xbmcgui.DialogProgress()
                extract_dlg.create('OpenELEC %s' % self.oe._(32323), ' '
                                   , ' ', ' ')
                extract_dlg.update(0)

                counter = 30
                while counter >= 0 and not extract_dlg.iscanceled():
                    extract_dlg.update(counter * 30, self.oe._(32329)
                            % counter)
                    time.sleep(1)
                    counter = counter - 1

                if not extract_dlg.iscanceled():
                    return 1
                else:
                    return 0

            self.oe.dbg_log('system::reset_oeask_sure_reset',
                            'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::ask_sure_reset', 'ERROR: ('
                            + repr(e) + ')', 4)

    def upload_logfiles(self, listItem=None):
        try:

            self.oe.dbg_log('system::upload_logfiles', 'enter_function'
                            , 0)

            distri = self.oe.load_file('/etc/distribution')
            arch = self.oe.load_file('/etc/arch')
            version = self.oe.load_file('/etc/version')

            info_file = open('/tmp/sysinfo', 'w')
            info_file.write('SYSTEM\n')
            info_file.write(distri + '\n')
            info_file.write(arch + '\n')
            info_file.write(version + '\n')
            info_file.close()

            xbmcKeyboard = xbmc.Keyboard('', self.oe._(32360))
            xbmcKeyboard.doModal()
            if xbmcKeyboard.isConfirmed():
                if xbmcKeyboard.getText() != '':
                    if '@' in xbmcKeyboard.getText():

                        xbmc.executebuiltin('ActivateWindow(busydialog)'
                                )

                        zipName = '/tmp/' + xbmcKeyboard.getText() \
                            + '.zip'

                        zip = zipfile.ZipFile(zipName, 'w')

                        zip.write('/tmp/sysinfo', 'sysinfo')

                        if os.path.exists('/var/log/messages'):
                            zip.write('/var/log/messages', 'messages')
                        if os.path.exists('/var/log/messages.0'):
                            zip.write('/var/log/messages.0',
                                    'messages.0')
                        if os.path.exists('/storage/.xbmc/temp/xbmc.log'
                                ):
                            zip.write('/storage/.xbmc/temp/xbmc.log',
                                    'xbmc.log')
                        if os.path.exists('/storage/.xbmc/temp/xbmc.old.log'
                                ):
                            zip.write('/storage/.xbmc/temp/xbmc.old.log'
                                    , 'xbmc.old.log')

                        os.system('lspci -v >/tmp/lspci')
                        if os.path.exists('/tmp/lspci'):
                            zip.write('/tmp/lspci', 'lspci')

                        os.system('lsusb -v >/tmp/lsusb')
                        if os.path.exists('/tmp/lsusb'):
                            zip.write('/tmp/lsusb', 'lsusb')

                        os.system('lsmod >/tmp/lsmod')
                        if os.path.exists('/tmp/lsmod'):
                            zip.write('/tmp/lsmod', 'lsmod')

                        for log in glob.glob('/var/log/*.log'):
                            zip.write(log, os.path.basename(log))

                        zip.close()

                        self.post_multipart('paste.fiebach.de',
                                '/upload.php', [('', '')], [('file',
                                open(zipName, 'rb'))])

                        os.remove(zipName)
                        os.remove('/tmp/lspci')
                        os.remove('/tmp/lsusb')
                        os.remove('/tmp/lsmod')
                        os.remove('/tmp/sysinfo')
                    else:

                        dialog = xbmcgui.Dialog()
                        dialog.ok(self.oe._(32214), self.oe._(32215))

            xbmc.executebuiltin('Dialog.Close(busydialog)')

            self.oe.dbg_log('system::upload_logfiles', 'exit_function',
                            0)
        except Exception, e:

            xbmc.executebuiltin('Dialog.Close(busydialog)')
            self.oe.dbg_log('system::upload_logfiles', 'ERROR: ('
                            + repr(e) + ')')

    def do_backup(self, listItem=None):
        try:

            self.oe.dbg_log('system::do_backup', 'enter_function', 0)

            self.total_backup_size = 1
            self.done_backup_size = 1

            for directory in self.backup_dirs:
                self.get_folder_size(directory)

            xbmcDialog = xbmcgui.Dialog()
            returnValue = xbmcDialog.browse(
                3,
                self.oe._(32376),
                'files',
                '',
                False,
                False,
                '',
                )

            self.backup_dlg = xbmcgui.DialogProgress()
            self.backup_dlg.create('OpenELEC', self.oe._(32375), ' ',
                                   ' ')

            zip = zipfile.ZipFile(returnValue + self.backup_file, 'w')
            for directory in self.backup_dirs:
                self.zip_add_folder(zip, directory)

            zip.close()
            self.backup_dlg.close()
            del self.backup_dlg

            self.oe.dbg_log('system::do_backup', 'exit_function', 0)
        except Exception, e:

            self.backup_dlg.close()
            self.oe.dbg_log('system::do_backup', 'ERROR: (' + repr(e)
                            + ')')

    def do_restore(self, listItem=None):
        try:

            self.oe.dbg_log('system::do_restore', 'enter_function', 0)

            xbmcDialog = xbmcgui.Dialog()
            restore_file = xbmcDialog.browse(
                1,
                self.oe._(32377),
                'files',
                self.backup_file,
                False,
                False,
                '/',
                )

            if restore_file != '':
                if not os.path.exists(self.restore_path):
                    os.makedirs(self.restore_path)

                folder_stat = os.statvfs(self.restore_path)
                file_size = os.path.getsize(restore_file)
                free_space = folder_stat.f_bsize * folder_stat.f_bavail

                if free_space > file_size * 2:
                    if os.path.exists(self.restore_path
                            + self.backup_file):
                        os.remove(self.restore_path + self.backup_file)

                    self.oe.copy_file(restore_file, self.restore_path
                            + self.backup_file)

            self.oe.dbg_log('system::do_restore', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::do_restore', 'ERROR: (' + repr(e)
                            + ')')

    def zip_add_folder(self, zip, folder):
        try:
            for item in os.listdir(folder):

                if item == self.backup_file:
                    continue

                if self.backup_dlg.iscanceled():
                    return 0

                itempath = os.path.join(folder, item)
                if os.path.isfile(itempath):
                    self.done_backup_size += os.path.getsize(itempath)
                    zip.write(itempath)
                    if hasattr(self, 'backup_dlg'):
                        progress = round(1.0 * self.done_backup_size
                                / self.total_backup_size * 100)
                        self.backup_dlg.update(int(progress), folder,
                                item)
                elif os.path.isdir(itempath):
                    self.zip_add_folder(zip, itempath)
        except Exception, e:

            self.backup_dlg.close()
            self.oe.dbg_log('system::zip_add_folder', 'ERROR: ('
                            + repr(e) + ')')

    def get_folder_size(self, folder):

        for item in os.listdir(folder):
            itempath = os.path.join(folder, item)
            if os.path.isfile(itempath):
                self.total_backup_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                self.get_folder_size(itempath)

    def post_multipart(
        self,
        host,
        selector,
        fields,
        files,
        ):
        try:

            (content_type, body) = \
                self._encode_multipart_formdata(fields, files)
            h = httplib.HTTPConnection(host)
            headers = {'User-Agent': 'python_multipart_caller',
                       'Content-Type': content_type}
            h.request('POST', selector, body, headers)
            res = h.getresponse()
            return res.read()
        except Exception, e:

            self.oe.dbg_log('system::post_multipart', 'ERROR: ('
                            + repr(e) + ')')

    def _encode_multipart_formdata(self, fields, files):
        try:

            BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
            CRLF = '\r\n'
            L = []
            for (key, value) in fields:
                L.append('--' + BOUNDARY)
                L.append('Content-Disposition: form-data; name="%s"'
                         % key)
                L.append('')
                L.append(value)
            for (key, fd) in files:
                file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
                filename = fd.name.split('/')[-1]
                contenttype = mimetypes.guess_type(filename)[0] \
                    or 'application/octet-stream'
                L.append('--%s' % BOUNDARY)
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"'
                          % (key, filename))
                L.append('Content-Type: %s' % contenttype)
                fd.seek(0)
                L.append('\r\n' + fd.read())
            L.append('--' + BOUNDARY + '--')
            L.append('')
            body = CRLF.join(L)
            content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
            return (content_type, body)
        except Exception, e:

            self.oe.dbg_log('system::_encode_multipart_formdata',
                            'ERROR: (' + repr(e) + ')')

    def do_wizard(self):
        try:

            self.oe.dbg_log('system::do_wizard', 'enter_function', 0)

            self.oe.winOeMain.set_wizard_title(self.oe._(32003))
            self.oe.winOeMain.set_wizard_text(self.oe._(32304))
            self.oe.winOeMain.set_wizard_button_title(self.oe._(32308))
            self.oe.winOeMain.set_wizard_button_1(self.config['ident'
                    ]['settings']['hostname']['value'], self,
                    'wizard_set_hostname')

            self.oe.dbg_log('system::do_wizard', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::do_wizard', 'ERROR: (' + repr(e)
                            + ')')

    def wizard_set_hostname(self):
        try:

            self.oe.dbg_log('system::wizard_set_hostname',
                            'enter_function', 0)

            currentHostname = self.config['ident']['settings'
                    ]['hostname']['value']

            xbmcKeyboard = xbmc.Keyboard(currentHostname)
            result_is_valid = False
            while not result_is_valid:
                xbmcKeyboard.doModal()

                if xbmcKeyboard.isConfirmed():
                    result_is_valid = True
                    validate_string = self.config['ident']['settings'
                            ]['hostname']['validate']
                    if validate_string != '':
                        if not re.search(validate_string,
                                xbmcKeyboard.getText()):
                            result_is_valid = False
                else:
                    result_is_valid = True

            if xbmcKeyboard.isConfirmed():
                self.config['ident']['settings']['hostname']['value'] = \
                    xbmcKeyboard.getText()
                self.set_hostname()
                self.oe.winOeMain.getControl(1401).setLabel(self.config['ident'
                        ]['settings']['hostname']['value'])
                self.oe.write_setting('system', 'hostname',
                        self.config['ident']['settings']['hostname'
                        ]['value'])

            self.oe.dbg_log('system::wizard_set_hostname',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::wizard_set_hostname', 'ERROR: ('
                            + repr(e) + ')')


class updateThread(threading.Thread):

    def __init__(self, oeMain):
        try:

            oeMain.dbg_log('system::updateThread::__init__',
                           'enter_function', 0)

            self.oe = oeMain
            self.last_check = time.time()
            self.stopped = False

            threading.Thread.__init__(self)

            self.oe.dbg_log('system::updateThread', 'Started', 1)

            self.oe.dbg_log('system::updateThread::__init__',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::updateThread::__init__', 'ERROR: ('
                             + repr(e) + ')')

    def stop(self):

        self.stopped = True

    def run(self):
        try:

            self.oe.dbg_log('system::updateThread::run',
                            'enter_function', 0)

            self.oe.dictModules['system'].check_updates()

            while not self.stopped and not xbmc.abortRequested:

                current_time = time.time()
                if current_time > self.last_check + 60:
                    if not xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying():
                        self.oe.dictModules['system'].check_updates()
                        self.last_check = current_time
                    else:
                        self.last_check = current_time
                        self.oe.dbg_log('system::updateThread',
                                'XBMC is Playing !', 1)

                time.sleep(0.2)

            self.oe.dbg_log('system::updateThread', 'Stopped', 1)

            self.oe.dbg_log('system::updateThread::run', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.dbg_log('system::updateThread::run', 'ERROR: ('
                            + repr(e) + ')')
