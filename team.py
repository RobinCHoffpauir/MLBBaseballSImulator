from typing import List
from player import Batter, Pitcher

class Team:
def init(self, name: str, batters: List[Batter], pitchers: List[Pitcher]):
self.name = name
self.batters = batters
self.pitchers = pitchers