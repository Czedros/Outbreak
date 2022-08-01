import random as rd
from Resource import Resource
from Animator import Animations
from Animator import Animation
import Animator
from ZombieAI import ZombieAI

class Person:
    wasVaccinated : bool = False
    turnsVaccinated : int = 0
    isVaccinated : bool= False
    isZombie : bool = False
    wasCured : bool = False
    classID = 0
    AP = Resource("AP", 3, {"Move" : 1 , "Bite": 1} )
    def __init__(self, iz: bool):
        self.isZombie = iz
        self.ID = Person.classID
        Person.classID+=1
        if(self.isZombie):
            self.animation = Animation(Animations.zombie.value)
            self.ai = ZombieAI() #originally at bottom
        else:
            self.animation = Animation(Animations.human.value)
        self.AP.setToMax()
        

    def clone(self):
        ret = Person(self.isZombie)
        ret.wasVaccinated = self.wasVaccinated
        ret.turnsVaccinated = self.turnsVaccinated
        ret.isVaccinated = self.isVaccinated
        ret.wasCured = self.wasCured
        ret.AP = self.AP
        ret.animation = self.animation
        return ret

    def calcInfect(self):
        chance = 100
        if self.isVaccinated == True:
            chance -= self.vaccinationStatus()
        if rd.randint(0,100) < chance:
            self.isZombie = True
            self.animation = Animation(Animations.zombie.value)
            print("The zombie successfully infected you, action completed successfully in Person")
        else:
            print("The zombie failed to infect you, action completed successfully in Person")
    def calcCureSuccess(self):
        chance = 20
        if self.wasCured == True:
            chance -= 20
        if rd.randint(0,100) > chance:
            self.isZombie = False
            self.animation = Animation(Animations.human.value)
            print("Cure/Vaccine was successful, action completed successfully in Person")
            Person.classID -= 1
            return True
        self.wasCured = True
        return False
 
    def vaccinationStatus(self):
        return 100 - (25*(self.turnsVaccinated - 1))

    def get_vaccinated(self):
        self.wasVaccinated = True
        self.isVaccinated = True
        self.turnsVaccinated = 0


    def update(self):
        if self.isVaccinated:
            self.turnsVaccinated += 1
        if self.turnsVaccinated > 4:
            self.isVaccinated = False
            self.turnsVaccinated = 0
        self.AP.setToMax()

    def __str__(self) -> str:
        return f"Person who is a zombie? {self.isZombie}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __o: object) -> bool:
        if type(__o) == Person:
            return (
                self.wasVaccinated == __o.wasVaccinated
                and self.turnsVaccinated == __o.turnsVaccinated
                and self.isVaccinated == __o.isVaccinated
                and self.isZombie == __o.isZombie
                and self.wasCured == __o.wasCured
            )
        return False
