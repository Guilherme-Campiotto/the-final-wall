#coding: utf-8


class Weapon():
    avaiable = False
    name = None

class Ak47(Weapon):
    name = "Ak47"

class Pistol(Weapon):
    name = "Pistol"

class Inventory(object):
    primary = None
    secondary = None

    slots = []

    def __init__(self):
        self._insertFromInventory(Pistol())
        self._insertFromInventory(Ak47())

    def toggleWeapon(self, weapon):
        weapon.avaiable = not weapon.avaiable

    def disableWeapon(self, weapon):
        weapon.avaiable = False

    def enableWeapon(self, weapon):
        weapon.avaiable = True

    def setPrimary(self, weapon):
        if not weapon.avaiable:
            return False
        self._removeFromInventory(weapon)
        self._insertFromInventory(self.primary)
        self.primary = weapon

    def setSecondary(self, weapon):
        if not weapon.avaiable:
            return False
        self._removeFromInventory(weapon)
        self._insertFromInventory(self.secondary)
        self.secondary = weapon

    def _removeFromInventory(self, weapon):
        if self.slots.get(weapon.name, False):
            del self.slots[weapon.name]

    def _insertToInventory(self, weapon):
        if self.slots.get(weapon.name, False):
            pass
        self.slots[weapon.name] = weapon
