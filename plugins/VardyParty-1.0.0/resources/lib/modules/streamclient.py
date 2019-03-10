import os, sys, re, json
reload(sys)

try:
    from xbmc import log
except:
    def log(msg):
        print(msg)

class StreamClient(object):
    def __init__(self, gameDataProvider, acestreamLinkProvider):
        self.gameDataProvider = gameDataProvider
        self.acestreamLinkProvider = acestreamLinkProvider

    def get_streams(self, game_id):
        streams=[]
        gameData= self.gameDataProvider.get_game_data()
        for competition in gameData:
            for event in competition['events']:
                if (str(event['id'])==game_id):
                    acestreams= self.acestreamLinkProvider.get_acestreams(game_id)
                    for acestreamUrl, title in acestreams:
                        if (title==None or title==""):
                            title= "Unknown Stream"
                        streams.append((acestreamUrl, title))
        return streams