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
import xbmc
import ConfigParser
from StringIO import StringIO
import subprocess

class services:

    menu = {'4': {
        'name': 32001,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 703,
        }}

    def __init__(self, oeMain):
        try:

            oeMain.dbg_log('services::__init__', 'enter_function', 0)

            self.struct = {
                'samba': {
                    'order': 1,
                    'name': 32200,
                    'not_supported': [],
                    'settings': {
                        'samba_autostart': {
                            'order': 1,
                            'name': 32204,
                            'value': None,
                            'action': 'initialize_samba',
                            'type': 'bool',
                            'InfoText': 738,
                            },
                        'samba_secure': {
                            'order': 2,
                            'name': 32202,
                            'value': None,
                            'action': 'initialize_samba',
                            'type': 'bool',
                            'parent': {'entry': 'samba_autostart',
                                    'value': ['1']},
                            'InfoText': 739,
                            },
                        'samba_username': {
                            'order': 3,
                            'name': 32106,
                            'value': None,
                            'action': 'initialize_samba',
                            'type': 'text',
                            'parent': {'entry': 'samba_secure',
                                    'value': ['1']},
                            'InfoText': 740,
                            },
                        'samba_password': {
                            'order': 4,
                            'name': 32107,
                            'value': None,
                            'action': 'initialize_samba',
                            'type': 'text',
                            'parent': {'entry': 'samba_secure',
                                    'value': ['1']},
                            'InfoText': 741,
                            },
                        },
                    },
                'ssh': {
                    'order': 2,
                    'name': 32201,
                    'not_supported': [],
                    'settings': {'ssh_autostart': {
                        'order': 1,
                        'name': 32205,
                        'value': None,
                        'action': 'initialize_ssh',
                        'type': 'bool',
                        'InfoText': 742,
                        }, 'ssh_secure': {
                        'order': 2,
                        'name': 32203,
                        'value': None,
                        'action': 'initialize_ssh',
                        'type': 'bool',
                        'parent': {'entry': 'ssh_autostart',
                                   'value': ['1']},
                        'InfoText': 743,
                        }},
                    },
                'avahi': {
                    'order': 3,
                    'name': 32207,
                    'not_supported': [],
                    'settings': {'avahi_autostart': {
                        'order': 1,
                        'name': 32206,
                        'value': None,
                        'action': 'initialize_avahi',
                        'type': 'bool',
                        'InfoText': 744,
                        }},
                    },
                'cron': {
                    'order': 3,
                    'name': 32319,
                    'not_supported': [],
                    'settings': {'cron_autostart': {
                        'order': 1,
                        'name': 32320,
                        'value': None,
                        'action': 'initialize_cron',
                        'type': 'bool',
                        'InfoText': 745,
                        }},
                    },
                'syslog': {
                    'order': 4,
                    'name': 32340,
                    'not_supported': [],
                    'settings': {'syslog_remote': {
                        'order': 1,
                        'name': 32341,
                        'value': None,
                        'action': 'initialize_syslog',
                        'type': 'bool',
                        'InfoText': 746,
                        }, 'syslog_server': {
                        'order': 2,
                        'name': 32342,
                        'value': None,
                        'action': 'initialize_syslog',
                        'type': 'ip',
                        'parent': {'entry': 'syslog_remote',
                                   'value': ['1']},
                        'InfoText': 747,
                        }},
                    },
                'bluez': {
                    'order': 5,
                    'name': 32331,
                    'not_supported': [],
                    'settings': {'disabled': {
                        'order': 1,
                        'name': 32344,
                        'value': None,
                        'action': 'init_bluetooth',
                        'type': 'bool',
                        'InfoText': 720,
                        }},
                    },                        
                }

            self.enabled = True
            
            self.oe = oeMain

            self.kernel_cmd = '/proc/cmdline'
            
            self.samba_nmbd = '/usr/bin/nmbd'
            self.samba_smbd = '/usr/bin/smbd'
            self.samba_init = '/etc/init.d/52_samba'

            self.ssh_daemon = '/usr/sbin/sshd'
            self.ssh_conf_dir =  self.oe.USER_CONFIG
            self.ssh_conf_file = 'sshd.conf'
            self.sshd_init = '/etc/init.d/51_sshd'

            self.avahi_daemon = '/usr/sbin/avahi-daemon'
            self.avahi_init = '/etc/init.d/53_avahi'

            self.cron_daemon = '/sbin/crond'
            self.crond_init = '/etc/init.d/09_crond'

            self.syslog_daemon = '/sbin/syslogd'
            self.syslog_init = '/etc/init.d/05_syslogd'

            self.bluetooth_daemon = '/usr/lib/bluetooth/bluetoothd'
            
            #self.oe = oeMain

      # self.load_values()

            oeMain.dbg_log('services::__init__', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::__init__', 'ERROR: (%s)'
                            % repr(e))

    def start_service(self):
        try:

            self.load_values()

            self.oe.dbg_log('services::start_service', 'enter_function'
                            , 0)

            self.initialize_samba(service=1)
            self.initialize_ssh(service=1)
            self.initialize_avahi(service=1)
            self.initialize_cron(service=1)

            self.init_bluetooth()
            
            self.oe.dbg_log('services::start_service', 'exit_function',
                            0)
        except Exception, e:

            self.oe.dbg_log('services::start_service', 'ERROR: (%s)'
                            % repr(e))

    def stop_service(self):
        try:

            self.oe.dbg_log('service::stop_service', 'enter_function', 0)

            #if 'bluetooth' in self.oe.dictModules:
            #    self.oe.dictModules['bluetooth'].stop_bluetoothd()

            self.oe.dbg_log('service::stop_service', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('service::stop_service', 'ERROR: ('
                            + repr(e) + ')')

    def do_init(self):
        try:

            self.oe.dbg_log('services::do_init', 'exit_function', 0)
            
            self.load_values()
            
            self.oe.dbg_log('services::do_init', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::do_init', 'ERROR: (%s)'
                            % repr(e))

    def set_value(self, listItem):
        try:

            self.oe.dbg_log('services::set_value', 'enter_function', 0)

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')

            self.oe.dbg_log('system::set_value', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::set_value', 'ERROR: (' + repr(e)
                            + ')')
            
    def load_menu(self, focusItem):

        try:

            self.oe.dbg_log('services::load_menu', 'enter_function', 0)

            self.oe.winOeMain.build_menu(self.struct)
            
            self.oe.dbg_log('services::load_menu', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::load_menu', 'ERROR: (%s)'
                            % repr(e))

    def load_values(self):
        try:

            self.oe.dbg_log('services::load_values', 'enter_function',
                            0)

            # read ssh settings from sshd_samba.conf
            if os.path.isfile(self.ssh_daemon):
                if self.oe.get_service_option('ssh', 'SSHD_START', 'true') == 'true':
                    self.struct['ssh']['settings']['ssh_autostart']['value'] = '1'
                else:
                    self.struct['ssh']['settings']['ssh_autostart']['value'] = '0'

                if self.oe.get_service_option('ssh', 'SSHD_DISABLE_PW_AUTH', 'false') == 'true':
                    self.struct['ssh']['settings']['ssh_secure']['value'] = '1'
                else:
                    self.struct['ssh']['settings']['ssh_secure']['value'] = '0'

                # hide ssh settings if Kernel Parameter isset
                cmd_file = open(self.kernel_cmd, 'r')
                cmd_args = cmd_file.read()
                if 'ssh' in cmd_args:
                    self.struct['ssh']['settings']['ssh_autostart'] \
                    ['hidden'] = 'true'

                cmd_file.close()
            else:
                self.struct['ssh']['hidden'] = 'true'
                
            # read samba settings from service_samba.conf
            if os.path.isfile(self.samba_nmbd) \
                and os.path.isfile(self.samba_smbd):
                if self.oe.get_service_option('samba', 'SAMBA_ENABLED', 'true') == 'true':
                    self.struct['samba']['settings']['samba_autostart']['value'] = '1'
                else:
                    self.struct['samba']['settings']['samba_autostart']['value'] = '0'

                if self.oe.get_service_option('samba', 'SAMBA_SECURE', 'true') == 'true':
                    self.struct['samba']['settings']['samba_secure']['value'] = '1'
                else:
                    self.struct['samba']['settings']['samba_secure']['value'] = '0'

                tmpVal = self.oe.get_service_option('samba', 'SAMBA_USERNAME', 'openelec')
                if not tmpVal is None:
                    self.struct['samba']['settings']['samba_username']['value'] = tmpVal
                
                tmpVal = self.oe.get_service_option('samba', 'SAMBA_PASSWORD', 'openelec')
                if not tmpVal is None:
                    self.struct['samba']['settings']['samba_password']['value'] = tmpVal

            else:
                self.struct['samba']['hidden'] = 'true'

            # read avahi settings from service_avahi.conf
            if os.path.isfile(self.avahi_daemon):
                if self.oe.get_service_option('avahi', 'AVAHI_ENABLED', 'true') == 'true':
                    self.struct['avahi']['settings']['avahi_autostart']['value'] = '1'
                else:
                    self.struct['avahi']['settings']['avahi_autostart']['value'] = '0'
            else:
                self.struct['avahi']['hidden'] = 'true'

            # read cron settings from service_cron.conf
            if os.path.isfile(self.cron_daemon):
                if self.oe.get_service_option('cron', 'CRON_ENABLED', 'true') == 'true':
                    self.struct['cron']['settings']['cron_autostart']['value'] = '1'
                else:
                    self.struct['cron']['settings']['cron_autostart']['value'] = '0'
            else:
                self.struct['cron']['hidden'] = 'true'
                
            # read syslog settings from service_syslog.conf    
            if os.path.isfile(self.syslog_daemon):
                if self.oe.get_service_option('syslog', 'SYSLOG_REMOTE', 'false') == 'true':
                    self.struct['syslog']['settings']['syslog_remote']['value'] = '1'
                else:
                    self.struct['syslog']['settings']['syslog_remote']['value'] = '0'
                    
                tmpVal = self.oe.get_service_option('syslog', 'SYSLOG_SERVER')
                if not tmpVal is None:
                    self.struct['samba']['settings']['syslog_server']['value'] = tmpVal
                    
            else:
                self.struct['syslog']['hidden'] = 'true'
            
            # read bluez settings from service_bluez.conf
            if os.path.isfile(self.bluetooth_daemon):              
                if self.oe.get_service_option('bluez', 'BLUEZ_ENABLED', 'true') == 'true':
                    self.struct['bluez']['settings']['disabled']['value'] = '0'
                else:
                    self.struct['bluez']['settings']['disabled']['value'] = '1'
            else:
                self.struct['bluez']['hidden'] = 'true'
                                        
            
            self.oe.dbg_log('services::load_values', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::load_values', 'ERROR: (%s)'
                            % repr(e))

    def initialize_samba(self, **kwargs):
        try:

            self.oe.dbg_log('services::initialize_samba',
                            'enter_function', 0)

            self.oe.set_busy(1)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
                
            if self.struct['samba']['settings']['samba_autostart'
                    ]['value'] != '1':
                
                self.oe.set_service_option('samba',
                                            'SAMBA_ENABLED',
                                            'false')
                
                if not 'service' in kwargs:
                    self.stop_samba()
                    self.oe.dbg_log('services::initialize_samba',
                                    'exit_function (samba disabled)', 0)
                
            else:

                self.oe.set_service_option('samba',
                                            'SAMBA_ENABLED',
                                            'true')
                
                if self.struct['samba']['settings']['samba_secure'
                        ]['value'] == '1' and self.struct['samba'
                        ]['settings']['samba_username']['value'] != '' \
                    and self.struct['samba']['settings'
                        ]['samba_password']['value'] != '':

                    self.oe.set_service_option('samba',
                                                'SAMBA_USERNAME',
                                                self.struct['samba'
                                                ]['settings']['samba_username'
                                                ]['value'])
                                            
                    self.oe.set_service_option('samba',
                                                'SAMBA_PASSWORD',
                                                self.struct['samba'
                                                ]['settings']['samba_password'
                                                ]['value'])
                                            
                    self.oe.set_service_option('samba',
                                               'SAMBA_SECURE',
                                               'true')

                else:

                    self.oe.set_service_option('samba',
                                               'SAMBA_SECURE',
                                               'false')
                 
                if not 'service' in kwargs: 
                    self.stop_samba()
                    subprocess.Popen('sh ' + self.samba_init, shell=True, close_fds=True)

            self.load_values()
            self.oe.set_busy(0)

            self.oe.dbg_log('services::initialize_samba',
                            'exit_function (samba enabled)', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_samba', 'ERROR: (%s)'
                            % repr(e), 4)

    def initialize_ssh(self, **kwargs):
        try:

            self.oe.dbg_log('services::initialize_ssh', 'enter_function'
                            , 0)

            self.oe.set_busy(1)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
                
            if self.struct['ssh']['settings']['ssh_autostart']['value'] \
                == '1':
                self.oe.set_service_option('ssh',
                                            'SSHD_START',
                                            'true')

            else:
                self.oe.set_service_option('ssh',
                                            'SSHD_START',
                                            'false')
                
            if self.struct['ssh']['settings']['ssh_secure']['value'] \
                == '1':
                self.oe.set_service_option('ssh',
                                            'SSHD_DISABLE_PW_AUTH',
                                            'true')
                
            else:
                self.oe.set_service_option('ssh',
                                            'SSHD_DISABLE_PW_AUTH',
                                            'false')

            #Initialize sshd
            if self.struct['ssh']['settings']['ssh_autostart']['value'] \
                == '0':
                if not 'service' in kwargs:
                    self.stop_ssh()

            else:
                if not 'service' in kwargs:
                    self.stop_ssh()
                    subprocess.Popen('sh ' + self.sshd_init, shell=True, close_fds=True)

            self.load_values()                          
            self.oe.set_busy(0)
            
            self.oe.dbg_log('services::initialize_ssh',
                            'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_ssh', 'ERROR: (%s)'
                            % repr(e), 4)

    def initialize_avahi(self, **kwargs):
        try:

            self.oe.dbg_log('services::initialize_avahi',
                            'enter_function', 0)

            self.oe.set_busy(1)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
                
            if self.struct['avahi']['settings']['avahi_autostart'
                    ]['value'] == '0':
                self.oe.set_service_option('avahi',
                                            'AVAHI_ENABLED',
                                            'false')   
                
                if not 'service' in kwargs:
                    self.stop_avahi()

            else:
                self.oe.set_service_option('avahi',
                                            'AVAHI_ENABLED',
                                            'true')   
            
                if not 'service' in kwargs:
                    self.stop_avahi()
                    subprocess.Popen('sh ' + self.avahi_init, shell=True, close_fds=True)

            self.load_values()
            self.oe.set_busy(0)
            
            self.oe.dbg_log('services::initialize_avahi',
                            'exit_function(avahi enabled)', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_avahi', 'ERROR: (%s)'
                            % repr(e), 4)

    def initialize_cron(self, **kwargs):
        try:

            self.oe.dbg_log('services::initialize_cron',
                            'enter_function', 0)

            self.oe.set_busy(1)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
                
            if self.struct['cron']['settings']['cron_autostart']['value'
                    ] == '0':                
                self.oe.set_service_option('cron',
                                            'CRON_ENABLED',
                                            'false')   
                
                if not 'service' in kwargs:
                    self.stop_cron()

            else:
                self.oe.set_service_option('cron',
                                            'CRON_ENABLED',
                                            'true')   
            
                if not 'service' in kwargs:
                    self.stop_cron()
                    subprocess.Popen('sh ' + self.crond_init, shell=True, close_fds=True)

            self.load_values()
            self.oe.set_busy(0)

            self.oe.dbg_log('services::initialize_cron',
                            'exit_function (cron enabled)', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_cron', 'ERROR: (%s)'
                            % repr(e), 4)

    def initialize_syslog(self, **kwargs):
        try:

            self.oe.dbg_log('services::initialize_syslog',
                            'enter_function', 0)

            self.oe.set_busy(1)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
                
            if self.struct['syslog']['settings'
                    ]['syslog_remote']['value'] == '1' \
                and self.struct['syslog']['settings']['syslog_server'
                    ]['value'] != None:

                if not os.path.exists(os.path.dirname(self.syslog_conf_file)):
                    os.makedirs(os.path.dirname(self.syslog_conf_file))

                self.oe.set_service_option('syslog',
                                            'SYSLOG_REMOTE',
                                            'true')
                
                self.oe.set_service_option('syslog',
                                            'SYSLOG_SERVER',
                                            self.struct['syslog'
                                            ]['settings']['syslog_server'
                                            ]['value'])
                
            else:

                self.oe.set_service_option('syslog',
                                           'SYSLOG_REMOTE',
                                           'false')

            self.stop_syslog()
            subprocess.Popen('sh ' + self.syslog_init, shell=True, close_fds=True)
                    
            self.load_values()
            self.oe.set_busy(0)

            self.oe.dbg_log('services::initialize_syslog',
                            'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_syslog', 'ERROR: (%s)'
                             % repr(e), 4)

    def init_bluetooth(self, **kwargs):
        try:

            self.oe.dbg_log('services::init_bluetooth', 'enter_function',
                            0)

            self.oe.set_busy(0)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
                
            if self.struct['bluez']['settings']['disabled']['value'] == '1':

                self.oe.set_service_option('bluez',
                                            'BLUEZ_ENABLED',
                                            'false')   
                if not 'service' in kwargs:
                    if 'bluetooth' in self.oe.dictModules:
                        self.oe.dictModules['bluetooth'].disabled = True
                        self.oe.dictModules['bluetooth'].stop_bluetoothd()
                
            else:

                self.oe.set_service_option('bluez',
                                            'BLUEZ_ENABLED',
                                            'true')                   

                if not 'service' in kwargs:                
                    if 'bluetooth' in self.oe.dictModules:
                        self.oe.dictModules['bluetooth'].disabled = False
                        self.oe.dictModules['bluetooth'].stop_bluetoothd()
                        self.oe.dictModules['bluetooth'].start_bluetoothd()


            self.load_values()
            self.oe.set_busy(0)
            
            self.oe.dbg_log('services::init_bluetooth', 'exit_function',
                            0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('services::init_bluetooth', 'ERROR: ('
                            + repr(e) + ')', 4)

    def stop_samba(self):
        try:

            self.oe.dbg_log('services::stop_samba', 'enter_function', 0)

            pid = self.oe.execute('pidof %s'
                                  % os.path.basename(self.samba_smbd)).split(' '
                    )
            for p in pid:
                self.oe.dbg_log('services::stop_samba PID', unicode(pid)
                                + ' --- ' + unicode(p), 0)
                os.system('kill ' + p.strip().replace('\n', ''))

            pid = self.oe.execute('pidof %s'
                                  % os.path.basename(self.samba_nmbd)).split(' '
                    )
            for p in pid:
                os.system('kill ' + p.strip().replace('\n', ''))

            self.oe.dbg_log('services::stop_samba', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::stop_samba', 'ERROR: (%s)'
                            % repr(e), 4)

    def stop_ssh(self):
        try:

            self.oe.dbg_log('services::stop_ssh', 'enter_function', 0)

            pid = self.oe.execute('pidof %s'
                                  % os.path.basename(self.ssh_daemon)).split(' '
                    )
            for p in pid:
                os.system('kill -9 ' + p.strip().replace('\n', ''))

            self.oe.dbg_log('services::stop_ssh', 'exit_function)', 0)
        except Exception, e:

            self.oe.dbg_log('services::stop_ssh', 'ERROR: (%s)'
                            % repr(e), 4)

    def stop_avahi(self):
        try:

            self.oe.dbg_log('services::stop_avahi', 'enter_function', 0)

            pid = self.oe.execute('pidof %s'
                                  % os.path.basename(self.avahi_daemon)).split(' '
                    )
            for p in pid:
                os.system('kill -9 ' + p.strip().replace('\n', ''))

            self.oe.dbg_log('services::stop_avahi', 'exit_function)', 0)
        except Exception, e:

            self.oe.dbg_log('services::stop_ssh', 'ERROR: (%s)'
                            % repr(e), 4)

    def stop_cron(self):
        try:

            self.oe.dbg_log('services::stop_cron', 'enter_function', 0)

            pid = self.oe.execute('pidof %s'
                                  % os.path.basename(self.cron_daemon)).split(' '
                    )
            for p in pid:
                os.system('kill -9 ' + p.strip().replace('\n', ''))

            self.oe.dbg_log('services::stop_cron', 'exit_function)', 0)
        except Exception, e:

            self.oe.dbg_log('services::stop_cron', 'ERROR: (%s)'
                            % repr(e), 4)

    def stop_syslog(self):
        try:

            self.oe.dbg_log('services::stop_syslog', 'enter_function',
                            0)

            pid = self.oe.execute('pidof %s'
                                  % os.path.basename(self.syslog_daemon)).split(' '
                    )
            for p in pid:
                os.system('kill -9 ' + p.strip().replace('\n', ''))

            self.oe.dbg_log('services::stop_syslog', 'exit_function)',
                            0)
        except Exception, e:

            self.oe.dbg_log('services::stop_syslog', 'ERROR: (%s)'
                            % repr(e), 4)
            
    def exit(self):
        try:

            self.oe.dbg_log('services::exit', 'enter_function', 0)
            self.oe.dbg_log('services::exit', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::exit', 'ERROR: (%s)' % repr(e),
                            4)

    def do_wizard(self):
        try:

            self.oe.dbg_log('services::do_wizard', 'enter_function', 0)

            self.oe.winOeMain.set_wizard_title(self.oe._(32311))

            if hasattr(self, 'samba'):
                self.oe.winOeMain.set_wizard_text(self.oe._(32313)
                        + '[CR][CR]' + self.oe._(32312))
            else:
                self.oe.winOeMain.set_wizard_text(self.oe._(32312))

            self.oe.winOeMain.set_wizard_button_title(self.oe._(32316))

            self.set_wizard_buttons()

            self.oe.dbg_log('services::do_wizard', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::do_wizard', 'ERROR: (%s)'
                            % repr(e))

    def set_wizard_buttons(self):
        try:

            self.oe.dbg_log('services::set_wizard_buttons',
                            'enter_function', 0)

            if self.struct['ssh']['settings']['ssh_autostart']['value'] \
                == '1':
                self.oe.winOeMain.set_wizard_radiobutton_1(self.oe._(32201),
                        self, 'wizard_set_ssh', True)
            else:
                self.oe.winOeMain.set_wizard_radiobutton_1(self.oe._(32201),
                        self, 'wizard_set_ssh')

            if hasattr(self, 'samba'):
                if self.struct['samba']['settings']['samba_autostart'
                        ]['value'] == '1':
                    self.oe.winOeMain.set_wizard_radiobutton_2(self.oe._(32200),
                            self, 'wizard_set_samba', True)
                else:
                    self.oe.winOeMain.set_wizard_radiobutton_2(self.oe._(32200),
                            self, 'wizard_set_samba')

            self.oe.dbg_log('services::set_wizard_buttons',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::set_wizard_buttons',
                            'ERROR: (%s)' % repr(e))

    def wizard_set_ssh(self):
        try:

            self.oe.dbg_log('services::wizard_set_ssh', 'enter_function'
                            , 0)

            if self.struct['ssh']['settings']['ssh_autostart']['value'] \
                == '1':
                self.oe.set_service_option('ssh',
                                            'SSHD_START',
                                            'true')
            else:
                self.oe.set_service_option('ssh',
                                            'SSHD_START',
                                            'false')

            self.load_values()
            self.initialize_ssh()
            self.set_wizard_buttons()

            self.oe.dbg_log('services::wizard_set_ssh', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.dbg_log('services::wizard_set_ssh', 'ERROR: (%s)'
                            % repr(e))

    def wizard_set_samba(self):
        try:

            self.oe.dbg_log('services::wizard_set_samba',
                            'enter_function', 0)

            if self.struct['samba']['settings']['samba_autostart'
                    ]['value'] == '1':
                self.oe.set_service_option('samba',
                                            'SAMBA_ENABLED',
                                            'true')
            else:
                self.oe.set_service_option('samba',
                                            'SAMBA_ENABLED',
                                            'false')

            self.initialize_samba()
            self.load_values()
            self.set_wizard_buttons()

            self.oe.dbg_log('services::wizard_set_samba',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::wizard_set_samba', 'ERROR: (%s)'
                            % repr(e))
