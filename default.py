from resources.lib.toollib import *
from resources.lib.connection import Connection

kl = KodiLib()

ip = kl.getAddonSetting('ip')
port = kl.getAddonSetting('port')

connection = Connection(ip, port)

moodcolor_1 = kl.getAddonSetting('moodcolor_1')
moodcolor_2 = kl.getAddonSetting('moodcolor_2')
moodcolor_3 = kl.getAddonSetting('moodcolor_3')

icon_1 = os.path.join(ADDON_PATH, 'resources', 'media', moodcolor_1)
icon_2 = os.path.join(ADDON_PATH, 'resources', 'media', moodcolor_2)
icon_3 = os.path.join(ADDON_PATH, 'resources', 'media', moodcolor_3)

if __name__ == '__main__':

    actions = []

    li = xbmcgui.ListItem(label=LS(32043), label2=LS(32044), iconImage=os.path.join(ADDON_PATH, 'icon.png'))
    li.setProperty('action', 'clearall')
    li.setProperty('param', '100')
    actions.append(li)
    li = xbmcgui.ListItem(label=LS(32040), label2=moodcolor_1, iconImage=icon_1)
    li.setProperty('action', 'setcolor')
    li.setProperty('param', moodcolor_1)
    actions.append(li)
    li = xbmcgui.ListItem(label=LS(32041), label2=moodcolor_2, iconImage=icon_2)
    li.setProperty('action', 'setcolor')
    li.setProperty('param', moodcolor_2)
    actions.append(li)
    li = xbmcgui.ListItem(label=LS(32042), label2=moodcolor_3, iconImage=icon_3)
    li.setProperty('action', 'setcolor')
    li.setProperty('param', moodcolor_3)
    actions.append(li)

    dialog = xbmcgui.Dialog()
    _idx = dialog.select(LS(32000), actions, useDetails=True)
    if _idx > -1:
        action = actions[_idx].getProperty('action')
        param = actions[_idx].getProperty('param')
        print action, param

        if action == 'setcolor': connection.setColor(param)
        elif action == 'clearall': connection.clearAll()
        else:
            kl.writeLog('unknown parameter', xbmc.LOGERROR)
