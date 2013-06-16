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
import tarfile
import stat
import mimetypes
import httplib
import oeWindows
import json

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
                        'not_supported': ['RPi.arm'],  
                        }, 'KeyboardType': {
                        'name': 32330,
                        'value': 'pc105',
                        'action': 'set_keyboard_layout',
                        'typ': 'multivalue',
                        'values': [],
                        'InfoText': 713,
                        'not_supported': ['RPi.arm'],                        
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
                    'order': 8,
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

            self.kernel_cmd = '/proc/cmdline'
            
            self.lcd_dir = '/usr/lib/lcdproc/'
            self.envFile = '/storage/oe_environment'
            self.keyboard_layouts = False
            self.rpi_keyboard_layouts = False
            
            self.update_url_release = 'http://releases.openelec.tv'            
            self.update_url_devel = 'http://snapshots.openelec.tv'
            self.update_url_v2 = 'http://update.openelec.tv/updates.php'
            self.download_url_v2 = 'http://%s.openelec.tv/%s'
            
            self.temp_folder = os.environ['HOME'] + '/.xbmc/temp/'
            self.update_folder = '/storage/.update/'
            self.last_update_check = 0
            self.xbmc_reset_file = '/storage/.cache/reset_xbmc'
            self.oe_reset_file = '/storage/.cache/reset_oe'

            self.keyboard_info = '/usr/share/X11/xkb/rules/base.xml'
            self.udev_keyboard_file = '/storage/.cache/xkb/layout'

            self.rpi_keyboard_info = '/usr/lib/keymaps'
            
            self.backup_dirs = ['/storage/.xbmc', '/storage/.config',
                                '/storage/.cache']
                                
            self.backup_folder = '/storage/backup/'
            self.restore_path = '/storage/.restore/'

            self.distri = self.oe.load_file('/etc/distribution')
            self.arch = self.oe.load_file('/etc/arch')
            self.version = self.oe.load_file('/etc/version')
            
            self.cpu_lm_flag = self.oe.execute('cat /proc/cpuinfo | grep -q "flags.* lm " && echo \'1\' || echo \'0\'')
            self.au = None
            
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
            self.init_bluetooth()
            self.set_auto_update()

            del self.is_service
            
            self.oe.dbg_log('system::start_service', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::start_service', 'ERROR: ('
                            + repr(e) + ')')

    def stop_service(self):
        try:

            self.oe.dbg_log('system::stop_service', 'enter_function', 0)

            if 'bluetooth' in self.oe.dictModules:
                self.oe.dictModules['bluetooth'].stop_bluetoothd()
            
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

                if not arrTypes == None: 
                    self.keyboard_layouts = True
                else:
                    self.rpi_keyboard_layouts = True
                    
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
            value = self.oe.read_setting('system', 'enable_hdd_standby')
            if not value is None:
                self.config['power']['settings']['enable_hdd_standby']['value'
                        ] = value

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

            # AutoUpdate = manual by environment var.
            if 'UPDATE_SUPPORT' in os.environ:
                if os.environ['UPDATE_SUPPORT'] == 'false':
                    self.config['update']['settings']['AutoUpdate']['value'
                            ] = 'manual'
                    
                    self.config['update']['settings']['AutoUpdate']['not_supported'
                            ] = [self.arch]

                    self.config['update']['settings']['CheckUpdate']['not_supported'
                            ] = [self.arch]
                    
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
                      
                    if 'not_supported' in self.config[category]['settings'][setting]:
                        if self.arch \
                            in self.config[category]['settings'][setting]['not_supported']:
                           continue
                        
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

                if 'bluetooth' in self.oe.dictModules:
                    self.oe.dictModules['bluetooth'].start_bluetoothd()

            else:

                if 'bluetooth' in self.oe.dictModules:
                    self.oe.dictModules['bluetooth'].stop_bluetoothd()

            self.oe.set_busy(0)

            self.oe.dbg_log('system::init_bluetooth', 'exit_function',
                            0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::init_bluetooth', 'ERROR: ('
                            + repr(e) + ')', 4)


    def set_keyboard_layout(self, listItem=None):
        try:

            self.oe.dbg_log('system::set_keyboard_layout',
                            'enter_function', 0)

            self.oe.set_busy(1)

            if not listItem == None:
                self.set_value(listItem)
                  
            if self.keyboard_layouts == True:

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

            elif self.rpi_keyboard_layouts == True:
                
                self.oe.dbg_log('system::set_keyboard_layout',
                                str(self.config['keyboard']['settings'
                                ]['KeyboardLayout1']['value']) , 1)                

                parameter = self.config['keyboard'
                              ]['settings']['KeyboardLayout1']['value']

                command = 'loadkmap < `ls -1 %s/*/%s.bmap`' % (self.rpi_keyboard_info, parameter)
                
                self.oe.dbg_log('system::set_keyboard_layout', command, 1)     
                result = self.oe.execute(command)
                
                #result = self.oe.execute('find /usr/lib/keymaps/ | grep %s.bmap`' % parameter)
                #os.system('loadkmap < %s' % result)

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

                hostname = open('/storage/.cache/hostname', 'w')
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
                            ]['hdd_standby']['value']) #* 12

                #find system hdd
                cmd_file = open(self.kernel_cmd, 'r')
                cmd_args = cmd_file.read()
                for param in cmd_args.split(' '):
                    if param.startswith('boot='):
                        sys_hdd = param.replace('boot=', '').split('=')[-1]                       
                        
                cmd_file.close()  
                
                blkid = self.oe.execute('blkid')
                for volume in blkid.splitlines():
                
                    if ('LABEL="%s"' % sys_hdd) in volume or \
                       ('UUID="%s"' % sys_hdd) in volume:
                         
                        sys_hdd_dev = volume.split(':')[0].replace('/dev/', '')                     
                
                parameters = []
                for device in glob.glob('/dev/sd?'):

                    device = device.replace('/dev/', '')
                    
                    if not device in sys_hdd_dev:
                      
                        parameters.append('-a %s' % device)
                        
                    else:
                        self.oe.dbg_log('system::set_hdd_standby', 
                                        ('Skip System Disk:%s' % device), 1)
                                        

                if len(parameters) > 0:   
                    os.system('hd-idle -i %d %s' % (value*60, ' '.join(parameters)))
                    self.oe.dbg_log('system::set_hdd_standby', 
                                    ('hd-idle -i %d %s' % (value*60, ' '.join(parameters))), 1)
                                        
            else:

                self.oe.dbg_log('system::set_hdd_standby', '0 (off)'
                                , 1)

                os.system('killall hd-idle')

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

            self.check_updates_v2(True)

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
            else:
                self.update_thread.wait_evt.set()

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

            if os.path.exists(self.keyboard_info):

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

            elif os.path.exists(self.rpi_keyboard_info):
              
                #for root, subFolders, files in os.walk(self.rpi_keyboard_info):
                #    for file in files:
                #        if file.endswith('.bmap'):
                #            xbmc.log(file)
                #            arrLayouts.append(file.split('.')[0])
                
                for layout in glob.glob(self.rpi_keyboard_info + '/*/*.bmap'):
                    if os.path.isfile(layout):
                        xbmc.log(layout)
                        arrLayouts.append(layout.split('/')[-1].split('.')[0])
                    
                arrLayouts.sort()
                arrTypes = None
            else:
              
                self.oe.dbg_log('system::get_keyboard_layouts',
                                'exit_function (no keyboard layouts found)',
                                0)
                return (None, None)

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

    def check_updates_v2(self, force=False):
        try:

            self.oe.dbg_log('system::check_updates_v2', 'enter_function', 0)
         
            if hasattr(self, "update_in_progress"):
                self.oe.dbg_log('system::check_updates_v2', 'Update in progress (exit)', 0)
                return
              
            sysid = os.environ['SYSTEMID']

            update_json = self.oe.load_url('%s?i=%s&d=%s&pa=%s&v=%s&l=%s' % ( \
              self.update_url_v2, sysid, self.distri, self.arch, self.version, self.cpu_lm_flag ))
            
            if update_json != "":
                update_json = json.loads(update_json)
                
                self.last_update_check = time.time()
                silent = True
                answer = 0
                
                if 'update' in update_json['data'] and 'folder' in update_json['data']:
                    self.update_file = self.download_url_v2 % (update_json['data']['folder'],
                                                               update_json['data']['update'])

                    if self.config['update']['settings']['UpdateNotify'
                            ]['value'] == '1':
                        xbmc.executebuiltin('Notification('
                                + self.oe._(32363) + ', '
                                + self.oe._(32364) + ')')
   
                    if (self.config['update']['settings']['AutoUpdate']['value'
                        ] == 'manual' or force == True):
                        silent = False
                      
                        if self.config['update']['settings']['UpdateNotify'
                                ]['value'] != '1' and force != True:
                          
                            xbmcDialog = xbmcgui.Dialog()
                            answer = xbmcDialog.yesno('OpenELEC Update',
                                    self.oe._(32188) + ':  ' + self.version,
                                    self.oe._(32187) + ':  ' + update_json['data']['update'].split('-')[-1].replace('.tar.bz2', ''),
                                    self.oe._(32180))
                            
                            xbmcDialog = None
                            del xbmcDialog
                        
                        if answer == 1:
                            self.update_in_progress = True
                            self.do_autoupdate()
                            
                    else:

                        self.update_in_progress = True
                        self.do_autoupdate(None, True)
                    
            self.oe.dbg_log('system::check_updates_v2', 'exit_function', 0)
            
        except Exception, e:

            self.oe.dbg_log('system::check_updates_v2', 'ERROR: ('
                            + repr(e) + ')')
            
    def do_autoupdate(self, listItem=None, silent=False):
        try:

            self.oe.dbg_log('system::do_autoupdate', 'enter_function',
                            0)

            if hasattr(self, 'update_file'):

                if not os.path.exists(self.update_folder):
                    os.makedirs(self.update_folder)

                downloaded = self.oe.download_file(self.update_file, 
                        self.temp_folder + self.update_file.split('/')[-1], silent)

                if not downloaded is None:

                    self.update_file = self.update_file.split('/')[-1]
                    
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

    def set_hw_clock(self):
        try:

            self.oe.dbg_log('system::set_hw_clock', 'enter_function', 0)

            os.system('/sbin/hwclock --systohc --utc')

            self.oe.dbg_log('system::set_hw_clock', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::set_hw_clock', 'ERROR: ('
                            + repr(e) + ')', 4)

    def reset_xbmc(self, listItem=None):
        try:

            self.oe.dbg_log('system::reset_xbmc', 'enter_function', 0)

            if self.ask_sure_reset('XBMC') == 1:

                self.oe.set_busy(1)

                reset_file = open(self.xbmc_reset_file, 'w')
                reset_file.write('reset')
                reset_file.close()

                self.oe.winOeMain.close()
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

                self.oe.winOeMain.close()
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

                if self.oe.reboot_counter(30, self.oe._(32323)) == 1:
                    return 1
                else:
                    return 0
                  
            self.oe.dbg_log('system::reset_oeask_sure_reset',
                            'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('system::ask_sure_reset', 'ERROR: ('
                            + repr(e) + ')', 4)

                  
    def do_backup(self, listItem=None):
        try:

            self.oe.dbg_log('system::do_backup', 'enter_function', 0)

            self.total_backup_size = 1
            self.done_backup_size = 1

            try:
              
              self.oe.set_busy(1)
              
              for directory in self.backup_dirs:
                  self.get_folder_size(directory)

              self.oe.set_busy(0)
            except:
              self.oe.set_busy(0)
              
            xbmcDialog = xbmcgui.Dialog()

            self.backup_dlg = xbmcgui.DialogProgress()
            self.backup_dlg.create('OpenELEC', self.oe._(32375), ' ', ' ')
            
            if not os.path.exists(self.backup_folder):
                os.makedirs(self.backup_folder)
            
            self.backup_file = self.oe.timestamp() + '.tar'

            tar = tarfile.open(self.backup_folder + self.backup_file, 'w')
            for directory in self.backup_dirs:
                self.tar_add_folder(tar, directory)

            tar.close()
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

            copy_success = 0
            backup_files = []
            for backup_file in sorted(glob.glob(self.backup_folder + '*.tar'), key=os.path.basename):
                backup_files.append(backup_file.split("/")[-1] + ":")
                
            select_window = oeWindows.selectWindow('selectWindow.xml',
                    self.oe.__cwd__, 'Default', oeMain=self.oe)

            select_window.availValues = ",".join(backup_files)
            
            select_window.doModal()
            restore_file = select_window.result
            
            del select_window

            if restore_file != '':
                if not os.path.exists(self.restore_path):
                    os.makedirs(self.restore_path)

                else:
                    os.system('rm -rf %s' % self.restore_path)
                    os.makedirs(self.restore_path)
                    
                folder_stat = os.statvfs(self.restore_path)
                file_size = os.path.getsize(self.backup_folder + restore_file)
                free_space = folder_stat.f_bsize * folder_stat.f_bavail

                if free_space > file_size * 2:
                    if os.path.exists(self.restore_path
                            + restore_file):
                        os.remove(self.restore_path + self.restore_file)

                    if self.oe.copy_file(self.backup_folder + restore_file, 
                            self.restore_path + restore_file) != None:

                        copy_success = 1
                    else:
                      
                        os.system('rm -rf %s' % self.restore_path)
                        
                else:
                    
                    txt = self.oe.split_dialog_text(self.oe._(32379))  
                    
                    xbmcDialog = xbmcgui.Dialog()
                    answer = xbmcDialog.ok('Restore',
                            txt[0], txt[1], txt[2])
                
                if copy_success == 1:
                  
                    txt = self.oe.split_dialog_text(self.oe._(32380))  

                    xbmcDialog = xbmcgui.Dialog()
                    answer = xbmcDialog.yesno('Restore',
                            txt[0], txt[1], txt[2])
                    
                    if answer == 1:
                        
                        if self.oe.reboot_counter(10, self.oe._(32371)) == 1:
                            self.oe.winOeMain.close()
                            time.sleep(1)
                            xbmc.executebuiltin('Reboot')
                        
                    else:
                        self.oe.dbg_log('system::do_restore',
                                        'User Abort!', 0)
                        os.system('rm -rf %s' % self.restore_path)
                      
            self.oe.dbg_log('system::do_restore', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::do_restore', 'ERROR: (' + repr(e)
                            + ')')

            
    def tar_add_folder(self, tar, folder):
        try:
            for item in os.listdir(folder):

                if item == self.backup_file:
                    continue

                if self.backup_dlg.iscanceled():
                    try:
                        os.remove(self.backup_folder + self.backup_file)
                    except:
                        pass
                    return 0

                itempath = os.path.join(folder, item)
                if os.path.isfile(itempath):
                    self.done_backup_size += os.path.getsize(itempath)
                    tar.add(itempath)
                    if hasattr(self, 'backup_dlg'):
                        progress = round(1.0 * self.done_backup_size
                                / self.total_backup_size * 100)
                        self.backup_dlg.update(int(progress), folder,
                                item)
                elif os.path.isdir(itempath):
                    self.tar_add_folder(tar, itempath)
        except Exception, e:

            self.backup_dlg.close()
            self.oe.dbg_log('system::tar_add_folder', 'ERROR: ('
                            + repr(e) + ')')


    def get_folder_size(self, folder):

        for item in os.listdir(folder):
            itempath = os.path.join(folder, item)
            if os.path.isfile(itempath):
                self.total_backup_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                self.get_folder_size(itempath)


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
            self.stopped = False

            self.wait_evt = threading.Event()

            threading.Thread.__init__(self)

            self.oe.dbg_log('system::updateThread', 'Started', 1)

            self.oe.dbg_log('system::updateThread::__init__',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::updateThread::__init__', 'ERROR: ('
                             + repr(e) + ')')

    def stop(self):
        try:
          
            self.oe.dbg_log('system::updateThread::stop()',
                            'enter_function', 0)

            self.stopped = True
            self.wait_evt.set()
         
            self.oe.dbg_log('system::updateThread::stop()',
                            'exit_function', 0)    
            
            del self.oe
         
        except Exception, e:

            self.oe.dbg_log('system::updateThread::stop()', 'ERROR: ('
                             + repr(e) + ')')        
    def run(self):
        try:

            self.oe.dbg_log('system::updateThread::run',
                            'enter_function', 0)
     
            while self.stopped == False:

                if not xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying():
                    self.oe.dictModules['system'].check_updates_v2()

                self.wait_evt.wait(21600)
                self.wait_evt.clear()

            self.oe.dbg_log('system::updateThread', 'Stopped', 1)

            self.oe.dbg_log('system::updateThread::run', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.dbg_log('system::updateThread::run', 'ERROR: ('
                            + repr(e) + ')')
