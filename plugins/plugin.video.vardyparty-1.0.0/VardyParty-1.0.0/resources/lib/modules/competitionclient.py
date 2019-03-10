import os, sys, re
reload(sys)

try:
    from xbmc import log
except:
    def log(msg):
        print(msg)

class CompetitionClient(object):
    def __init__(self, gameDataProvider, gameClient):
        self.gameDataProvider= gameDataProvider
        self.gameClient= gameClient

    def get_competitions(self):
        gameData= self.gameDataProvider.get_game_data()
        competitions= []
        for i in gameData:
            eventStreams= len(self.gameClient.get_games(i['id']))
            if (eventStreams > 0):
                competitions.append(
                    (i['id'], i['name'] + "\n"+str(eventStreams)+" events", i['logo'])
                )
        return competitions