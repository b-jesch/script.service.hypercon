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

    colors = []

    li = xbmcgui.ListItem(label=LS(32040), label2=moodcolor_1, iconImage=icon_1)
    li.setProperty('color', moodcolor_1)
    colors.append(li)
    li = xbmcgui.ListItem(label=LS(32041), label2=moodcolor_2, iconImage=icon_2)
    li.setProperty('color', moodcolor_2)
    colors.append(li)
    li = xbmcgui.ListItem(label=LS(32042), label2=moodcolor_3, iconImage=icon_3)
    li.setProperty('color', moodcolor_3)
    colors.append(li)


    dialog = xbmcgui.Dialog()
    _idx = dialog.select(LS(32000), colors, useDetails=True)
    if _idx > -1:
        kl.writeLog('set color to %s' % colors[_idx].getProperty('color'))
        connection.setColor(colors[_idx].getProperty('color'))
