import random
import world, items

__author__ = 'Ian Kent'


class Player:
    def __init__(self):
        self.inventory = [items.Rock()]
        self.gold = 15
        self.hp = 20
        self.location_x, self.location_y = world.starting_position
        self.victory = False

    def is_alive(self):
        return self.hp > 0

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')
        print("Gold : {}".format(self.gold))

    def print_map(self):
        print("")
        print("Feature Will Be Added Soon.")
        print("Until then, you can check the txt file next to the exe!")
        print("")

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        try:
            if world.tile_exists(self.location_x, self.location_y).name == "Leave Apartment":
                print(world.tile_exists(self.location_x, self.location_y).intro_text(self))
        except AttributeError:
            print(world.tile_exists(self.location_x, self.location_y).intro_text())


    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i

        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        dmg = random.randint(0,best_weapon.damage)
        enemy.hp -= dmg
        print("You did {} damage".format(dmg))
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
            print("You gained {} gold!".format(enemy.gold))
            self.gold += enemy.gold
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

    def remove_gold(self, amt):
        self.gold -= amt

    def add_gold(self, amt):
        self.gold += amt