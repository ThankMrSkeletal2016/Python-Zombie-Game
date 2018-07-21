import random

class Enemy:
    """A base class for all enemies"""
    def __init__(self, name, hp, damage):
        """Creates a new enemy

        :param name: the name of the enemy
        :param hp: the hit points of the enemy
        :param damage: the damage the enemy does with each attack
        """
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0


class EasyZombie(Enemy):
    def __init__(self):
        super().__init__(name="Easy Zombie", hp=10, damage=5)
        print(self.hp)
        print(self.damage)


class MediumZombie(Enemy):
    def __init__(self):
        super().__init__(name="Medium Zombie", hp=30, damage=15)
