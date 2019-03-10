from __future__ import unicode_literals


import sys,os,urllib
reload(sys)
sys.setdefaultencoding('utf-8')

import xbmc
try:
    from xbmc import log
except:
    def log(msg):
        print(msg)
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory

from resources.lib.modules.addon import Addon
from resources.lib.modules import routing
from resources.lib.modules.log_utils import log

addon = Addon('plugin.video.vardyparty', sys.argv)
addon_handle = int(sys.argv[1])
plugin = routing.Plugin()
AddonPath = addon.get_path()
IconPath = os.path.join(AddonPath , "resources/media/")
fanart = os.path.join(AddonPath + "/fanart.jpg")

# Update path so that praw doesnt complain
sys.path.append(os.path.join(AddonPath, 'resources/lib/modules'))

from resources.lib.modules.competitionclient import CompetitionClient
from resources.lib.modules.gameclient import GameClient
from resources.lib.modules.streamclient import StreamClient
from resources.lib.modules.gamedataprovider.gamedataprovider import GameDataProvider
from resources.lib.modules.gamedataprovider.footybitestreamprovider import FootyBiteStreamProvider
from resources.lib.modules.gamedataprovider.redditstreamprovider import RedditStreamProvider
from resources.lib.modules.subreddits import SubRedditEvents
from resources.lib.modules.gamedataprovider.acestreamlinkprovider import AcestreamLinkProvider

AS_LAUNCH_LINK = 'XBMC.RunPlugin(plugin://program.plexus/?mode=1&url={url}&name={name})'

def icon_path(filename):
    if 'http://' in filename:
        return filename
    return os.path.join(IconPath, filename)

@plugin.route('/')
def index():
    addDirectoryItem(
        plugin.handle,
        plugin.url_for(competitions),
        ListItem("Acestreams"), True)
    endOfDirectory(plugin.handle)

@plugin.route('/competitions')
def competitions():
    gameDataProvider= GameDataProvider()
    redditStreamProvider= RedditStreamProvider(SubRedditEvents())
    acestreamLinkProvider=AcestreamLinkProvider(gameDataProvider, redditStreamProvider,FootyBiteStreamProvider())
    gameClient=GameClient(gameDataProvider, acestreamLinkProvider)
    competitionClient= CompetitionClient(gameDataProvider, gameClient)
    for url, title, icon in competitionClient.get_competitions():
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(competition, url),
            ListItem(title, iconImage=icon), True)
    endOfDirectory(plugin.handle)

@plugin.route('/competition/<competition_id>')
def competition(competition_id):
    gameDataProvider= GameDataProvider()
    redditStreamProvider=RedditStreamProvider(SubRedditEvents())
    acestreamLinkProvider=AcestreamLinkProvider(gameDataProvider, redditStreamProvider, FootyBiteStreamProvider())
    gameClient= GameClient(gameDataProvider, acestreamLinkProvider)
    for title, id in gameClient.get_games(competition_id):
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(game,id),
            ListItem(title), True)
    endOfDirectory(plugin.handle)

@plugin.route('/game/<game_id>')
def game(game_id):
    gameDataProvider= GameDataProvider()
    streamClient= StreamClient(gameDataProvider, AcestreamLinkProvider(gameDataProvider, RedditStreamProvider(SubRedditEvents()), FootyBiteStreamProvider()))
    for acestreamLink, title in streamClient.get_streams(game_id):
        url = plugin.url_for(play, urllib.quote(acestreamLink, safe=''))
        addDirectoryItem(
            plugin.handle,
            url,
            ListItem(title), True)
    endOfDirectory(plugin.handle)

@plugin.route('/play/<url>')
def play(url):
    stream_url = urllib.unquote(url)
    log("Playing {}".format(stream_url))
    try:
        xbmc.executebuiltin(AS_LAUNCH_LINK.format(url=stream_url, name='Vardys Party'))
    except Exception as inst:
        xbmc.log(inst, 3)


if __name__ == '__main__':
    plugin.run()