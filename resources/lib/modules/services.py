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
                            'value': '1',
                            'action': 'initialize_samba',
                            'typ': 'bool',
                            'InfoText': 738,
                            },
                        'samba_secure': {
                            'order': 2,
                            'name': 32202,
                            'value': '0',
                            'action': 'initialize_samba',
                            'typ': 'bool',
                            'parent': {'entry': 'samba_autostart',
                                    'value': ['1']},
                            'InfoText': 739,
                            },
                        'samba_username': {
                            'order': 3,
                            'name': 32106,
                            'value': 'openelec',
                            'action': 'initialize_samba',
                            'typ': 'text',
                            'parent': {'entry': 'samba_secure',
                                    'value': ['1']},
                            'InfoText': 740,
                            },
                        'samba_password': {
                            'order': 4,
                            'name': 32107,
                            'value': 'openelec',
                            'action': 'initialize_samba',
                            'typ': 'text',
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
                        'value': '0',
                        'action': 'initialize_ssh',
                        'typ': 'bool',
                        'InfoText': 742,
                        }, 'ssh_unsecure': {
                        'order': 2,
                        'name': 32203,
                        'value': '0',
                        'action': 'initialize_ssh',
                        'typ': 'bool',
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
                        'value': '1',
                        'action': 'initialize_avahi',
                        'typ': 'bool',
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
                        'value': '0',
                        'action': 'initialize_cron',
                        'typ': 'bool',
                        'InfoText': 745,
                        }},
                    },
                'syslog': {
                    'order': 4,
                    'name': 32340,
                    'not_supported': [],
                    'settings': {'remote_syslog_autostart': {
                        'order': 1,
                        'name': 32341,
                        'value': '0',
                        'action': 'initialize_syslog',
                        'typ': 'bool',
                        'InfoText': 746,
                        }, 'remote_syslog_ip': {
                        'order': 2,
                        'name': 32342,
                        'value': '0',
                        'action': 'initialize_syslog',
                        'typ': 'ip',
                        'parent': {'entry': 'remote_syslog_autostart',
                                   'value': ['1']},
                        'InfoText': 747,
                        }},
                    },
                'bt': {
                    'order': 5,
                    'name': 32331,
                    'not_supported': [],
                    'settings': {'disable_bt': {
                        'order': 1,
                        'name': 32344,
                        'value': '0',
                        'action': 'init_bluetooth',
                        'typ': 'bool',
                        'InfoText': 720,
                        }},
                    },                        
                }

            self.oe = oeMain

            self.kernel_cmd = '/proc/cmdline'
            
            self.samba_conf = '/var/run/smb.conf'
            self.samba_user_conf = '%s/samba.conf' % self.oe.USER_CONFIG
            self.samba_default_conf = '/etc/samba/smb.conf'
            self.samba_nmbd_pid = '/var/run/nmbd-smb.conf.pid'
            self.samba_smbd_pid = '/var/run/smbd-smb.conf.pid'
            self.samba_username_map = '/var/run/samba.map'
            self.samba_nmbd = '/usr/bin/nmbd'
            self.samba_smbd = '/usr/bin/smbd'

            self.ssh_daemon = '/usr/sbin/sshd'
            self.ssh_conf_dir =  self.oe.USER_CONFIG
            self.ssh_conf_file = 'sshd.conf'
            self.sshd_init = '/etc/init.d/51_sshd'

            self.avahi_daemon = '/usr/sbin/avahi-daemon'
            self.avahi_init = '/etc/init.d/53_avahi'

            self.cron_daemon = '/sbin/crond'
            self.crond_init = '/etc/init.d/09_crond'

            self.syslog_daemon = '/sbin/syslogd'
            self.syslog_conf_file = '%s/syslog/remote' % self.oe.CONFIG_CACHE
            self.syslog_start = '/etc/init.d/08_syslogd'

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

            # self.initialize_ssh(service=1)

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

            if 'bluetooth' in self.oe.dictModules:
                self.oe.dictModules['bluetooth'].stop_bluetoothd()

            self.oe.dbg_log('service::stop_service', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('service::stop_service', 'ERROR: ('
                            + repr(e) + ')')

    def do_init(self):
        try:

            self.oe.dbg_log('services::do_init', 'exit_function', 0)
            self.oe.dbg_log('services::do_init', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::do_init', 'ERROR: (%s)'
                            % repr(e))

    def load_menu(self, focusItem):

        try:

            self.oe.dbg_log('services::load_menu', 'enter_function', 0)

            for category in sorted(self.struct, key=lambda x: \
                                   self.struct[x]['order']):
                if 'not_supported' in self.struct[category]:
                    if self.arch \
                        in self.struct[category]['not_supported'] \
                        or not hasattr(self, category):
                        continue

                self.oe.winOeMain.addConfigItem(self.oe._(self.struct[category]['name'
                        ]), {'typ': 'separator'},
                        focusItem.getProperty('listTyp'))

                for setting in sorted(self.struct[category]['settings'
                        ], key=lambda x: \
                        self.struct[category]['settings'][x]['order']):   

                    if 'not_supported' in self.struct[category]['settings'][setting]:

                        #skip setting
                        self.oe.dbg_log('services::load_menu', 'skip setting ' + setting, 0)
                        
                    else:
                      
                        dictProperties = {
                            'entry': setting,
                            'category': category,
                            'action': self.struct[category]['settings'
                                    ][setting]['action'],
                            'value': self.struct[category]['settings'
                                    ][setting]['value'],
                            'typ': self.struct[category]['settings'
                                    ][setting]['typ'],
                            }

                        if 'InfoText' in self.struct[category]['settings'
                                ][setting]:
                            dictProperties['InfoText'] = \
                                self.oe._(self.struct[category]['settings'
                                    ][setting]['InfoText'])

                        if 'values' in self.struct[category]['settings'
                                ][setting]:
                            if len(self.struct[category]['settings'
                                  ][setting]['values']) > 0:
                                dictProperties['values'] = \
                                    ','.join(self.struct[category]['settings'
                                        ][setting]['values'])

                        if not 'parent' in self.struct[category]['settings'
                                ][setting]:

                            self.oe.winOeMain.addConfigItem(self.oe._(self.struct[category]['settings'
                                    ][setting]['name']), dictProperties,
                                    focusItem.getProperty('listTyp'))
                        else:

                            if self.struct[category]['settings'
                                    ][self.struct[category]['settings'
                                      ][setting]['parent']['entry']]['value'
                                    ] in self.struct[category]['settings'
                                    ][setting]['parent']['value']:

                                self.oe.winOeMain.addConfigItem(self.oe._(self.struct[category]['settings'
                                        ][setting]['name']),
                                        dictProperties,
                                        focusItem.getProperty('listTyp'))

            self.oe.dbg_log('services::load_menu', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::load_menu', 'ERROR: (%s)'
                            % repr(e))

    def load_values(self):
        try:

            self.oe.dbg_log('services::load_values', 'enter_function',
                            0)

            self.arch = self.oe.load_file('/etc/arch')

            # SSH
            if os.path.isfile(self.ssh_daemon):
                self.ssh = True

                if os.path.exists(self.ssh_conf_dir + '/'
                                  + self.ssh_conf_file):
                    ssh_file = open(self.ssh_conf_dir + '/'
                                    + self.ssh_conf_file, 'r')
                    for line in ssh_file:
                        if 'SSHD_START' in line:
                            if line.split('=')[-1].lower().strip() \
                                == 'true':
                                self.struct['ssh']['settings'
                                        ]['ssh_autostart']['value'] = \
                                    '1'
                                self.oe.write_setting('services',
                                        'ssh_autostart', '1')
                            else:
                                self.struct['ssh']['settings'
                                        ]['ssh_autostart']['value'] = \
                                    '0'
                                self.oe.write_setting('services',
                                        'ssh_autostart', '0')

                        if 'SSHD_DISABLE_PW_AUTH' in line:
                            if line.split('=')[-1].lower().strip() \
                                == 'true':
                                self.struct['ssh']['settings'
                                        ]['ssh_unsecure']['value'] = '1'
                                self.oe.write_setting('services',
                                        'ssh_unsecure', '1')
                            else:
                                self.struct['ssh']['settings'
                                        ]['ssh_unsecure']['value'] = '0'
                                self.oe.write_setting('services',
                                        'ssh_unsecure', '0')

                    ssh_file.close()

                    cmd_file = open(self.kernel_cmd, 'r')
                    cmd_args = cmd_file.read()
                    if 'ssh' in cmd_args:
                        self.struct['ssh']['settings']['ssh_autostart'] \
                        ['not_supported'] = True

                    cmd_file.close()
                            
            if os.path.isfile(self.samba_nmbd) \
                and os.path.isfile(self.samba_smbd):
                self.samba = True
                for entry in self.struct['samba']['settings']:
                    value = self.oe.read_setting('services', entry)
                    if not value is None:
                        self.struct['samba']['settings'][entry]['value'
                                ] = value

            if os.path.isfile(self.avahi_daemon):
                self.avahi = True
                value = self.oe.read_setting('services',
                        'avahi_autostart')
                if not value is None:
                    self.struct['avahi']['settings']['avahi_autostart'
                            ]['value'] = value

            if os.path.isfile(self.cron_daemon):
                self.cron = True
                value = self.oe.read_setting('services',
                        'cron_autostart')
                if not value is None:
                    self.struct['cron']['settings']['cron_autostart'
                            ]['value'] = value

            if os.path.isfile(self.syslog_daemon):
                self.syslog = True
                value = self.oe.read_setting('services',
                        'remote_syslog_autostart')
                ip = self.oe.read_setting('services', 'remote_syslog_ip'
                        )
                if value != None and ip != None:
                    self.struct['syslog']['settings'
                            ]['remote_syslog_autostart']['value'] = \
                        value
                    self.struct['syslog']['settings']['remote_syslog_ip'
                            ]['value'] = ip

            value = self.oe.read_setting('services',
                    'disable_bt')
            if not value is None:
                self.struct['bt']['settings']['disable_bt'
                        ]['value'] = value
            self.bt = True
            
            self.oe.dbg_log('services::load_values', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::load_values', 'ERROR: (%s)'
                            % repr(e))

    def set_value(self, listItem=None):
        try:

            self.oe.dbg_log('services::set_value', 'enter_function', 0)

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')

            self.oe.write_setting('services',
                                  listItem.getProperty('entry'),
                                  unicode(listItem.getProperty('value')))

            self.oe.dbg_log('services::set_value', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::set_value', 'ERROR: (%s)'
                            % repr(e), 4)

    def initialize_samba(self, **kwargs):
        try:

            self.oe.dbg_log('services::initialize_samba',
                            'enter_function', 0)

            self.oe.set_busy(1)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])

            if self.struct['samba']['settings']['samba_autostart'
                    ]['value'] != '1':
                self.stop_samba()
                self.oe.dbg_log('services::initialize_samba',
                                'exit_function (samba disabled)', 0)
                
                self.oe.set_service_option('samba',
                                            'SAMBA_ENABLED',
                                            'false')
                
                self.oe.set_busy(0)
                return
            else:

                self.samba_active_conf = ConfigParser.ConfigParser()

                if os.path.isfile(self.samba_user_conf):
                    self.samba_active_conf.readfp(StringIO('\n'.join(line.strip()
                            for line in open(self.samba_user_conf))))
                else:
                    self.samba_active_conf.readfp(StringIO('\n'.join(line.strip()
                            for line in open(self.samba_default_conf))))

                self.oe.set_service_option('samba',
                                            'SAMBA_ENABLED',
                                            'true')
                
                if self.struct['samba']['settings']['samba_secure'
                        ]['value'] == '1' and self.struct['samba'
                        ]['settings']['samba_username']['value'] != '' \
                    and self.struct['samba']['settings'
                        ]['samba_password']['value'] != '':

                    os.system('echo -e "%(pw)s\n%(pw)s" | smbpasswd -s -a root >/dev/null 2>&1'
                               % {'pw': self.struct['samba']['settings'
                              ]['samba_password']['value']})

                    samba_map = open(self.samba_username_map, 'w')
                    samba_map.write('nobody = root\n')
                    samba_map.write('root = %s\n' % self.struct['samba'
                                    ]['settings']['samba_username'
                                    ]['value'])
                    samba_map.close()

                    for entry in self.samba_active_conf.sections():
                        if self.samba_active_conf.has_option(entry,
                                'public') and entry.lower() != 'global':
                            self.samba_active_conf.set(entry, 'public',
                                    'no')

                    self.samba_active_conf.set('global', 'security',
                            'user')

                    self.samba_active_conf.set('global', 'username map'
                            , self.samba_username_map)
                    
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

                    for entry in self.samba_active_conf.sections():
                        if self.samba_active_conf.has_option(entry,
                                'public') and entry.lower() != 'global':
                            self.samba_active_conf.set(entry, 'public',
                                    'yes')

                    self.samba_active_conf.set('global', 'security',
                            'share')

                    if self.samba_active_conf.has_option('global',
                            'username map'):
                        self.samba_active_conf.remove_option('global',
                                'username map')

                    self.oe.set_service_option('samba',
                                               'SAMBA_SECURE',
                                               'false')
                    
                with open(self.samba_conf, 'wb') as configfile:
                    self.samba_active_conf.write(configfile)

                self.stop_samba()

                os.system('%s --daemon --configfile=%s'
                          % (self.samba_nmbd, self.samba_conf))
                os.system('%s --daemon --configfile=%s'
                          % (self.samba_smbd, self.samba_conf))

                self.oe.dbg_log('services::initialize_samba',
                                'exit_function (samba enabled)', 0)

            self.oe.set_busy(0)
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
                == '0':
                self.oe.dbg_log('services::initialize_ssh',
                                'exit_function (ssh disabled)', 0)

                if os.path.exists(self.ssh_conf_dir + '/'
                                  + self.ssh_conf_file):
                    os.remove(self.ssh_conf_dir + '/'
                              + self.ssh_conf_file)

                self.oe.set_service_option('ssh',
                                            'SSHD_START',
                                            'false')
                
                self.stop_ssh()

                self.oe.set_busy(0)
                return

            else:
                self.oe.set_service_option('ssh',
                                            'SSHD_START',
                                            'true')
                
            if not os.path.exists(self.ssh_conf_dir):
                os.makedirs(self.ssh_conf_dir)

            ssh_conf = open(self.ssh_conf_dir + '/'
                            + self.ssh_conf_file, 'w')
            ssh_conf.write('SSHD_START=true\n')
            if self.struct['ssh']['settings']['ssh_unsecure']['value'] \
                == '1':
                ssh_conf.write('SSHD_DISABLE_PW_AUTH=true\n')
                self.oe.set_service_option('ssh',
                                            'SSHD_DISABLE_PW_AUTH',
                                            'true')
                
            else:
                self.oe.set_service_option('ssh',
                                            'SSHD_DISABLE_PW_AUTH',
                                            'false')   
                
            ssh_conf.close()

            self.stop_ssh()
            os.system('sh ' + self.sshd_init)

            self.oe.set_busy(0)

            self.oe.dbg_log('services::initialize_ssh',
                            'exit_function (ssh enabled)', 0)
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
                self.oe.dbg_log('services::initialize_avahi',
                                'exit_function (avahi disabled)', 0)
                
                self.oe.set_service_option('avahi',
                                            'AVAHI_ENABLED',
                                            'false')   
                
                self.stop_avahi()
                self.oe.set_busy(0)
                return

            else:
                self.oe.set_service_option('avahi',
                                            'AVAHI_ENABLED',
                                            'true')   
                
            self.stop_avahi()
            os.system('sh ' + self.avahi_init)

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
                self.oe.dbg_log('services::initialize_cron',
                                'exit_function (cron disabled)', 0)
                
                self.oe.set_service_option('cron',
                                            'CRON_ENABLED',
                                            'false')   
                
                self.stop_cron()
                self.oe.set_busy(0)
                return

            else:
                self.oe.set_service_option('cron',
                                            'CRON_ENABLED',
                                            'true')   
                
            self.stop_cron()
            os.system('sh ' + self.crond_init)

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
                    ]['remote_syslog_autostart']['value'] == '1' \
                and self.struct['syslog']['settings']['remote_syslog_ip'
                    ]['value'] != '':

                if not os.path.exists(os.path.dirname(self.syslog_conf_file)):
                    os.makedirs(os.path.dirname(self.syslog_conf_file))

                config_file = open(self.syslog_conf_file, 'w')
                config_file.write('SYSLOG_REMOTE="true"\n')
                config_file.write('SYSLOG_SERVER="'
                                  + self.struct['syslog']['settings'
                                  ]['remote_syslog_ip']['value'] + '"\n'
                                  )
                config_file.close()
            else:

                if os.path.exists(self.syslog_conf_file):
                    os.remove(self.syslog_conf_file)

            self.stop_syslog()
            os.system('sh ' + self.syslog_start)

            self.oe.set_busy(0)

            self.oe.dbg_log('services::initialize_syslog',
                            'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_syslog', 'ERROR: (%s)'
                             % repr(e), 4)

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

            if os.path.isfile(self.samba_nmbd_pid):
                os.remove(self.samba_nmbd_pid)

            if os.path.isfile(self.samba_smbd_pid):
                os.remove(self.samba_smbd_pid)

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


    def init_bluetooth(self, listItem=None):
        try:

            self.oe.dbg_log('services::init_bluetooth', 'enter_function',
                            0)

            if not listItem == None:
                self.set_value(listItem)

            if self.struct['bt']['settings']['disable_bt']['value'] \
                == '0' or self.struct['bt']['settings']['disable_bt'
                    ]['value'] == None:

                if 'bluetooth' in self.oe.dictModules:
                    self.oe.dictModules['bluetooth'].start_bluetoothd()

                self.oe.set_service_option('bluez',
                                            'BLUEZ_ENABLED',
                                            'true')   
                
            else:
                self.oe.set_service_option('bluez',
                                            'BLUEZ_ENABLED',
                                            'false')   
                
                if 'bluetooth' in self.oe.dictModules:
                    self.oe.dictModules['bluetooth'].stop_bluetoothd()

            self.oe.dbg_log('services::init_bluetooth', 'exit_function',
                            0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('services::init_bluetooth', 'ERROR: ('
                            + repr(e) + ')', 4)
            
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
                self.struct['ssh']['settings']['ssh_autostart']['value'
                        ] = '0'
            else:
                self.struct['ssh']['settings']['ssh_autostart']['value'
                        ] = '1'

            self.oe.write_setting('services', 'ssh',
                                  unicode(self.struct['ssh']['settings'
                                  ]['ssh_autostart']['value']))
            self.struct['ssh']['settings']['ssh_autostart']['changed'
                    ] = True

            self.initialize_ssh()
            self.set_wizard_buttons()

            del self.struct['ssh']['settings']['ssh_autostart'
                    ]['changed']

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
                self.struct['samba']['settings']['samba_autostart'
                        ]['value'] = '0'
            else:
                self.struct['samba']['settings']['samba_autostart'
                        ]['value'] = '1'

            self.oe.write_setting('services', 'samba',
                                  unicode(self.struct['samba']['settings'
                                  ]['samba_autostart']['value']))
            self.struct['samba']['settings']['samba_autostart'
                    ]['changed'] = True

            self.initialize_samba()
            self.set_wizard_buttons()

            del self.struct['samba']['settings']['samba_autostart'
                    ]['changed']

            self.oe.dbg_log('services::wizard_set_samba',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('services::wizard_set_samba', 'ERROR: (%s)'
                            % repr(e))
