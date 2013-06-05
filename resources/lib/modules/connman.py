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
import oeWindows
import time
import dbus
import xbmcgui
import dbus.service
import threading
import gobject
import uuid
import os
import ConfigParser


class networkMount(object):

    def __init__(self, mount_id, oeMain):
        try:

            oeMain.dbg_log('networkMount::__init__', 'enter_function',
                           0)

            oeMain.set_busy(1)

            self.struct = {'mount': {
                'order': 1,
                'name': 32350,
                'menuLoader': 'menu_network_configuration',
                'settings': {
                    'type': {
                        'order': 1,
                        'name': 32351,
                        'value': '',
                        'type': 'multivalue',
                        'values': ['cifs', 'nfs'],
                        },
                    'mountpoint': {
                        'order': 2,
                        'name': 32352,
                        'value': '',
                        'type': 'text',
                        'parent': {'entry': 'type', 'value': ['cifs',
                                   'nfs']},
                        },
                    'server': {
                        'order': 3,
                        'name': 32353,
                        'value': '',
                        'type': 'text',
                        'parent': {'entry': 'type', 'value': ['cifs',
                                   'nfs']},
                        },
                    'share': {
                        'order': 4,
                        'name': 32354,
                        'value': '',
                        'type': 'text',
                        'parent': {'entry': 'type', 'value': ['cifs',
                                   'nfs']},
                        },
                    'user': {
                        'order': 5,
                        'name': 32355,
                        'value': '',
                        'type': 'text',
                        'parent': {'entry': 'type', 'value': ['cifs',
                                   'nfs']},
                        },
                    'pass': {
                        'order': 6,
                        'name': 32356,
                        'value': '',
                        'type': 'text',
                        'parent': {'entry': 'type', 'value': ['cifs',
                                   'nfs']},
                        },
                    'options': {
                        'order': 7,
                        'name': 32357,
                        'value': '',
                        'type': 'text',
                        'parent': {'entry': 'type', 'value': ['cifs',
                                   'nfs']},
                        },
                    },
                }}

            self.oe = oeMain
            self.winOeMount = oeWindows.mainWindow('mainWindow.xml',
                    self.oe.__cwd__, 'Default', oeMain=oeMain,
                    isChild=True)
            self.mount_id = mount_id
            self.oe.dictModules['networkMount'] = self
            self.winOeMount.show()
            self.current_mountpoint = None

            if self.mount_id != 'new_mount':

                mount_dict = self.oe.read_node('mounts')
                if self.mount_id in mount_dict['mounts']:
                    for entry in self.struct['mount']['settings']:
                        self.struct['mount']['settings'][entry]['value'
                                ] = mount_dict['mounts'
                                ][self.mount_id][entry]

                    self.current_mountpoint = mount_dict['mounts'
                            ][self.mount_id]['mountpoint']

            for strEntry in sorted(self.struct, key=lambda x: \
                                   self.struct[x]['order']):

                dictProperties = {
                    'modul': 'networkMount',
                    'listTyp': self.oe.listObject['list'],
                    'menuLoader': 'menu_loader',
                    'category': strEntry,
                    }

                self.winOeMount.addMenuItem(self.struct[strEntry]['name'
                        ], dictProperties)

            self.oe.set_busy(0)

            self.winOeMount.doModal()

            del self.winOeMount
            del self.oe.dictModules['networkMount']

            oeMain.dbg_log('networkMount::__init__', 'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('networkMount::__init__', 'ERROR: ('
                            + repr(e) + ')', 4)

    def menu_loader(self, menuItem):
        try:

            self.oe.dbg_log('networkMount::menu_loader',
                            'enter_function', 0)

            self.winOeMount.showButton(3, 32140, 'networkMount',
                    'save_mount')

            if self.mount_id != 'new_mount':
                self.winOeMount.showButton(2, 32141, 'networkMount',
                        'delete_mount')
            category = 'mount'
            for entry in sorted(self.struct[category]['settings'],
                                key=lambda x: \
                                self.struct[category]['settings'
                                ][x]['order']):

                dictProperties = {
                    'value': self.struct[category]['settings'
                            ][entry]['value'],
                    'typ': self.struct[category]['settings'
                            ][entry]['type'],
                    'entry': entry,
                    'category': category,
                    'action': 'set_value',
                    }

                if 'values' in self.struct[category]['settings'][entry]:
                    dictProperties['values'] = \
                        ','.join(self.struct[category]['settings'
                                 ][entry]['values'])

                if not 'parent' in self.struct[category]['settings'
                        ][entry]:

                    self.winOeMount.addConfigItem(self.oe._(self.struct[category]['settings'
                            ][entry]['name']), dictProperties,
                            self.oe.listObject['list'])
                else:

                    if self.struct[category]['settings'
                            ][self.struct[category]['settings'
                              ][entry]['parent']['entry']]['value'] \
                        in self.struct[category]['settings'
                            ][entry]['parent']['value']:

                        self.winOeMount.addConfigItem(self.oe._(self.struct[category]['settings'
                                ][entry]['name']), dictProperties,
                                self.oe.listObject['list'])

            self.oe.dbg_log('networkMount::menu_loader', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.dbg_log('networkMount::menu_loader', 'ERROR: ('
                            + repr(e) + ')', 4)

    def set_value(self, listItem):
        try:

            self.oe.dbg_log('networkMount::set_value', 'enter_function'
                            , 0)

            if listItem.getProperty('entry') == 'mountpoint':
                s = listItem.getProperty('value')
                listItem.setProperty('value', ''.join(x for x in s
                        if x.isalnum()))

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['changed'] = True

            self.oe.dbg_log('networkMount::set_value', 'exit_function',
                            0)
        except Exception, e:

            self.oe.dbg_log('networkMount::set_value', 'ERROR: ('
                            + repr(e) + ')', 4)

    def save_mount(self):
        try:

            self.oe.dbg_log('save_mount::save_mount', 'enter_function',
                            0)

            if self.struct['mount']['settings']['mountpoint']['value'] \
                == '':
                dialog = xbmcgui.Dialog()
                dialog.ok('Mount', self.oe._(32361), '',
                          self.oe._(32352))
                return

            if self.struct['mount']['settings']['server']['value'] \
                == '':
                dialog = xbmcgui.Dialog()
                dialog.ok('Mount', self.oe._(32361), '',
                          self.oe._(32353))
                return

            if self.struct['mount']['settings']['share']['value'] == '':
                dialog = xbmcgui.Dialog()
                dialog.ok('Mount', self.oe._(32361), '',
                          self.oe._(32354))
                return

            self.oe.set_busy(1)

            if self.current_mountpoint != None \
                and os.path.exists('/media/' + self.current_mountpoint):
                umount = self.oe.execute('umount /media/'
                        + self.current_mountpoint)
            else:
                umount = ''

            if 'busy' in umount:
                xbmc.executebuiltin('Notification(Umount Error, '
                                    + umount + ')')
                self.oe.set_busy(0)
                return 'close'

            if self.mount_id == 'new_mount':
                mount_uuid = 'mount_' + str(uuid.uuid1()).replace('-',
                        '')
            else:
                self.oe.remove_node(self.mount_id)
                mount_uuid = self.mount_id

            mount_info = {}

            mount_info['type'] = self.struct['mount']['settings']['type'
                    ]['value']
            self.oe.write_setting(mount_uuid, 'type',
                                  self.struct['mount']['settings'
                                  ]['type']['value'], 'mounts')

            mount_info['mountpoint'] = self.struct['mount']['settings'
                    ]['mountpoint']['value']
            self.oe.write_setting(mount_uuid, 'mountpoint',
                                  self.struct['mount']['settings'
                                  ]['mountpoint']['value'], 'mounts')

            mount_info['server'] = self.struct['mount']['settings'
                    ]['server']['value']
            self.oe.write_setting(mount_uuid, 'server',
                                  self.struct['mount']['settings'
                                  ]['server']['value'], 'mounts')

            mount_info['share'] = self.struct['mount']['settings'
                    ]['share']['value']
            self.oe.write_setting(mount_uuid, 'share',
                                  self.struct['mount']['settings'
                                  ]['share']['value'], 'mounts')

            mount_info['user'] = self.struct['mount']['settings']['user'
                    ]['value']
            self.oe.write_setting(mount_uuid, 'user',
                                  self.struct['mount']['settings'
                                  ]['user']['value'], 'mounts')

            mount_info['pass'] = self.struct['mount']['settings']['pass'
                    ]['value']
            self.oe.write_setting(mount_uuid, 'pass',
                                  self.struct['mount']['settings'
                                  ]['pass']['value'], 'mounts')

            mount_info['options'] = self.struct['mount']['settings'
                    ]['options']['value']
            self.oe.write_setting(mount_uuid, 'options',
                                  self.struct['mount']['settings'
                                  ]['options']['value'], 'mounts')

            self.oe.dictModules['connman'].mount_drive(mount_info)

            self.oe.dbg_log('save_mount::save_mount', 'exit_function',
                            0)

            self.oe.set_busy(0)

            return 'close'
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('save_mount::save_mount', 'ERROR: ('
                            + repr(e) + ')', 4)

    def delete_mount(self):
        try:

            self.oe.dbg_log('save_mount::delete_mount', 'enter_function'
                            , 0)

            umount = self.oe.execute('umount /media/'
                    + self.current_mountpoint)
            if 'busy' in umount:
                xbmc.executebuiltin('Notification(Umount Error, '
                                    + umount + ')')
            else:
                self.oe.remove_node(self.mount_id)

            self.oe.dbg_log('save_mount::delete_mount', 'exit_function'
                            , 0)

            return 'close'
        except Exception, e:

            self.oe.dbg_log('save_mount::delete_mount', 'ERROR: ('
                            + repr(e) + ')', 4)

    def exit(self):
        pass


class connmanService(object):

    menu = {}

    def __init__(self, servicePath, oeMain):
        try:

            oeMain.dbg_log('connmanService::__init__', 'enter_function'
                           , 0)

            oeMain.set_busy(1)

            self.struct = {
                'AutoConnect': {
                    'order': 1,
                    'name': 32110,
                    'type': 'Boolean',
                    'menuLoader': 'menu_network_configuration',
                    'settings': {'AutoConnect': {
                        'order': 1,
                        'name': 32109,
                        'value': '',
                        'type': 'bool',
                        'dbus': 'Boolean',
                        }},
                    },
                'IPv4': {
                    'order': 2,
                    'name': 32111,
                    'type': 'Dictionary',
                    'settings': {
                        'Method': {
                            'order': 1,
                            'name': 32113,
                            'value': '',
                            'type': 'multivalue',
                            'dbus': 'String',
                            'values': ['dhcp', 'manual', 'off'],
                            },
                        'Address': {
                            'order': 2,
                            'name': 32114,
                            'value': '',
                            'type': 'ip',
                            'dbus': 'String',
                            'parent': {'entry': 'Method',
                                    'value': ['manual']},
                            },
                        'Netmask': {
                            'order': 3,
                            'name': 32115,
                            'value': '',
                            'type': 'ip',
                            'dbus': 'String',
                            'parent': {'entry': 'Method',
                                    'value': ['manual']},
                            },
                        'Gateway': {
                            'order': 4,
                            'name': 32116,
                            'value': '',
                            'type': 'ip',
                            'dbus': 'String',
                            'parent': {'entry': 'Method',
                                    'value': ['manual']},
                            },
                        },
                    },
                'IPv6': {
                    'order': 3,
                    'name': 32112,
                    'type': 'Dictionary',
                    'settings': {
                        'Method': {
                            'order': 1,
                            'name': 32113,
                            'value': '',
                            'type': 'multivalue',
                            'dbus': 'String',
                            'values': ['auto', 'manual', '6to4', 'off'
                                    ],
                            },
                        'Address': {
                            'order': 2,
                            'name': 32114,
                            'value': '',
                            'type': 'text',
                            'dbus': 'String',
                            'parent': {'entry': 'Method',
                                    'value': ['manual']},
                            },
                        'PrefixLength': {
                            'order': 4,
                            'name': 32117,
                            'value': '',
                            'type': 'text',
                            'dbus': 'Byte',
                            'parent': {'entry': 'Method',
                                    'value': ['manual']},
                            },
                        'Gateway': {
                            'order': 3,
                            'name': 32116,
                            'value': '',
                            'type': 'text',
                            'dbus': 'String',
                            'parent': {'entry': 'Method',
                                    'value': ['manual']},
                            },
                        'Privacy': {
                            'order': 5,
                            'name': 32118,
                            'value': '',
                            'type': 'multivalue',
                            'dbus': 'String',
                            'parent': {'entry': 'Method',
                                    'value': ['manual']},
                            'values': ['disabled', 'enabled', 'prefered'
                                    ],
                            },
                        },
                    },
                'Nameservers': {
                    'order': 4,
                    'name': 32119,
                    'type': 'Array',
                    'settings': {'0': {
                        'order': 1,
                        'name': 32120,
                        'value': '',
                        'type': 'ip',
                        'dbus': 'String',
                        }, '1': {
                        'order': 2,
                        'name': 32121,
                        'value': '',
                        'type': 'ip',
                        'dbus': 'String',
                        }, '2': {
                        'order': 3,
                        'name': 32122,
                        'value': '',
                        'type': 'ip',
                        'dbus': 'String',
                        }},
                    },
                'Timeservers': {
                    'order': 6,
                    'name': 32123,
                    'type': 'Array',
                    'settings': {'0': {
                        'order': 1,
                        'name': 32124,
                        'value': '',
                        'type': 'text',
                        'dbus': 'String',
                        }, '1': {
                        'order': 2,
                        'name': 32125,
                        'value': '',
                        'type': 'text',
                        'dbus': 'String',
                        }, '2': {
                        'order': 3,
                        'name': 32126,
                        'value': '',
                        'type': 'text',
                        'dbus': 'String',
                        }},
                    },
                'Domains': {
                    'order': 5,
                    'name': 32127,
                    'type': 'Array',
                    'settings': {'0': {
                        'order': 1,
                        'name': 32128,
                        'value': '',
                        'type': 'text',
                        'dbus': 'String',
                        }, '1': {
                        'order': 2,
                        'name': 32129,
                        'value': '',
                        'type': 'text',
                        'dbus': 'String',
                        }, '2': {
                        'order': 3,
                        'name': 32130,
                        'value': '',
                        'type': 'text',
                        'dbus': 'String',
                        }},
                    },
                }

            self.datamap = {
                0: {'AutoConnect': 'AutoConnect'},
                1: {'IPv4': 'IPv4'},
                2: {'IPv4.Configuration': 'IPv4'},
                3: {'IPv6': 'IPv6'},
                4: {'IPv6.Configuration': 'IPv6'},
                5: {'Nameservers': 'Nameservers'},
                6: {'Nameservers.Configuration': 'Nameservers'},
                7: {'Domains': 'Domains'},
                8: {'Domains.Configuration': 'Domains'},
                9: {'Timeservers': 'Timeservers'},
                10: {'Timeservers.Configuration': 'Timeservers'},
                }

            self.oe = oeMain
            self.dbusSystemBus = self.oe.dbusSystemBus
            self.winOeCon = oeWindows.mainWindow('mainWindow.xml',
                    self.oe.__cwd__, 'Default', oeMain=oeMain,
                    isChild=True)
            self.dbusConnmanManager = \
                dbus.Interface(self.dbusSystemBus.get_object('net.connman'
                               , '/'), 'net.connman.Manager')
            self.servicePath = servicePath
            self.oe.dictModules['connmanNetworkConfig'] = self

            self.service = \
                dbus.Interface(self.dbusSystemBus.get_object('net.connman'
                               , servicePath), 'net.connman.Service')
            self.service_properties = self.service.GetProperties()

            if self.service_properties['Type'] == 'vpn':
                self.dbusConnmanManager = \
                    dbus.Interface(self.dbusSystemBus.get_object('net.connman.vpn'
                                   , '/'), 'net.connman.vpn.Manager')
                self.vpn_connections = \
                    self.dbusConnmanManager.GetConnections()
                for (self.servicePath, self.vpn_properties) in \
                    self.vpn_connections:
                    if self.servicePath.split('/')[-1] \
                        in servicePath.split('/')[-1]:
                        self.service_properties['Provider'] = \
                            self.vpn_properties
                        break

            for entry in sorted(self.datamap):
                for (key, value) in self.datamap[entry].iteritems():

                    if self.struct[value]['type'] == 'Boolean':
                        if key in self.service_properties:
                            self.struct[value]['settings'
                                    ][value]['value'] = \
                                self.service_properties[key]

                    if self.struct[value]['type'] == 'Dictionary':
                        if key in self.service_properties:
                            for setting in self.struct[value]['settings'
                                    ]:
                                if setting \
                                    in self.service_properties[key]:
                                    self.struct[value]['settings'
        ][setting]['value'] = self.service_properties[key][setting]

                    if self.struct[value]['type'] == 'Array':
                        if key in self.service_properties:
                            for setting in self.struct[value]['settings'
                                    ]:
                                if int(setting) \
                                    < len(self.service_properties[key]):
                                    self.struct[value]['settings'
        ][setting]['value'] = self.service_properties[key][int(setting)]

            self.winOeCon.show()

            for strEntry in sorted(self.struct, key=lambda x: \
                                   self.struct[x]['order']):

                if strEntry == 'Provider':
                    if 'Type' in self.service_properties:
                        if not self.service_properties['Type'] == 'vpn':
                            break

                if strEntry != 'Provider':
                    if 'Type' in self.service_properties:
                        if self.service_properties['Type'] == 'vpn':
                            continue

                dictProperties = {
                    'modul': 'connmanNetworkConfig',
                    'listTyp': self.oe.listObject['list'],
                    'menuLoader': 'menu_loader',
                    'category': strEntry,
                    }

                self.winOeCon.addMenuItem(self.struct[strEntry]['name'
                        ], dictProperties)

            self.oe.set_busy(0)

            self.winOeCon.doModal()

            del self.winOeCon
            del self.oe.dictModules['connmanNetworkConfig']

            self.oe.dbg_log('connmanService::__init__', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connmanService::__init__', 'ERROR: ('
                            + repr(e) + ')', 4)

    def cancel(self):
        try:

            self.oe.dbg_log('connmanService::cancel', 'exit_function',
                            0)

            self.oe.set_busy(1)
            self.winOeCon.close()
            self.oe.set_busy(0)
            self.oe.dbg_log('connmanService::cancel', 'exit_function',
                            0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connmanService::cancel', 'ERROR: ('
                            + repr(e) + ')', 4)

    def menu_loader(self, menuItem):
        try:

            self.oe.dbg_log('connmanService::menu_loader',
                            'enter_function', 0)

            self.winOeCon.showButton(3, 32140, 'connmanNetworkConfig',
                    'save_network')

            self.winOeCon.showButton(2, 32212, 'connmanNetworkConfig',
                    'cancel')

            if self.servicePath not in ['new_vpn']:
                if self.service_properties['Type'] in ['wifi']:
                    if self.service_properties['Favorite'] == True:
                        self.winOeCon.showButton(1, 32141,
                                'connmanNetworkConfig', 'delete_network'
                                )

                if self.service_properties['State'] in ['ready',
                        'online']:
                    self.winOeCon.showButton(
                        4,
                        32143,
                        'connmanNetworkConfig',
                        'disconnect_network',
                        self.oe.listObject['list'],
                        self.oe.listObject['list'],
                        )
                else:

                    self.winOeCon.showButton(
                        4,
                        32144,
                        'connmanNetworkConfig',
                        'connect_network',
                        self.oe.listObject['list'],
                        self.oe.listObject['list'],
                        )

            category = menuItem.getProperty('category')
            for entry in sorted(self.struct[category]['settings'],
                                key=lambda x: \
                                self.struct[category]['settings'
                                ][x]['order']):

                dictProperties = {
                    'value': self.struct[category]['settings'
                            ][entry]['value'],
                    'typ': self.struct[category]['settings'
                            ][entry]['type'],
                    'entry': entry,
                    'category': category,
                    'action': 'set_value',
                    }

                if 'values' in self.struct[category]['settings'][entry]:
                    dictProperties['values'] = \
                        ','.join(self.struct[category]['settings'
                                 ][entry]['values'])

                if not 'parent' in self.struct[category]['settings'
                        ][entry]:

                    self.winOeCon.addConfigItem(self.oe._(self.struct[category]['settings'
                            ][entry]['name']), dictProperties,
                            menuItem.getProperty('listTyp'))
                else:

                    if self.struct[category]['settings'
                            ][self.struct[category]['settings'
                              ][entry]['parent']['entry']]['value'] \
                        in self.struct[category]['settings'
                            ][entry]['parent']['value']:

                        self.winOeCon.addConfigItem(self.oe._(self.struct[category]['settings'
                                ][entry]['name']), dictProperties,
                                menuItem.getProperty('listTyp'))

            self.oe.dbg_log('connmanService::menu_loader',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connmanService::menu_loader', 'ERROR: ('
                            + repr(e) + ')', 4)

    def set_value(self, listItem):
        try:

            self.oe.dbg_log('connmanService::set_value',
                            'enter_function', 0)

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['changed'] = True

            self.oe.dbg_log('connmanService::set_value', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.dbg_log('connmanService::set_value', 'ERROR: ('
                            + repr(e) + ')', 4)

    def dbus_config(self, category):
        try:

            value = None
            postfix = ''

            if self.struct[category]['type'] == 'Dictionary':
                value = {}
                postfix = '.Configuration'
            elif self.struct[category]['type'] == 'Array':
                value = dbus.Array([], signature=dbus.Signature('s'),
                                   variant_level=1)
                postfix = '.Configuration'

            for entry in self.struct[category]['settings']:

                setting = self.struct[category]['settings'][entry]

                if (setting['value'] != '' or hasattr(setting, 'changed'
                    )) and not 'parent' in setting or 'parent' \
                    in setting and self.struct[category]['settings'
                        ][setting['parent']['entry']]['value'] \
                    in setting['parent']['value']:

                    if setting['dbus'] == 'Array':

                        value = dbus.Array(dbus.String(setting['value'
                                ], variant_level=1).split(','),
                                signature=dbus.Signature('s'),
                                variant_level=1)
                    else:

                        if self.struct[category]['type'] == 'Boolean':

                            if setting['value'] == '1' or setting['value'] == \
                              dbus.Boolean(True, variant_level=1):
                                setting['value'] = True
                            else:
                                setting['value'] = False

                            value = getattr(dbus, setting['dbus'
                                    ])(setting['value'],
                                    variant_level=1)
                        elif self.struct[category]['type'] \
                            == 'Dictionary':

                            value[entry] = getattr(dbus, setting['dbus'
                                    ])(setting['value'],
                                    variant_level=1)
                        elif self.struct[category]['type'] == 'Array':

                            value.append(getattr(dbus, setting['dbus'
                                    ])(setting['value'],
                                    variant_level=1))

            return (category + postfix, value)
        except Exception, e:

            self.oe.dbg_log('connmanService::dbus_config', 'ERROR: ('
                            + repr(e) + ')', 4)

    def save_network(self):
        try:

            self.oe.set_busy(1)

            self.oe.dbg_log('connmanService::save_network',
                            'enter_function', 0)

            for category in [
                'AutoConnect',
                'IPv4',
                'IPv6',
                'Nameservers',
                'Timeservers',
                'Domains',
                ]:
                (category, value) = self.dbus_config(category)
                if value != None:
                    self.service.SetProperty(dbus.String(category),
                            value)

            self.oe.dbg_log('connmanService::save_network',
                            'exit_function', 0)
            self.oe.set_busy(0)

            return 'close'
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connmanService::save_network', 'ERROR: ('
                            + repr(e) + ')', 4)
            return 'close'

    def delete_network(self):
        try:

            self.oe.dbg_log('connmanService::delete_network',
                            'enter_function', 0)

            self.oe.dictModules['connman'].delete_network(None)

            self.oe.dbg_log('connmanService::delete_network',
                            'exit_function', 0)

            return 'close'
        except Exception, e:

            self.oe.dbg_log('connmanService::delete_network', 'ERROR: ('
                             + repr(e) + ')', 4)
            return 'close'

    def connect_network(self):
        try:

            self.oe.dbg_log('connmanService::connect_network',
                            'enter_function', 0)

            self.oe.dictModules['connman'].connect_network(None)

            self.oe.dbg_log('connmanService::connect_network',
                            'exit_function', 0)

            return 'close'
        except Exception, e:

            self.oe.dbg_log('connmanService::connect_network',
                            'ERROR: (' + repr(e) + ')', 4)
            return 'close'

    def disconnect_network(self):
        try:

            self.oe.dbg_log('connmanService::disconnect_network',
                            'enter_function', 0)

            self.oe.dictModules['connman'].disconnect_network(None)

            self.oe.dbg_log('connmanService::disconnect_network',
                            'exit_function', 0)

            return 'close'
        except Exception, e:

            self.oe.dbg_log('connmanService::disconnect_network',
                            'ERROR: (' + repr(e) + ')', 4)
            return 'close'


class connmanVpn(object):

    menu = {}

    def __init__(self, vpn, oeMain):
        try:

            oeMain.dbg_log('connmanVpn::__init__', 'enter_function', 0)

            self.struct = {'Provider': {
                'order': 8,
                'name': 32104,
                'listTyp': 'list',
                'type': 'Dictionary',
                'menuLoader': 'menu_loader',
                'settings': {
                    'Type': {
                        'order': 1,
                        'name': 32131,
                        'value': '',
                        'action': 'set_value',
                        'type': 'multivalue',
                        'dbus': 'String',
                        'values': ['openvpn', 'pptp'],
                        },
                    'Name': {
                        'order': 2,
                        'name': 32132,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['pptp',
                                   'openvpn']},
                        },
                    'Host': {
                        'order': 3,
                        'name': 32133,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['pptp',
                                   'openvpn']},
                        },
                    'Domain': {
                        'order': 27,
                        'name': 32134,
                        'value': 'vpn',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['pptp',
                                   'openvpn']},
                        'changed': True,
                        },
                    'PPTP.User': {
                        'order': 4,
                        'name': 32106,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        },
                    'PPTP.Password': {
                        'order': 5,
                        'name': 32107,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        },
                    'PPTP.EchoFailure': {
                        'order': 25,
                        'name': 32162,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'num',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.EchoInterval': {
                        'order': 26,
                        'name': 32163,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'num',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.RefuseEAP': {
                        'order': 13,
                        'name': 32151,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.RefusePAP': {
                        'order': 14,
                        'name': 32152,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.RefuseCHAP': {
                        'order': 15,
                        'name': 32153,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.RefuseMSCHAP': {
                        'order': 16,
                        'name': 32154,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.RefuseMSCHAP2': {
                        'order': 17,
                        'name': 32155,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.NoBSDComp': {
                        'order': 28,
                        'name': 32160,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.NoDeflate': {
                        'order': 27,
                        'name': 32164,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.RequirMPPE': {
                        'order': 20,
                        'name': 32156,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.RequirMPPE40': {
                        'order': 21,
                        'name': 32157,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.RequirMPPE128': {
                        'order': 22,
                        'name': 32158,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.RequirMPPEStateful': {
                        'order': 23,
                        'name': 32159,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'PPTP.NoVJ': {
                        'order': 24,
                        'name': 32161,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['pptp']},
                        'optional': '',
                        },
                    'OpenVPN.CACert': {
                        'order': 8,
                        'name': 32137,
                        'value': '',
                        'action': 'set_value',
                        'type': 'file',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        },
                    'OpenVPN.Cert': {
                        'order': 8,
                        'name': 32138,
                        'value': '',
                        'action': 'set_value',
                        'type': 'file',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        },
                    'OpenVPN.Key': {
                        'order': 8,
                        'name': 32139,
                        'value': '',
                        'action': 'set_value',
                        'type': 'file',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        },
                    'OpenVPN.MTU': {
                        'order': 11,
                        'name': 32165,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.NSCertType': {
                        'order': 12,
                        'name': 32166,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.Proto': {
                        'order': 13,
                        'name': 32167,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.Port': {
                        'order': 6,
                        'name': 32168,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.AuthUserPass': {
                        'order': 5,
                        'name': 32169,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.AskPass': {
                        'order': 16,
                        'name': 32170,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.AuthNoCache': {
                        'order': 17,
                        'name': 32171,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.TLSRemote': {
                        'order': 18,
                        'name': 32172,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.TLSAuth': {
                        'order': 19,
                        'name': 32173,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.TLSAuthDir': {
                        'order': 20,
                        'name': 32174,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.Auth': {
                        'order': 4,
                        'name': 32175,
                        'value': '',
                        'action': 'set_value',
                        'type': 'text',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.CompLZO': {
                        'order': 22,
                        'name': 32176,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.RemoteCertTls': {
                        'order': 23,
                        'name': 32177,
                        'value': '0',
                        'action': 'set_value',
                        'type': 'bool',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    'OpenVPN.ConfigFile': {
                        'order': 7,
                        'name': 32178,
                        'value': '',
                        'action': 'set_value',
                        'type': 'file',
                        'parent': {'entry': 'Type', 'value': ['openvpn'
                                   ]},
                        'optional': '',
                        },
                    },
                }}

            self.oe = oeMain
            self.winOeCon = oeWindows.mainWindow('mainWindow.xml',
                    self.oe.__cwd__, 'Default', oeMain=oeMain,
                    isChild=True)
            self.show_advanced_entrys = '0'
            self.oe.dictModules['connmanVpnConfig'] = self
            self.vpn_conf_dir = '/storage/.config/vpn-config/'
            self.vpn_name = vpn

            self.winOeCon.show()

            dictProperties = {
                'modul': 'connmanVpnConfig',
                'listTyp': self.oe.listObject['list'],
                'menuLoader': 'menu_loader',
                'category': 'Provider',
                }

            self.winOeCon.addMenuItem(self.struct['Provider']['name'],
                    dictProperties)

            if self.vpn_name != '__new__':
                self.load_vpn_config(vpn)

            self.winOeCon.doModal()

            del self.winOeCon
            del self.oe.dictModules['connmanVpnConfig']

            self.oe.dbg_log('connmanVpn::__init__', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connmanVpn::__init__', 'ERROR: ('
                            + repr(e) + ')', 4)

    def cancel(self):
        try:

            self.oe.dbg_log('connmanVpn::cancel', 'exit_function', 0)

            self.oe.set_busy(1)
            self.winOeCon.close()
            self.oe.set_busy(0)
            self.oe.dbg_log('connmanVpn::cancel', 'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connmanVpn::cancel', 'ERROR: (' + repr(e)
                            + ')', 4)

    def show_advanced(self, listItem=None):
        try:

            self.oe.dbg_log('connmanVpn::show_advanced', 'exit_function'
                            , 0)

            self.show_advanced_entrys = listItem.getProperty('value')

            self.oe.dbg_log('connmanVpn::show_advanced', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.dbg_log('connmanVpn::show_advanced', 'ERROR: ('
                            + repr(e) + ')', 4)

    def menu_loader(self, menuItem):
        try:

            self.oe.dbg_log('connmanVpn::menu_loader', 'enter_function'
                            , 0)

            self.winOeCon.showButton(3, 32140, 'connmanVpnConfig',
                    'save_vpn_config')

            self.winOeCon.showButton(2, 32212, 'connmanVpnConfig',
                    'cancel')

            if self.vpn_name not in ['__new__']:
                self.winOeCon.showButton(1, 32141, 'connmanVpnConfig',
                        'delete_vpn_config')

            category = menuItem.getProperty('category')
            for entry in sorted(self.struct[category]['settings'],
                                key=lambda x: \
                                self.struct[category]['settings'
                                ][x]['order']):

                if 'optional' in self.struct[category]['settings'
                        ][entry]:
                    continue

                dictProperties = {
                    'value': self.struct[category]['settings'
                            ][entry]['value'],
                    'typ': self.struct[category]['settings'
                            ][entry]['type'],
                    'entry': entry,
                    'category': category,
                    'action': 'set_value',
                    }

                if 'values' in self.struct[category]['settings'][entry]:
                    dictProperties['values'] = \
                        ','.join(self.struct[category]['settings'
                                 ][entry]['values'])

                if not 'parent' in self.struct[category]['settings'
                        ][entry]:

                    self.winOeCon.addConfigItem(self.oe._(self.struct[category]['settings'
                            ][entry]['name']), dictProperties,
                            menuItem.getProperty('listTyp'))
                else:

                    if self.struct[category]['settings'
                            ][self.struct[category]['settings'
                              ][entry]['parent']['entry']]['value'] \
                        in self.struct[category]['settings'
                            ][entry]['parent']['value']:

                        self.winOeCon.addConfigItem(self.oe._(self.struct[category]['settings'
                                ][entry]['name']), dictProperties,
                                menuItem.getProperty('listTyp'))

            if self.struct[category]['settings']['Type']['value'] != '':

                self.winOeCon.addConfigItem('Advanced',
                        {'typ': 'separator'},
                        menuItem.getProperty('listTyp'))

                dictProperties = {'value': self.show_advanced_entrys,
                                  'typ': 'bool',
                                  'action': 'show_advanced'}

                self.winOeCon.addConfigItem('Show Advanced',
                        dictProperties, menuItem.getProperty('listTyp'))

                if self.show_advanced_entrys == '1':

                    for entry in sorted(self.struct[category]['settings'
                            ], key=lambda x: \
                            self.struct[category]['settings'][x]['order'
                            ]):

                        if not 'optional' \
                            in self.struct[category]['settings'][entry]:
                            continue

                        dictProperties = {
                            'value': self.struct[category]['settings'
                                    ][entry]['value'],
                            'typ': self.struct[category]['settings'
                                    ][entry]['type'],
                            'entry': entry,
                            'category': category,
                            'action': 'set_value',
                            }

                        if 'values' in self.struct[category]['settings'
                                ][entry]:
                            dictProperties['values'] = \
                                ','.join(self.struct[category]['settings'
                                    ][entry]['values'])

                        if not 'parent' \
                            in self.struct[category]['settings'][entry]:

                            self.winOeCon.addConfigItem(self.oe._(self.struct[category]['settings'
                                    ][entry]['name']), dictProperties,
                                    menuItem.getProperty('listTyp'))
                        else:

                            if self.struct[category]['settings'
                                    ][self.struct[category]['settings'
                                    ][entry]['parent']['entry']]['value'
                                    ] \
                                in self.struct[category]['settings'
                                    ][entry]['parent']['value']:

                                self.winOeCon.addConfigItem(self.oe._(self.struct[category]['settings'
                                        ][entry]['name']),
                                        dictProperties,
                                        menuItem.getProperty('listTyp'))

            self.oe.dbg_log('connmanVpn::menu_loader', 'exit_function',
                            0)
        except Exception, e:

            self.oe.dbg_log('connmanVpn::menu_loader', 'ERROR: ('
                            + repr(e) + ')', 4)

    def set_value(self, listItem):
        try:

            self.oe.dbg_log('connmanVpn::set_value', 'enter_function',
                            0)

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['changed'] = True

            self.oe.dbg_log('connmanVpn::set_value', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connmanVpn::set_value', 'ERROR: ('
                            + repr(e) + ')', 4)

    def load_vpn_config(self, vpn_name):

        try:

            self.oe.dbg_log('connmanVpn::load_vpn_config',
                            'enter_function', 0)

            self.vpn_conf = ConfigParser.RawConfigParser()
            self.vpn_conf.optionxform = str

            vpn_file_name = '%s%s.config' % (self.vpn_conf_dir,
                    vpn_name)
            if os.path.exists(vpn_file_name):
                self.vpn_conf.readfp(open(vpn_file_name))

            for section in self.vpn_conf.sections():
                if 'provider_' in section:
                    if self.vpn_conf.has_option(section, 'Name'):
                        if self.vpn_conf.get(section, 'Name') \
                            == vpn_name:
                            for option in \
                                self.vpn_conf.options(section):
                                if option in self.struct['Provider'
                                        ]['settings']:
                                    self.struct['Provider']['settings'
        ][option]['value'] = self.vpn_conf.get(section, option)
                                    self.struct['Provider']['settings'
        ][option]['changed'] = True

            self.oe.dbg_log('connmanVpn::load_vpn_config',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connmanVpn::load_vpn_config', 'ERROR: ('
                            + repr(e) + ')', 4)

    def save_vpn_config(self):
        try:

            self.oe.dbg_log('connmanVpn::save_vpn_config',
                            'enter_function', 0)

            self.oe.set_busy(1)

            for entry in sorted(self.struct['Provider']['settings'],
                                key=lambda x: self.struct['Provider'
                                ]['settings'][x]['order']):
                if 'parent' in self.struct['Provider']['settings'
                        ][entry]:
                    if self.struct['Provider']['settings']['Type'
                            ]['value'] in self.struct['Provider'
                            ]['settings'][entry]['parent']['value'] \
                        and not 'optional' in self.struct['Provider'
                            ]['settings'][entry] \
                        and self.struct['Provider']['settings'
                            ][entry]['value'] == '':

                        dialog = xbmcgui.Dialog()
                        self.oe.set_busy(0)
                        dialog.ok('OpenELEC VPN', self.oe._(32378))
                        self.oe.dbg_log('connmanVpn::save_vpn_config',
                                'exit_function (incomplete)', 0)
                        return

            self.vpn_conf = ConfigParser.ConfigParser()
            self.vpn_conf.optionxform = str

            self.vpn_conf.add_section('global')
            self.vpn_conf.set('global', 'Name', self.struct['Provider'
                              ]['settings']['Name']['value'])

            section = 'provider_%s' % self.struct['Provider']['settings'
                    ]['Type']['value']
            self.vpn_conf.add_section(section)

            for entry in sorted(self.struct['Provider']['settings'],
                                key=lambda x: self.struct['Provider'
                                ]['settings'][x]['order']):
                if 'changed' in self.struct['Provider']['settings'
                        ][entry]:
                    self.vpn_conf.set(section, entry,
                            self.struct['Provider']['settings'
                            ][entry]['value'])

            if os.path.exists('%s%s.config' % (self.vpn_conf_dir,
                              self.vpn_name)):
                os.remove('%s%s.config' % (self.vpn_conf_dir,
                          self.vpn_name))

            vpn_file_name = '%s%s.config' % (self.vpn_conf_dir,
                    self.struct['Provider']['settings']['Name']['value'
                    ])
            with open(vpn_file_name, 'wb') as configfile:
                self.vpn_conf.write(configfile)

            self.oe.dbg_log('connmanVpn::save_vpn_config',
                            'exit_function', 0)

            self.oe.set_busy(0)

            return 'close'
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connmanVpn::save_vpn_config', 'ERROR: ('
                            + repr(e) + ')', 4)

    def delete_vpn_config(self):
        try:

            self.oe.dbg_log('connmanVpn::delete_vpn_config',
                            'enter_function', 0)

            self.oe.dictModules['connman'].delete_network(None)

            self.oe.dbg_log('connmanVpn::delete_vpn_config',
                            'exit_function', 0)

            return 'close'
        except Exception, e:

            self.oe.dbg_log('connmanService::delete_network', 'ERROR: ('
                             + repr(e) + ')', 4)
            return 'close'


class connman:

    oe = None
    menu = {'2': {
        'name': 32100,
        'menuLoader': 'menu_connections',
        'listTyp': 'netlist',
        'InfoText': 702,
        }, '3': {
        'name': 32101,
        'menuLoader': 'menu_loader',
        'listTyp': 'list',
        'InfoText': 701,
        }}

    def __init__(self, oeMain):
        try:

            oeMain.dbg_log('connman::__init__', 'enter_function', 0)

            self.listItems = {}

            self.struct = {
                '/net/connman/technology/wifi': {
                    'order': 1,
                    'name': 32102,
                    'dbus': 'Dictionary',
                    'settings': {
                        'Powered': {
                            'order': 1,
                            'name': 32105,
                            'value': '',
                            'action': 'set_technologie',
                            'type': 'bool',
                            'dbus': 'Boolean',
                            'InfoText': 726,
                            },
                        'Tethering': {
                            'order': 2,
                            'name': 32108,
                            'value': '',
                            'action': 'set_technologie',
                            'type': 'bool',
                            'dbus': 'Boolean',
                            'parent': {'entry': 'Powered', 'value': ['1'
                                    ]},
                            'InfoText': 727,
                            },
                        'TetheringIdentifier': {
                            'order': 3,
                            'name': 32198,
                            'value': 'OpenELEC-AP',
                            'action': 'set_technologie',
                            'type': 'text',
                            'dbus': 'String',
                            'parent': {'entry': 'Tethering',
                                    'value': ['1']},
                            'validate': '^([a-zA-Z0-9](?:[a-zA-Z0-9-\.]*[a-zA-Z0-9]))$',
                            'InfoText': 728,
                            },
                        'TetheringPassphrase': {
                            'order': 4,
                            'name': 32107,
                            'value': 'openelec',
                            'action': 'set_technologie',
                            'type': 'text',
                            'dbus': 'String',
                            'parent': {'entry': 'Tethering',
                                    'value': ['1']},
                            'validate': '^[\\x00-\\x7F]{8,64}$',
                            'InfoText': 729,
                            },
                        },
                    },
                '/net/connman/technology/ethernet': {
                    'order': 2,
                    'name': 32103,
                    'dbus': 'Dictionary',
                    'settings': {'Powered': {
                        'order': 1,
                        'name': 32105,
                        'value': '',
                        'action': 'set_technologie',
                        'type': 'bool',
                        'dbus': 'Boolean',
                        'InfoText': 730,
                        }},
                    },
                'vpn': {
                    'order': 3,
                    'name': 32321,
                    'dbus': 'Dictionary',
                    'settings': {'add': {
                        'order': 1,
                        'name': 32322,
                        'action': 'add_vpn',
                        'type': 'button',
                        'InfoText': 731,
                        }},
                    },
                'Timeservers': {
                    'order': 4,
                    'name': 32123,
                    'dbus': 'Array',
                    'settings': {'0': {
                        'order': 1,
                        'name': 32124,
                        'value': '',
                        'action': 'set_timeservers',
                        'type': 'text',
                        'dbus': 'String',
                        'validate': '^([a-zA-Z0-9](?:[a-zA-Z0-9-\.]*[a-zA-Z0-9]))$',
                        'InfoText': 732,
                        }, '1': {
                        'order': 2,
                        'name': 32125,
                        'value': '',
                        'action': 'set_timeservers',
                        'type': 'text',
                        'dbus': 'String',
                        'validate': '^([a-zA-Z0-9](?:[a-zA-Z0-9-\.]*[a-zA-Z0-9]))$',
                        'InfoText': 733,
                        }, '2': {
                        'order': 3,
                        'name': 32126,
                        'value': '',
                        'action': 'set_timeservers',
                        'type': 'text',
                        'dbus': 'String',
                        'validate': '^([a-zA-Z0-9](?:[a-zA-Z0-9-\.]*[a-zA-Z0-9]))$',
                        'InfoText': 734,
                        }},
                    },
                'mounts': {'order': 5, 'name': 32348,
                           'settings': {'add': {
                    'order': 1,
                    'name': 32349,
                    'value': '',
                    'action': 'edit_mount',
                    'type': 'button',
                    'InfoText': 735,
                    }}},
                'advanced': {'order': 6, 'name': 32368,
                             'settings': {'wait_for_network': {
                    'order': 1,
                    'name': 32369,
                    'value': '0',
                    'action': 'set_network_wait',
                    'type': 'bool',
                    'InfoText': 736,
                    }, 'wait_for_network_time': {
                    'order': 2,
                    'name': 32370,
                    'value': '10',
                    'action': 'set_network_wait',
                    'type': 'num',
                    'parent': {'entry': 'wait_for_network',
                               'value': ['1']},
                    'InfoText': 737,
                    }}},
                }

            self.wait_conf_file = \
                '/storage/.cache/openelec/network_wait'

            self.busy = 0
            self.oe = oeMain
            self.oe.dbg_log('connman::__init__', 'exit_function', 0)
            self.vpn_conf_dir = '/storage/.config/vpn-config/'
        except Exception, e:

            self.oe.dbg_log('connman::__init__', 'ERROR: (' + repr(e)
                            + ')', 4)

    def clear_list(self):
        try:

            remove = [entry for entry in self.listItems]
            for entry in remove:
                self.listItems[entry] = None
                del self.listItems[entry]
        except Exception, e:

            self.oe.dbg_log('connman::clear_list', 'ERROR: (' + repr(e)
                            + ')', 4)

    def do_init(self):
        try:

            self.oe.dbg_log('connman::do_init', 'enter_function', 0)

            self.dbusSystemBus = self.oe.dbusSystemBus
            self.dbusConnmanManager = \
                dbus.Interface(self.dbusSystemBus.get_object('net.connman'
                               , '/'), 'net.connman.Manager')

            self.load_values()

            self.dbusMonitor = monitorLoop(self.oe, self.dbusSystemBus)
            self.dbusMonitor.start()

            self.oe.dbg_log('connman::do_init', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::do_init', 'ERROR: (' + repr(e)
                            + ')', 4)

    def exit(self):
        try:

            self.oe.dbg_log('connman::exit', 'enter_function', 0)

            self.dbusMonitor.exit()

            self.clear_list()

            if hasattr(self, 'dbusSystemBus'):
                del self.dbusSystemBus

            if hasattr(self, 'dbusConnmanManager'):
                self.dbusConnmanManager = None
                del self.dbusConnmanManager

            if hasattr(self, 'dbusMonitor'):
                self.dbusMonitor = None
                del self.dbusMonitor

            self.oe.dbg_log('connman::exit', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::exit', 'ERROR: (' + repr(e) + ')'
                            , 4)

    def load_values(self):
        try:

            self.oe.dbg_log('connman::load_values', 'enter_function', 0)

      
            # Network Wait
            self.struct['advanced']['settings']['wait_for_network'
                    ]['value'] = '0'
            self.struct['advanced']['settings']['wait_for_network_time'
                    ]['value'] = '10'

            if os.path.exists(self.wait_conf_file):
                wait_file = open(self.wait_conf_file, 'r')
                for line in wait_file:
                    if 'WAIT_NETWORK=' in line:
                        if line.split('=')[-1].lower().strip() \
                            == 'true':
                            self.struct['advanced']['settings'
                                    ]['wait_for_network']['value'] = '1'
                        else:
                            self.struct['advanced']['settings'
                                    ]['wait_for_network']['value'] = '0'

                    if 'WAIT_NETWORK_TIME=' in line:
                        self.struct['advanced']['settings'
                                ]['wait_for_network_time']['value'] = \
                            line.split('=')[-1].lower().strip()

                wait_file.close()

            self.oe.dbg_log('connman::load_values', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::load_values', 'ERROR: ('
                            + repr(e) + ')')

    def menu_connections(
        self,
        focusItem,
        services={},
        removed={},
        force=False,
        ):

        try:

            self.oe.dbg_log('connman::menu_connections',
                            'enter_function', 0)

            self.oe.set_busy(1)
            self.oe.dbg_log('connman::menu_connections__busy__',
                            str(self.oe.__busy__), 0)

            # type 1=int, 2=string, 3=array
            properties = {
                0: {'flag': 0, 'type': 2, 'values': ['State']},
                1: {'flag': 0, 'type': 1, 'values': ['Strength']},
                2: {'flag': 0, 'type': 1, 'values': ['Favorite']},
                3: {'flag': 0, 'type': 3, 'values': ['Security']},
                4: {'flag': 0, 'type': 2, 'values': ['IPv4', 'Method'
                    ]},
                5: {'flag': 0, 'type': 2, 'values': ['IPv4', 'Address'
                    ]},
                6: {'flag': 0, 'type': 2,
                    'values': ['IPv4.Configuration', 'Method']},
                7: {'flag': 0, 'type': 2,
                    'values': ['IPv4.Configuration', 'Address']},
                8: {'flag': 0, 'type': 2, 'values': ['Ethernet',
                    'Interface']},
                }

            self.dbusServices = self.dbusConnmanManager.GetServices()

            rebuildList = 0
            if len(self.dbusServices) != len(self.listItems):
                rebuildList = 1
                self.oe.winOeMain.getControl(int(self.oe.listObject['netlist'
                        ])).reset()
                self.clear_list()
            else:

                for (dbusServicePath, dbusServiceValues) in \
                    self.dbusServices:
                    if dbusServicePath not in self.listItems:
                        rebuildList = 1
                        self.oe.winOeMain.getControl(int(self.oe.listObject['netlist'
                                ])).reset()
                        self.clear_list()
                        break

            for (dbusServicePath, dbusServiceProperties) in \
                self.dbusServices:

                dictProperties = {}

                if rebuildList == 1:
                    if 'Name' in dbusServiceProperties:
                        apName = dbusServiceProperties['Name']
                    else:
                        if 'Security' in dbusServiceProperties:
                            apName = self.oe._(32208) + ' (' \
                                + str(dbusServiceProperties['Security'
                                    ][0]) + ')'
                        else:
                            apName = ''

                    if apName != '':
                        dictProperties['entry'] = dbusServicePath
                        dictProperties['modul'] = \
                            self.__class__.__name__

                        if 'Type' in dbusServiceProperties:
                            dictProperties['netType'] = \
                                dbusServiceProperties['Type']
                            dictProperties['action'] = \
                                'open_context_menu'

                for prop in properties:
                    result = dbusServiceProperties
                    for value in properties[prop]['values']:
                        if value in result:
                            result = result[value]
                            properties[prop]['flag'] = 1
                        else:
                            properties[prop]['flag'] = 0

                    if properties[prop]['flag'] == 1:
                        if properties[prop]['type'] == 1:
                            result = str(int(result))
                        if properties[prop]['type'] == 2:
                            result = str(result)
                        if properties[prop]['type'] == 3:
                            result = str(len(result))

                        if rebuildList == 1:
                            dictProperties[value] = result
                        else:
                            if self.listItems[dbusServicePath] != None:
                                self.listItems[dbusServicePath].setProperty(value,
                                        result)

                if rebuildList == 1:
                    self.listItems[dbusServicePath] = \
                        self.oe.winOeMain.addConfigItem(apName,
                            dictProperties, self.oe.listObject['netlist'
                            ])

            self.oe.set_busy(0)

            self.oe.dbg_log('connman::menu_connections', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::menu_connections', 'ERROR: ('
                            + repr(e) + ')', 4)

    def menu_loader(self, menuItem=None):
        try:

            self.oe.dbg_log('connman::menu_loader', 'enter_function0',
                            0)

            self.oe.set_busy(1)

            if menuItem == None:
                menuItem = \
                    self.oe.winOeMain.getControl(self.oe.winOeMain.guiMenList).getSelectedItem()

            self.technologie_properties = \
                self.dbusConnmanManager.GetTechnologies()

            self.clock = \
                dbus.Interface(self.dbusSystemBus.get_object('net.connman'
                               , '/'), 'net.connman.Clock')
            self.clock_properties = self.clock.GetProperties()

            # Wifi and Ethernet
            for (path, technologie) in self.technologie_properties:

                if path in self.struct:
                    self.oe.winOeMain.addConfigItem(self.oe._(self.struct[path]['name'
                            ]), {'typ': 'separator'},
                            menuItem.getProperty('listTyp'))

                if path in self.struct:
                    for entry in sorted(self.struct[path]['settings'],
                            key=lambda x: self.struct[path]['settings'
                            ][x]['order']):
                        if entry in technologie:
                            if not 'changed' \
                                in self.struct[path]['settings'][entry]:
                                self.struct[path]['settings'
                                        ][entry]['value'] = \
                                    str(technologie[entry])

                        dictProperties = {
                            'value': self.struct[path]['settings'
                                    ][entry]['value'],
                            'typ': self.struct[path]['settings'
                                    ][entry]['type'],
                            'entry': entry,
                            'category': path,
                            'action': self.struct[path]['settings'
                                    ][entry]['action'],
                            }

                        if 'InfoText' in self.struct[path]['settings'
                                ][entry]:
                            dictProperties['InfoText'] = \
                                self.oe._(self.struct[path]['settings'
                                    ][entry]['InfoText'])

                        if 'validate' in self.struct[path]['settings'
                                ][entry]:
                            dictProperties['validate'] = \
                                self.struct[path]['settings'
                                    ][entry]['validate']

                        if 'values' in self.struct[path]['settings'
                                ][entry]:
                            dictProperties['values'] = \
                                ','.join(self.struct[path]['settings'
                                    ][entry]['values'])

                        if not 'parent' in self.struct[path]['settings'
                                ][entry]:

                            self.oe.winOeMain.addConfigItem(self.oe._(self.struct[path]['settings'
                                    ][entry]['name']), dictProperties,
                                    menuItem.getProperty('listTyp'))
                        else:

                            if self.struct[path]['settings'
                                    ][self.struct[path]['settings'
                                    ][entry]['parent']['entry']]['value'
                                    ] in self.struct[path]['settings'
                                    ][entry]['parent']['value']:

                                self.oe.winOeMain.addConfigItem(self.oe._(self.struct[path]['settings'
                                        ][entry]['name']),
                                        dictProperties,
                                        menuItem.getProperty('listTyp'))

            # Virtual Private Network
            self.oe.winOeMain.addConfigItem(self.oe._(self.struct['vpn'
                    ]['name']), {'typ': 'separator'},
                    menuItem.getProperty('listTyp'))

            self.oe.winOeMain.addConfigItem(self.oe._(self.struct['vpn'
                    ]['settings']['add']['name']), {'typ': 'button',
                    'action': self.struct['vpn']['settings']['add'
                    ]['action'], 'InfoText': self.oe._(self.struct['vpn'
                    ]['settings']['add']['InfoText'])},
                    menuItem.getProperty('listTyp'))

            # Timeservers
            self.oe.winOeMain.addConfigItem(self.oe._(self.struct['Timeservers'
                    ]['name']), {'typ': 'separator'},
                    menuItem.getProperty('listTyp'))

            if 'Timeservers' in self.clock_properties:
                for setting in sorted(self.struct['Timeservers'
                        ]['settings']):
                    if int(setting) \
                        < len(self.clock_properties['Timeservers']):
                        if not 'changed' in self.struct['Timeservers'
                                ]['settings'][setting]:
                            self.struct['Timeservers']['settings'
                                    ][setting]['value'] = \
                                self.clock_properties['Timeservers'
                                    ][int(setting)]

                    dictProperties = {
                        'value': self.struct['Timeservers']['settings'
                                ][str(setting)]['value'],
                        'typ': self.struct['Timeservers']['settings'
                                ][str(setting)]['type'],
                        'entry': str(setting),
                        'category': 'Timeservers',
                        'action': self.struct['Timeservers']['settings'
                                ][str(setting)]['action'],
                        }

                    if 'InfoText' in self.struct['Timeservers'
                            ]['settings'][setting]:
                        dictProperties['InfoText'] = \
                            self.oe._(self.struct['Timeservers'
                                ]['settings'][setting]['InfoText'])

                    if 'validate' in self.struct['Timeservers'
                            ]['settings'][str(setting)]:
                        dictProperties['validate'] = \
                            self.struct['Timeservers']['settings'
                                ][str(setting)]['validate']

                    self.oe.winOeMain.addConfigItem(self.oe._(self.struct['Timeservers'
                            ]['settings'][str(setting)]['name']),
                            dictProperties,
                            menuItem.getProperty('listTyp'))

            # Mounts
            self.oe.winOeMain.addConfigItem(self.oe._(self.struct['mounts'
                    ]['name']), {'typ': 'separator'},
                    menuItem.getProperty('listTyp'))

            self.oe.winOeMain.addConfigItem(self.oe._(self.struct['mounts'
                    ]['settings']['add']['name']), {
                'typ': self.struct['mounts']['settings']['add']['type'
                        ],
                'action': self.struct['mounts']['settings']['add'
                        ]['action'],
                'entry': 'new_mount',
                'InfoText': self.oe._(self.struct['mounts']['settings'
                        ]['add']['InfoText']),
                }, menuItem.getProperty('listTyp'))

            mount_dict = self.oe.read_node('mounts')
            if 'mounts' in mount_dict:
                for mount in mount_dict['mounts']:

                    dictProperties = {
                        'typ': 'button',
                        'entry': mount,
                        'category': 'mounts',
                        'action': 'edit_mount',
                        }

                    self.oe.winOeMain.addConfigItem(mount_dict['mounts'
                            ][mount]['mountpoint'], dictProperties,
                            menuItem.getProperty('listTyp'))

            # Network Wait
            self.oe.winOeMain.addConfigItem(self.oe._(self.struct['advanced'
                    ]['name']), {'typ': 'separator'},
                    menuItem.getProperty('listTyp'))

            self.oe.winOeMain.addConfigItem(self.oe._(self.struct['advanced'
                    ]['settings']['wait_for_network']['name']), {
                'entry': 'wait_for_network',
                'category': 'advanced',
                'typ': self.struct['advanced']['settings'
                        ]['wait_for_network']['type'],
                'action': self.struct['advanced']['settings'
                        ]['wait_for_network']['action'],
                'value': self.struct['advanced']['settings'
                        ]['wait_for_network']['value'],
                'InfoText': self.oe._(self.struct['advanced']['settings'
                        ]['wait_for_network']['InfoText']),
                }, menuItem.getProperty('listTyp'))

            if self.struct['advanced']['settings']['wait_for_network'
                    ]['value'] in self.struct['advanced']['settings'
                    ]['wait_for_network_time']['parent']['value']:

                self.oe.winOeMain.addConfigItem(self.oe._(self.struct['advanced'
                        ]['settings']['wait_for_network_time']['name'
                        ]), {
                    'entry': 'wait_for_network_time',
                    'category': 'advanced',
                    'typ': self.struct['advanced']['settings'
                            ]['wait_for_network_time']['type'],
                    'action': self.struct['advanced']['settings'
                            ]['wait_for_network_time']['action'],
                    'value': self.struct['advanced']['settings'
                            ]['wait_for_network_time']['value'],
                    }, menuItem.getProperty('listTyp'))

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::menu_loader', 'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::menu_loader', 'ERROR: ('
                            + repr(e) + ')', 4)

    def open_context_menu(self, listItem):
        try:

            self.oe.dbg_log('connman::open_context_menu',
                            'enter_function', 0)

            values = {}

            if listItem is None:
                listItem = \
                    self.oe.winOeMain.getControl(self.oe.listObject['netlist'
                        ]).getSelectedItem()

            if listItem is None:
                self.oe.dbg_log('connman::open_context_menu',
                                'exit_function (listItem=None)', 0)
                return

            if listItem.getProperty('State') in ['ready', 'online']:
                values[1] = {'text': self.oe._(32143),
                             'action': 'disconnect_network'}
            else:
                values[1] = {'text': self.oe._(32144),
                             'action': 'connect_network'}

            if listItem.getProperty('Favorite') == '1' \
                or listItem.getProperty('netType') == 'vpn':
                values[2] = {'text': self.oe._(32150),
                             'action': 'configure_network'}

            if listItem.getProperty('Favorite') == '1' \
                and listItem.getProperty('netType') == 'wifi' \
                or listItem.getProperty('netType') == 'vpn':
                values[3] = {'text': self.oe._(32141),
                             'action': 'delete_network'}

            if hasattr(self, 'technologie_properties'):
                for (path, technologie) in self.technologie_properties:
                    if path == '/net/connman/technology/wifi':
                        values[4] = {'text': self.oe._(32142),
                                'action': 'refresh_network'}
                        break

            context_menu = oeWindows.contextWindow('contexMenu.xml',
                    self.oe.__cwd__, 'Default', oeMain=self.oe)  #
            context_menu.options = values
            context_menu.doModal()

            if context_menu.result != '':
                getattr(self, context_menu.result)(listItem)

            del context_menu

            self.oe.dbg_log('connman::open_context_menu',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::open_context_menu', 'ERROR: ('
                            + repr(e) + ')', 4)

    def set_timeservers(self, **kwargs):
        try:

            self.oe.set_busy(1)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])

            self.oe.dbg_log('connman::set_timeservers', 'enter_function'
                            , 0)

            self.clock = \
                dbus.Interface(self.dbusSystemBus.get_object('net.connman'
                               , '/'), 'net.connman.Clock')

            timeservers = []

            for setting in sorted(self.struct['Timeservers']['settings'
                                  ]):
                timeservers.append(self.struct['Timeservers']['settings'
                                   ][setting]['value'])

            self.clock.SetProperty(dbus.String('Timeservers'),
                                   timeservers)

            self.oe.dbg_log('connman::set_timeservers', 'exit_function'
                            , 0)

            self.oe.set_busy(0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::set_timeservers', 'ERROR: ('
                            + repr(e) + ')', 4)

    def set_value(self, listItem=None):
        try:

            self.oe.dbg_log('connman::set_value', 'enter_function', 0)

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['changed'] = True

            self.oe.dbg_log('connman::set_value', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::set_value', 'ERROR: (' + repr(e)
                            + ')', 4)

    def set_technologie(self, **kwargs):
        try:

            self.oe.dbg_log('connman::set_technologies',
                            'enter_function', 0)

            self.oe.set_busy(1)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])

            self.technologie_properties = \
                self.dbusConnmanManager.GetTechnologies()

            techPath = '/net/connman/technology/wifi'
            for (path, technologie) in self.technologie_properties:
                if path == techPath:
                    for setting in self.struct[techPath]['settings']:
                        settings = self.struct[techPath]['settings']
                        self.Technology = \
                            dbus.Interface(self.dbusSystemBus.get_object('net.connman'
                                          , techPath), 'net.connman.Technology'
                                          )

                        if settings['Powered']['value'] == '1':
                            if technologie['Powered'] != True:
                                self.Technology.SetProperty('Powered',
                                        dbus.Boolean(True, variant_level=1))

                            if settings['Tethering']['value'] == '1' \
                                and dbus.String(settings['TetheringIdentifier'
                                    ]['value']) != '' \
                                and dbus.String(settings['TetheringPassphrase'
                                    ]['value']) != '':

                                time.sleep(5)
                                self.Technology.SetProperty('TetheringIdentifier'
                                        ,
                                        dbus.String(settings['TetheringIdentifier'
                                        ]['value'], variant_level=1))
                                self.Technology.SetProperty('TetheringPassphrase'
                                        ,
                                        dbus.String(settings['TetheringPassphrase'
                                        ]['value'], variant_level=1))

                                if technologie['Tethering'] != True:
                                    self.Technology.SetProperty('Tethering',
                                            dbus.Boolean(True, variant_level=1))
                            else:
                                if technologie['Tethering'] != False:
                                    self.Technology.SetProperty('Tethering',
                                            dbus.Boolean(False,
                                            variant_level=1))
                        else:

                            if technologie['Powered'] != False:
                                self.Technology.SetProperty('Powered',
                                        dbus.Boolean(False, variant_level=1))

                        break

            techPath = '/net/connman/technology/ethernet'
            for (path, technologie) in self.technologie_properties:
                if path == techPath:
                    for setting in self.struct[techPath]['settings']:
                        settings = self.struct[techPath]['settings']
                        self.Technology = \
                            dbus.Interface(self.dbusSystemBus.get_object('net.connman'
                                          , techPath), 'net.connman.Technology'
                                          )

                        if settings['Powered']['value'] == '1':
                            if technologie['Powered'] != True:
                                self.Technology.SetProperty('Powered',
                                        dbus.Boolean(True, variant_level=1))
                        else:
                            if technologie['Powered'] != False:
                                self.Technology.SetProperty('Powered',
                                        dbus.Boolean(False, variant_level=1))

                        break

            self.technologie_properties = None
            
            self.menu_loader(None)
            self.oe.set_busy(0)

            self.oe.dbg_log('connman::set_technologies', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::set_technologies', 'ERROR: ('
                            + repr(e) + ')', 4)

    def configure_network(self, listItem=None):
        try:

            self.oe.dbg_log('connman::configure_network',
                            'enter_function', 0)

            if listItem == None:
                listItem = \
                    self.oe.winOeMain.getControl(self.oe.listObject['netlist'
                        ]).getSelectedItem()

            if not listItem.getProperty('netType') == 'vpn':
                self.configureService = \
                    connmanService(listItem.getProperty('entry'),
                                   self.oe)
                del self.configureService
            else:

                self.configure_vpn = connmanVpn(listItem.getLabel(),
                        self.oe)
                del self.configure_vpn

                pid = self.oe.execute('pidof %s' % 'connman-vpnd'
                        ).split(' ')
                if len(pid) > 0:
                    os.system('connman-vpnd -n &')

                time.sleep(1)

            self.menu_connections(None)

            self.oe.dbg_log('connman::configure_network',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::configure_network', 'ERROR: ('
                            + repr(e) + ')', 4)

    def connect_network(self, listItem=None):
        try:

            self.oe.dbg_log('connman::connect_network', 'enter_function'
                            , 0)

            self.oe.set_busy(1)

            if listItem == None:
                listItem = \
                    self.oe.winOeMain.getControl(self.oe.listObject['netlist'
                        ]).getSelectedItem()

            service_object = self.dbusSystemBus.get_object('net.connman'
                    , listItem.getProperty('entry'))
            dbus.Interface(service_object, 'net.connman.Service'
                           ).Connect(reply_handler=self.connect_reply_handler,
                    error_handler=self.dbus_error_handler)

            service_object = None
            del service_object

            self.oe.dbg_log('connman::connect_network', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::connect_network', 'ERROR: ('
                            + repr(e) + ')', 4)

    def connect_reply_handler(self):
        try:

            self.oe.dbg_log('connman::connect_reply_handler',
                            'enter_function', 0)

            self.oe.set_busy(0)
            self.menu_connections(None)

            self.oe.dbg_log('connman::connect_reply_handler',
                            'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::connect_reply_handler', 'ERROR: ('
                             + repr(e) + ')', 4)

    def dbus_error_handler(self, error):
        try:

            self.oe.dbg_log('connman::dbus_error_handler',
                            'enter_function', 0)

            self.oe.set_busy(0)

            err_name = error.get_dbus_name()

            if 'InProgress' in err_name:
                self.disconnect_network()
                self.connect_network()
            else:
                xbmc.executebuiltin('Notification(Network Error, '
                                    + err_name.split('.')[-1] + ')')
                self.oe.dbg_log('connman::dbus_error_handler',
                                'ERROR: (' + err_name + ')', 4)

            self.oe.dbg_log('connman::dbus_error_handler',
                            'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::dbus_error_handler', 'ERROR: ('
                            + repr(e) + ')', 4)

    def disconnect_network(self, listItem=None):
        try:

            self.oe.dbg_log('connman::disconnect_network',
                            'enter_function', 0)

            self.oe.set_busy(1)

            if listItem == None:
                listItem = \
                    self.oe.winOeMain.getControl(self.oe.listObject['netlist'
                        ]).getSelectedItem()

            service_object = self.dbusSystemBus.get_object('net.connman'
                    , listItem.getProperty('entry'))
            dbus.Interface(service_object, 'net.connman.Service'
                           ).Disconnect()

            service_object = None
            del service_object
            
            self.oe.set_busy(0)

            self.oe.dbg_log('connman::disconnect_network',
                            'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::disconnect_network', 'ERROR: ('
                            + repr(e) + ')', 4)

    def delete_network(self, listItem=None):
        try:

            self.oe.dbg_log('connman::delete_network', 'enter_function'
                            , 0)

            self.oe.set_busy(1)

            if listItem == None:
                listItem = \
                    self.oe.winOeMain.getControl(self.oe.listObject['netlist'
                        ]).getSelectedItem()

            service_path = listItem.getProperty('entry')
            network_type = listItem.getProperty('netType')

            if network_type == 'vpn':
                
                if listItem.getProperty('State') in ['ready', 'online']:
                    self.disconnect_network(listItem)

                if os.path.exists('%s%s.config' % (self.vpn_conf_dir,
                                  listItem.getLabel())):
                    os.remove('%s%s.config' % (self.vpn_conf_dir,
                              listItem.getLabel()))
            else:

                service_object = \
                    self.dbusSystemBus.get_object('net.connman',
                        service_path)
                dbus.Interface(service_object, 'net.connman.Service'
                               ).Remove()
                
                service_object = None
                del service_object

            self.oe.set_busy(0)

            self.oe.dbg_log('connman::delete_network', 'exit_function',
                            0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::delete_network', 'ERROR: ('
                            + repr(e) + ')', 4)

    def refresh_network(self, listItem=None):
        try:

            self.oe.dbg_log('connman::refresh_network', 'enter_function'
                            , 0)

            self.oe.set_busy(1)
            wifi = self.dbusSystemBus.get_object('net.connman',
                    '/net/connman/technology/wifi')
            dbus.Interface(wifi, 'net.connman.Technology').Scan()

            wifi = None
            del wifi
            
            self.oe.set_busy(0)
            self.menu_connections(None)

            self.oe.dbg_log('connman::refresh_network', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::refresh_network', 'ERROR: ('
                            + repr(e) + ')', 4)

    def add_vpn(self, listItem=None):
        try:

            self.oe.dbg_log('connman::add_vpn', 'enter_function', 0)

            self.configure_vpn = connmanVpn('__new__', self.oe)
            self.configure_vpn = None
            del self.configure_vpn

            try:
                self.dbusSystemBus.activate_name_owner('net.connman.vpn'
                        )
            except:
                pass

            self.oe.dbg_log('connman::add_vpn', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::add_vpn', 'ERROR: (' + repr(e)
                            + ')', 4)

    def get_service_path(self):
        try:

            self.oe.dbg_log('connman::get_service_path',
                            'enter_function', 0)

            if hasattr(self, 'winOeCon'):
                return self.winOeCon.service_path
            else:
                listItem = \
                    self.oe.winOeMain.getControl(self.oe.listObject['netlist'
                        ]).getSelectedItem()
                return listItem.getProperty('entry')

            self.oe.dbg_log('connman::get_service_path', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.dbg_log('connman::get_service_path', 'ERROR: ('
                            + repr(e) + ')', 4)

    def edit_mount(self, listItem=None):
        try:

            self.oe.dbg_log('connman::add_mount', 'enter_function', 0)

            self.configureMount = \
                networkMount(listItem.getProperty('entry'), self.oe)
            del self.configureMount

            self.oe.dbg_log('connman::add_mount', 'enter_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::add_mount', 'ERROR: (' + repr(e)
                            + ')')

    def mount_drives(self):
        try:

            self.oe.dbg_log('connman::mount_drives', 'enter_function',
                            0)

            self.oe.set_busy(1)

            mount_dict = self.oe.read_node('mounts')
            if 'mounts' in mount_dict:
                for mount in mount_dict['mounts']:
                    self.mount_drive(mount_dict['mounts'][mount])

            self.oe.set_busy(0)

            self.oe.dbg_log('connman::mount_drives', 'exit_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::mount_drives', 'ERROR: ('
                            + repr(e) + ')')

    def mount_drive(self, mount_info):
        try:

            self.oe.set_busy(1)

            self.oe.dbg_log('connman::mount_drive', 'enter_function', 0)

            if mount_info['type'] == 'cifs':

                if os.path.exists('/media/' + mount_info['mountpoint']):
                    if os.listdir('/media/' + mount_info['mountpoint']) \
                        != []:
                        mount_info['mountpoint'] = '_' \
                            + mount_info['mountpoint']

                mount_info['mountpoint'] = '/media/' \
                    + mount_info['mountpoint']

                if not os.path.exists(mount_info['mountpoint']):
                    os.makedirs(mount_info['mountpoint'])

                self.oe.dbg_log('connman::umount_drive',
                                self.oe.execute('umount '
                                + mount_info['mountpoint']), 0)

                mount_command = 'mount -t cifs //' + mount_info['server'
                        ] + '/' + mount_info['share'] + ' ' \
                    + mount_info['mountpoint'] + ' -o "'

                if mount_info['options'] != '':
                    mount_command = mount_command + mount_info['options'
                            ] + ','

                self.oe.dbg_log('connman::mount_drive', mount_command
                                + '"', 0)

                mount_command = mount_command + 'user=' \
                    + mount_info['user'] + ','
                mount_command = mount_command + 'pass=' \
                    + mount_info['pass']
                mount_command = mount_command + '"'

                self.oe.dbg_log('connman::mount_drive',
                                self.oe.execute(mount_command), 0)

            if mount_info['type'] == 'nfs':

                if os.path.exists('/media/' + mount_info['mountpoint']):
                    if os.listdir('/media/' + mount_info['mountpoint']) \
                        != []:
                        mount_info['mountpoint'] = '_' \
                            + mount_info['mountpoint']

                mount_info['mountpoint'] = '/media/' \
                    + mount_info['mountpoint']

                if not os.path.exists(mount_info['mountpoint']):
                    os.makedirs(mount_info['mountpoint'])

                self.oe.dbg_log('connman::umount_drive',
                                self.oe.execute('umount '
                                + mount_info['mountpoint']), 0)

                mount_command = 'mount ' + mount_info['server'] + ':/' \
                    + mount_info['share'] + ' ' \
                    + mount_info['mountpoint'] + ' -o "nolock,tcp'

                if mount_info['options'] != '':
                    mount_command = mount_command + ',' \
                        + mount_info['options']

                self.oe.dbg_log('connman::mount_drive', mount_command
                                + '"', 0)

                mount_command = mount_command + '"'

                self.oe.dbg_log('connman::mount_drive',
                                self.oe.execute(mount_command), 0)

            self.oe.set_busy(0)

            self.oe.dbg_log('connman::mount_drive', 'enter_function', 0)
        except Exception, e:

            self.oe.set_busy(0)
            self.oe.dbg_log('connman::mount_drive', 'ERROR: ('
                            + repr(e) + ')')

    def start_service(self):
        try:

            self.oe.dbg_log('connman::start_service', 'enter_function',
                            0)

            self.mount_drives()

            self.oe.dbg_log('connman::start_service', 'exit_function',
                            0)
        except Exception, e:

            self.oe.dbg_log('connman::start_service', 'ERROR: ('
                            + repr(e) + ')')

    def stop_service(self):
        try:

            self.oe.dbg_log('connman::stop_service', 'enter_function',
                            0)

            self.oe.dbg_log('connman::stop_service', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('system::stop_service', 'ERROR: ('
                            + repr(e) + ')')

    def set_network_wait(self, **kwargs):
        try:

            self.oe.dbg_log('connman::set_network_wait',
                            'enter_function', 0)

            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])

            if self.struct['advanced']['settings']['wait_for_network'
                    ]['value'] == '0':

                if os.path.exists(self.wait_conf_file):
                    os.remove(self.wait_conf_file)

                return
            else:

                if not os.path.exists(os.path.dirname(self.wait_conf_file)):
                    os.makedirs(os.path.dirname(self.wait_conf_file))

                wait_conf = open(self.wait_conf_file, 'w')
                wait_conf.write('WAIT_NETWORK=true\n')
                wait_conf.write('WAIT_NETWORK_TIME=%s\n'
                                % self.struct['advanced']['settings'
                                ]['wait_for_network_time']['value'])
                wait_conf.close()

            self.oe.dbg_log('connman::set_network_wait', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.dbg_log('system::set_network_wait', 'ERROR: ('
                            + repr(e) + ')')

    def do_wizard(self):
        try:

            self.oe.dbg_log('connman::do_wizard', 'enter_function', 0)

            self.oe.winOeMain.set_wizard_title(self.oe._(32305))
            self.oe.winOeMain.set_wizard_text(self.oe._(32306))
            self.oe.winOeMain.set_wizard_button_title('')
            self.oe.winOeMain.set_wizard_list_title(self.oe._(32309))

            self.oe.winOeMain.getControl(1391).setLabel('show')

            self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[1]['id'
                    ]).controlUp(self.oe.winOeMain.getControl(self.oe.winOeMain.guiNetList))
            self.oe.winOeMain.getControl(self.oe.winOeMain.buttons[1]['id'
                    ]).controlLeft(self.oe.winOeMain.getControl(self.oe.winOeMain.guiNetList))

            self.menu_connections(None)

            self.oe.dbg_log('connman::do_wizard', 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::do_wizard', 'ERROR: (' + repr(e)
                            + ')')


# --------------------------- Wifi Monitor Loop Class --------------------------- #

class monitorLoop(threading.Thread):

    mainLoop = gobject.MainLoop()

    def __init__(self, oeMain, dbusSystemBus):
        try:

            oeMain.dbg_log('connman::monitorLoop::__init__',
                           'enter_function', 0)

            gobject.threads_init()
            dbus.mainloop.glib.threads_init()

            self.oe = oeMain
            self.dbusSystemBus = dbusSystemBus

            self.wifiAgentPath = '/OpenELEC/agent_wifi'
            self.vpnAgentPath = '/OpenELEC/agent_vpn'

            threading.Thread.__init__(self)

            self.oe.dbg_log('connman::monitorLoop::__init__',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::__init__', 'ERROR: ('
                             + repr(e) + ')', 4)

    def run(self):
        try:

            self.oe.dbg_log('connman::monitorLoop::run',
                            'enter_function', 0)

            self.dbusSystemBus.add_signal_receiver(self.propertyChanged,
                    bus_name='net.connman',
                    dbus_interface='net.connman.Manager',
                    signal_name='PropertyChanged', path_keyword='path')

            self.dbusSystemBus.add_signal_receiver(self.servicesChanged,
                    bus_name='net.connman',
                    dbus_interface='net.connman.Manager',
                    signal_name='ServicesChanged')

            self.dbusSystemBus.add_signal_receiver(self.propertyChanged,
                    bus_name='net.connman',
                    dbus_interface='net.connman.Service',
                    signal_name='PropertyChanged', path_keyword='path')

            self.dbusSystemBus.add_signal_receiver(self.technologyChanged,
                    bus_name='net.connman',
                    dbus_interface='net.connman.Technology',
                    signal_name='PropertyChanged', path_keyword='path')

            self.dbusSystemBus.add_signal_receiver(self.managerPropertyChanged,
                    bus_name='net.connman',
                    signal_name='PropertyChanged', path_keyword='path',
                    interface_keyword='interface')

            self.dbusSystemBus.watch_name_owner('net.connman.vpn',
                    self.vpnNameOwnerChanged)
            self.dbusSystemBus.watch_name_owner('net.connman',
                    self.nameOwnerChanged)

            try:
                self.oe.dbg_log('Connman Monitor started.', '', 1)
                self.mainLoop.run()
                self.oe.dbg_log('Connman Monitor stopped.', '', 1)
            except:
                pass

            self.oe.dbg_log('connman::monitorLoop::run', 'exit_function'
                            , 0)
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::run', 'ERROR: ('
                            + repr(e) + ')', 4)

    def exit(self):
        try:

            self.oe.dbg_log('connman::monitorLoop::exit',
                            'enter_function', 0)

            self.mainLoop.quit()

            self.dbusSystemBus.remove_signal_receiver(self.propertyChanged,
                    bus_name='net.connman',
                    dbus_interface='net.connman.Manager',
                    signal_name='PropertyChanged', path_keyword='path')

            self.dbusSystemBus.remove_signal_receiver(self.servicesChanged,
                    bus_name='net.connman',
                    dbus_interface='net.connman.Manager',
                    signal_name='ServicesChanged')

            self.dbusSystemBus.remove_signal_receiver(self.propertyChanged,
                    bus_name='net.connman',
                    dbus_interface='net.connman.Service',
                    signal_name='PropertyChanged', path_keyword='path')

            self.dbusSystemBus.remove_signal_receiver(self.technologyChanged,
                    bus_name='net.connman',
                    dbus_interface='net.connman.Technology',
                    signal_name='PropertyChanged', path_keyword='path')

            self.dbusSystemBus.remove_signal_receiver(self.managerPropertyChanged,
                    bus_name='net.connman',
                    signal_name='PropertyChanged', path_keyword='path',
                    interface_keyword='interface')

            try:

                if hasattr(self, 'wifiAgent'):
                    self.dbusConnmanManager.UnregisterAgent(self.wifiAgentPath)
                    self.wifiAgent.remove_from_connection(self.dbusSystemBus,
                            self.wifiAgentPath)
                    del self.wifiAgent  # = None
                    self.oe.dbg_log('connman::agentLoop::UnregisterAgent'
                                    , '(WIFI)', 0)

                    self.dbusConnmanManager = None
            except Exception, e:
                self.oe.dbg_log('connman::agentLoop::UnregisterAgent (wifi)'
                                , 'ERROR: (' + repr(e) + ')', 4)

            try:

                if hasattr(self, 'vpnAgent'):
                    self.dbusConnmanVpnManager.UnregisterAgent(self.vpnAgentPath)
                    self.vpnAgent.remove_from_connection(self.dbusSystemBus,
                            self.vpnAgentPath)
                    del self.vpnAgent  # = None
                    self.oe.dbg_log('connman::agentLoop::UnregisterAgent'
                                    , '(VPN)', 0)

                    self.dbusConnmanVpnManager = None
            except Exception, e:

                self.oe.dbg_log('connman::agentLoop::UnregisterAgent (vpn)'
                                , 'ERROR: (' + repr(e) + ')', 4)

            self.oe.dbg_log('connman::monitorLoop::exit',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::quit', 'ERROR: ('
                            + repr(e) + ')', 4)

    def nameOwnerChanged(self, proxy):
        try:

            self.oe.dbg_log('connman::agentLoop::nameOwnerChanged',
                            'enter_function', 0)

            if proxy:
                self.oe.dbg_log('connman::agentLoop::nameOwnerChanged',
                                'connman is connected to system bus', 0)
                if not hasattr(self, 'dbusConnmanManager'):
                    self.dbusConnmanManager = \
                        dbus.Interface(self.dbusSystemBus.get_object('net.connman'
                            , '/'), 'net.connman.Manager')
                self.wifiAgent = wifiAgent(self.dbusSystemBus,
                        self.wifiAgentPath)
                self.wifiAgent.oe = self.oe

                self.dbusConnmanManager.RegisterAgent(self.wifiAgentPath)
            else:

                self.oe.dbg_log('connman::agentLoop::nameOwnerChanged',
                                'connman is disconnected from system bus'
                                , 0)

                if hasattr(self, 'wifiAgent'):

                    self.dbusConnmanManager.UnregisterAgent(self.wifiAgentPath)
                    self.wifiAgent.remove_from_connection(self.dbusSystemBus,
                            self.wifiAgentPath)
                    
                    self.wifiAgent = None
                    del self.wifiAgent

                    self.dbusConnmanManager = None
                    del self.dbusConnmanManager
                    
            self.oe.dbg_log('connman::agentLoop::nameOwnerChanged',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::agentLoop::nameOwnerChanged',
                            'ERROR: (' + repr(e) + ')', 4)

    def vpnNameOwnerChanged(self, proxy):
        try:

            self.oe.dbg_log('connman::agentLoop::vpnNameOwnerChanged',
                            'enter_function', 0)

            if proxy:
                self.oe.dbg_log('connman::agentLoop::vpnNameOwnerChanged'
                                , 'vpnd is connected to system bus', 0)
                if not hasattr(self, 'dbusConnmanVpnManager'):
                    self.dbusConnmanVpnManager = \
                        dbus.Interface(self.dbusSystemBus.get_object('net.connman.vpn'
                            , '/'), 'net.connman.vpn.Manager')
                self.vpnAgent = vpnAgent(self.dbusSystemBus,
                        self.vpnAgentPath)
                self.vpnAgent.oe = self.oe

                self.dbusConnmanVpnManager.RegisterAgent(self.vpnAgentPath)
            else:

                self.oe.dbg_log('connman::agentLoop::vpnNameOwnerChanged'
                                , 'vpnd is disconnected from system bus'
                                , 0)

                if hasattr(self, 'vpnAgent'):

                    self.dbusConnmanVpnManager.UnregisterAgent(self.vpnAgentPath)
                    self.vpnAgent.remove_from_connection(self.dbusSystemBus,
                            self.vpnAgentPath)
                    
                    self.vpnAgent = None
                    del self.vpnAgent

                    self.dbusConnmanVpnManager = None
                    del self.dbusConnmanVpnManager

            self.oe.dbg_log('connman::agentLoop::vpnNameOwnerChanged',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::agentLoop::vpnNameOwnerChanged',
                            'ERROR: (' + repr(e) + ')', 4)

    def managerPropertyChanged(
        self,
        name,
        value,
        path,
        interface,
        ):
        try:

            self.oe.dbg_log('connman::monitorLoop::managerPropertyChanged'
                            , 'enter_function', 0)

            self.updateGui(name, value, path)

            self.oe.dbg_log('connman::monitorLoop::managerPropertyChanged'
                            , 'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::managerPropertyChanged'
                            , 'ERROR: (' + repr(e) + ')', 4)

    def propertyChanged(
        self,
        name,
        value,
        path,
        ):
        try:

            self.oe.dbg_log('connman::monitorLoop::propertyChanged',
                            'enter_function', 0)

            self.updateGui(name, value, path)

            self.oe.dbg_log('connman::monitorLoop::propertyChanged',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::propertyChanged',
                            'ERROR: (' + repr(e) + ')', 4)

    def technologyChanged(
        self,
        name,
        value,
        path,
        ):
        try:

            self.oe.dbg_log('connman::monitorLoop::technologyChanged',
                            'enter_function', 0)

            self.updateList()

            self.oe.dbg_log('connman::monitorLoop::technologyChanged',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::technologyChanged',
                            'ERROR: (' + repr(e) + ')', 4)

    def servicesChanged(self, services, removed):
        try:

            self.oe.dbg_log('connman::monitorLoop::servicesChanged',
                            'enter_function', 0)

            self.updateList(services, removed)

            self.oe.dbg_log('connman::monitorLoop::servicesChanged',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::servicesChanged',
                            'ERROR: (' + repr(e) + ')', 4)

    def updateList(self, services={}, removed={}):
        try:

            self.oe.dbg_log('connman::monitorLoop::updateList',
                            'enter_function', 0)

            self.oe.dictModules['connman'].menu_connections(None,
                    services, removed, force=True)

            self.oe.dbg_log('connman::monitorLoop::updateList',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::updateList',
                            'ERROR: (' + repr(e) + ')', 4)

    def updateGui(
        self,
        name,
        value,
        path,
        ):
        try:

            if not path in self.oe.dictModules['connman'].listItems \
                or self.oe.dictModules['connman'].listItems[path] \
                == None:
                return

            self.oe.dbg_log('connman::monitorLoop::updateGui',
                            'enter_function', 0)

            if name == 'Strength':
                value = str(int(value))
                self.oe.dictModules['connman'
                                    ].listItems[path].setProperty(name,
                        value)
                self.forceRender()
            elif name == 'State':

                value = str(value)
                self.oe.dictModules['connman'
                                    ].listItems[path].setProperty(name,
                        value)
                self.forceRender()
            elif name == 'IPv4':

                if 'Address' in value:
                    value = str(value['Address'])
                    self.oe.dictModules['connman'
                            ].listItems[path].setProperty('Address',
                            value)
                if 'Method' in value:
                    value = str(value['Method'])
                    self.oe.dictModules['connman'
                            ].listItems[path].setProperty('Address',
                            value)
                self.forceRender()
            elif name == 'Favorite':

                value = str(int(value))
                self.oe.dictModules['connman'
                                    ].listItems[path].setProperty(name,
                        value)
                self.forceRender()

            self.oe.dbg_log('connman::monitorLoop::updateGui',
                            'exit_function', 0)
        except KeyError:

            self.oe.dbg_log('connman::monitorLoop::updateGui',
                            'exit_function (KeyError)', 0)
            self.updateList()
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::updateGui',
                            'ERROR: (' + repr(e) + ')', 4)

    def forceRender(self):
        try:

            self.oe.dbg_log('connman::monitorLoop::forceRender',
                            'enter_function', 0)

            focusId = self.oe.winOeMain.getFocusId()
            self.oe.winOeMain.setFocusId(self.oe.listObject['netlist'])
            self.oe.winOeMain.setFocusId(focusId)

            self.oe.dbg_log('connman::monitorLoop::forceRender',
                            'exit_function', 0)
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::forceRender',
                            'ERROR: (' + repr(e) + ')', 4)


# --------------------------- Wifi Monitor Agent Class --------------------------- #....

class Failed(dbus.DBusException):

    _dbus_error_name = 'net.connman.Error.Failed'


class Canceled(dbus.DBusException):

    _dbus_error_name = 'net.connman.Error.Canceled'


class Retry(dbus.DBusException):

    _dbus_error_name = 'net.connman.Agent.Error.Retry'


class LaunchBrowser(dbus.DBusException):

    _dbus_error_name = 'net.connman.Agent.Error.LaunchBrowser'


class wifiAgent(dbus.service.Object):

    def busy(self):

        self.oe.input_request = False
        if self.oe.__busy__ > 0:
            xbmc.executebuiltin('ActivateWindow(busydialog)')

    @dbus.service.method('net.connman.Agent', in_signature='',
                         out_signature='')
    def Release(self):
        return {}

    @dbus.service.method('net.connman.Agent', in_signature='oa{sv}',
                         out_signature='a{sv}')
    def RequestInput(self, path, fields):

        try:

            self.oe.dbg_log('connman::wifiAgent::RequestInput',
                            'enter_function', 0)

            self.oe.input_request = True
            xbmc.executebuiltin('Dialog.Close(busydialog)')

            response = {}

            if fields.has_key('Name'):
                xbmcKeyboard = xbmc.Keyboard('', self.oe._(32146))
                xbmcKeyboard.doModal()
                if xbmcKeyboard.isConfirmed():
                    if xbmcKeyboard.getText() != '':
                        response['Name'] = xbmcKeyboard.getText()
                    else:
                        self.busy()
                        raise Canceled('canceled')
                        return response
                else:
                    self.busy()
                    raise Canceled('canceled')
                    return response

            if fields.has_key('Passphrase'):
                xbmcKeyboard = xbmc.Keyboard('', self.oe._(32147))
                xbmcKeyboard.doModal()
                if xbmcKeyboard.isConfirmed():
                    if xbmcKeyboard.getText() != '':
                        response['Passphrase'] = xbmcKeyboard.getText()
                        if fields.has_key('Identity'):
                            response['Identity'] = \
                                xbmcKeyboard.getText()
                        if fields.has_key('wpspin'):
                            response['wpspin'] = xbmcKeyboard.getText()
                    else:
                        self.busy()
                        raise Canceled('canceled')
                        return response
                else:
                    self.busy()
                    raise Canceled('canceled')
                    return response

            if fields.has_key('Username'):
                xbmcKeyboard = xbmc.Keyboard('', self.oe._(32148))
                xbmcKeyboard.doModal()
                if xbmcKeyboard.isConfirmed():
                    if xbmcKeyboard.getText() != '':
                        response['Username'] = xbmcKeyboard.getText()
                    else:
                        self.busy()
                        raise Canceled('canceled')
                        return response
                else:
                    self.busy()
                    raise Canceled('canceled')
                    return response

            if fields.has_key('Password'):
                xbmcKeyboard = xbmc.Keyboard('', self.oe._(32148), True)
                xbmcKeyboard.doModal()
                if xbmcKeyboard.isConfirmed():
                    if xbmcKeyboard.getText() != '':
                        response['Password'] = xbmcKeyboard.getText()
                    else:
                        self.busy()
                        raise Canceled('canceled')
                        return response
                else:
                    self.busy()
                    raise Canceled('canceled')
                    return response

            self.busy()

            self.oe.dbg_log('connman::wifiAgent::RequestInput',
                            'exit_function', 0)

            return response
        except Exception, e:

            self.oe.dbg_log('connman::monitorLoop::RequestInput',
                            'ERROR: (' + repr(e) + ')', 4)

    @dbus.service.method('net.connman.Agent', in_signature='os',
                         out_signature='')
    def RequestBrowser(self, path, url):
        self.oe.dbg_log('connman::wifiAgent::RequestBrowser',
                        'enter_function', 0)
        self.oe.dbg_log('connman::wifiAgent::RequestBrowser',
                        'exit_function', 0)
        return

    @dbus.service.method('net.connman.Agent', in_signature='os',
                         out_signature='')
    def ReportError(self, path, error):
        self.oe.dbg_log('connman::wifiAgent::ReportError',
                        'enter_function', 0)
        self.oe.dbg_log('connman::wifiAgent::ReportError',
                        'exit_function (CANCELED)', 0)
        raise Failed()
        return

    @dbus.service.method('net.connman.Agent', in_signature='',
                         out_signature='')
    def Cancel(self):
        self.oe.dbg_log('connman::wifiAgent::Cancel', 'enter_function',
                        0)
        self.oe.dbg_log('connman::wifiAgent::Cancel', 'exit_function',
                        0)
        return


class vpnAgent(dbus.service.Object):

    def busy(self):

        self.oe.input_request = False
        if self.oe.__busy__ > 0:
            xbmc.executebuiltin('ActivateWindow(busydialog)')

    @dbus.service.method('net.connman.vpn.Agent', in_signature='',
                         out_signature='')
    def Release(self):
        self.oe.dbg_log('connman::vpnAgent::Release', 'enter_function',
                        0)
        self.oe.dbg_log('connman::vpnAgent::Release',
                        'exit_function (CANCELED)', 0)

    @dbus.service.method('net.connman.vpn.Agent', in_signature='oa{sv}'
                         , out_signature='a{sv}')
    def RequestInput(self, path, fields):

        try:

            self.oe.dbg_log('connman::vpnAgent::RequestInput',
                            'enter_function', 0)

            self.oe.input_request = True
            xbmc.executebuiltin('Dialog.Close(busydialog)')

            response = {}

            for field in fields:

                if not 'Value' in fields[field]:

                    xbmcKeyboard = xbmc.Keyboard('', field)
                    xbmcKeyboard.doModal()
                    if xbmcKeyboard.isConfirmed():
                        if xbmcKeyboard.getText() != '':
                            response[field] = xbmcKeyboard.getText()
                        else:

                            raise Canceled('canceled')
                            self.busy()
                            return {}
                    else:
                        self.busy()
                        raise Canceled('canceled')
                        return {}
                else:
                    response[field] = fields[field]['Value']

            self.oe.dbg_log('connman::vpnAgent::RequestInput',
                            'exit_function', 0)

            self.busy()
            return response
        except Exception, e:

            self.oe.dbg_log('connman::vpnAgent::RequestInput',
                            'ERROR: (' + repr(e) + ')', 4)

    @dbus.service.method('net.connman.vpn.Agent', in_signature='os',
                         out_signature='')
    def ReportError(self, path, error):
        self.oe.dbg_log('connman::vpnAgent::ReportError',
                        'enter_function', 0)
        self.oe.dbg_log('connman::vpnAgent::ReportError',
                        'exit_function', 0)
        return

    @dbus.service.method('net.connman.vpn.Agent', in_signature='',
                         out_signature='')
    def Cancel(self):
        self.oe.dbg_log('connman::vpnAgent::Cancel', 'enter_function',
                        0)
        self.oe.dbg_log('connman::vpnAgent::Cancel', 'exit_function', 0)
