from typing import Optional

class Player:
def init(self, name: str):
self.name = name

class Batter(Player):
def init(self, name: str, avg: float, obp: float, slg: float):
super().init(name)
self.avg = avg
self.obp = obp
self.slg = slg

class Pitcher(Player):
def init(self, name: str, era: float, whip: float):
super().init(name)
self.era = era
self.whip = whip