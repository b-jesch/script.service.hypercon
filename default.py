#! /bin/python

from resources.lib.toollib import *
from resources.lib.connection import Connection
import sys

kl = KodiLib()
dialog = xbmcgui.Dialog()

ip = kl.getAddonSetting('ip')
port = kl.getAddonSetting('port')

connection = Connection(ip, port)

switchDirectly = kl.getAddonSetting('switchDirectly', sType=BOOL)

moodcolor_1 = kl.getAddonSetting('moodcolor_1')
moodcolor_2 = kl.getAddonSetting('moodcolor_2')
moodcolor_3 = kl.getAddonSetting('moodcolor_3')

effect_1 = kl.getAddonSetting('effect_1')
effect_2 = kl.getAddonSetting('effect_2')
effect_3 = kl.getAddonSetting('effect_3')

icon_1 = os.path.join(ADDON_PATH, 'resources', 'media', moodcolor_1)
icon_2 = os.path.join(ADDON_PATH, 'resources', 'media', moodcolor_2)
icon_3 = os.path.join(ADDON_PATH, 'resources', 'media', moodcolor_3)

defaultIcon = os.path.join(ADDON_PATH, 'icon.png')


def toogle():
    if kl.getProperty('hyperion.status') == 'on':
        connection.setColor('#000000')
        kl.setProperty('hyperion.status', 'off')
        kl.writeLog('Hyperion service status toggle to off', xbmc.LOGINFO)
    else:
        kl.setProperty('hyperion.status', 'on')
        kl.setProperty('hyperion.check', '0')
        kl.writeLog('Hyperion service status toggle to on', xbmc.LOGINFO)


if __name__ == '__main__':

    items = list()
    arguments = sys.argv
    if len(arguments) > 1:
        c_args = kl.ParamsToDict(arguments[1])
        kl.writeLog('getting controller parameters: %s' % c_args)

        if c_args['action'] == 'fetch_effects':
            effects = connection.fetchEffectList()
            if effects:
                for names in effects:
                    li = xbmcgui.ListItem(label=names)
                    li.setArt({'icon': defaultIcon})
                    li.setProperty('effect', names)
                    items.append(li)
                _idx = dialog.select(LS(32015), items)
                if _idx > -1:
                    ADDON.setSetting(c_args['item'], items[_idx].getProperty('effect'))
            else:
                kl.notifyOSD(32000, 32061, icon=xbmcgui.NOTIFICATION_WARNING)

        elif c_args['action'] == 'toggle': toogle()
        elif c_args['action'] == 'check':

            li = xbmcgui.ListItem(label=LS(32040), label2=moodcolor_1)
            li.setArt({'icon': icon_1})
            li.setProperty('action', 'setcolor')
            li.setProperty('param', moodcolor_1)
            items.append(li)
            li = xbmcgui.ListItem(label=LS(32041), label2=moodcolor_2)
            li.setArt({'icon': icon_2})
            li.setProperty('action', 'setcolor')
            li.setProperty('param', moodcolor_2)
            items.append(li)
            li = xbmcgui.ListItem(label=LS(32042), label2=moodcolor_3)
            li.setArt({'icon': icon_3})
            li.setProperty('action', 'setcolor')
            li.setProperty('param', moodcolor_3)
            items.append(li)
            li = xbmcgui.ListItem(label=LS(32045), label2=effect_1)
            li.setArt({'icon': defaultIcon})
            li.setProperty('action', 'effect')
            li.setProperty('param', effect_1)
            items.append(li)
            li = xbmcgui.ListItem(label=LS(32046), label2=effect_2)
            li.setArt({'icon': defaultIcon})
            li.setProperty('action', 'effect')
            li.setProperty('param', effect_2)
            items.append(li)
            li = xbmcgui.ListItem(label=LS(32047), label2=effect_3)
            li.setArt({'icon': defaultIcon})
            li.setProperty('action', 'effect')
            li.setProperty('param', effect_3)
            items.append(li)

            _idx = dialog.select(LS(32000), items, useDetails=True)
            if _idx > -1:
                action = items[_idx].getProperty('action')
                param = items[_idx].getProperty('param')
                kl.setProperty('hyperion.check', '5')

                if action == 'setcolor':
                    if kl.getProperty('hyperion.status') == 'off': toogle()
                    connection.setColor(param)
                elif action == 'effect':
                    if kl.getProperty('hyperion.status') == 'off': toogle()
                    connection.setEffect(param)
                else:
                    kl.writeLog('unknown parameter', xbmc.LOGERROR)

    if not switchDirectly:
        li = xbmcgui.ListItem(label=LS(32058),
                              label2=LS(32059) % {'on': LS(32043), 'off': LS(32057)}.get(kl.getProperty('hyperion.status')))
        li.setArt({'icon': defaultIcon})
        li.setProperty('action', 'toggle')
        li.setProperty('param', '')
        items.append(li)
        li = xbmcgui.ListItem(label=LS(32050), label2=LS(32044))
        li.setArt({'icon': defaultIcon})
        li.setProperty('action', 'clearall')
        li.setProperty('param', '100')
        items.append(li)

        _idx = dialog.select(LS(32000), items, useDetails=True)
        if _idx > -1:
            action = items[_idx].getProperty('action')
            param = items[_idx].getProperty('param')

            if action == 'toggle': toogle()
            elif action == 'clearall':
                if kl.getProperty('hyperion.status') == 'off': toogle()
                kl.setProperty('hyperion.check', '0')
                connection.clearAll()
            else:
                kl.writeLog('unknown parameter', xbmc.LOGERROR)
    else:
        toogle()
