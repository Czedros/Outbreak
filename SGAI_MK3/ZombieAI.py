import random as rd


class ZombieAI:
    wasVaccinated : bool = False
    turnsVaccinated : int = 0
    isVaccinated : bool= False
    isZombie : bool = False
    wasCured : bool = False
    def __init__(self, iz: bool):
        self.isZombie = iz
        self.states = {
            "Roam" : self.setStateRoam(),
            "Seek" : self.setStateSeek(),
            "Attack" : self.setAttackState()
        }
    def act(self):
        return False
    def setStateRoam(self):
        return True