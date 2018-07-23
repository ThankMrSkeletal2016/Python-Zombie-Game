__author__ = 'Ian Kent'

import enemies, world, actions, items, random

"""The base class for a tile within the world space"""
"""------------------------------------------------"""
class MapTile:
    """The base class for a tile within the world space"""

    def __init__(self, x, y):
        """Creates a new tile.

        :param x: the x-coordinate of the tile
        :param y: the y-coordinate of the tile
        """
        self.x = x
        self.y = y

    def intro_text(self):
        """Information to be displayed when the player moves into this tile."""
        raise NotImplementedError()

    def modify_player(self, the_player):
        """Process actions that change the state of the player."""
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.ViewMap())
        return moves


"""The base tiles that inherit the original Map Tile, and are passed on"""
"""------------------------------------------------"""

class LootRoom(MapTile):
    """A room that adds something to the player's inventory"""

    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, the_player):
        the_player.inventory.append(self.item)

    def modify_player(self, the_player):
        self.add_loot(the_player)

class ConditionRoom(MapTile):
    """A room that has a condition that depends on character"""

    def __init__(self, x, y, name):
        self.name = name
        super().__init__(x, y)

    def modify_player(self, the_player):
        pass


class GoldRoom(MapTile):
    """A room that adds something to the player's inventory"""

    def __init__(self, x, y, amt):
        self.amt = amt
        super().__init__(x, y)

    def add_gold(self, the_player, amt):
        the_player.gold += amt

    def modify_player(self, the_player):
        self.add_gold(the_player, self.amt)

class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            enemy_damage = random.randint(0, self.enemy.damage)
            the_player.hp = the_player.hp - enemy_damage
            print("Enemy does {} damage. You have {} HP remaining.".format(enemy_damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()

"""Item Tiles"""
"""------------------------------------------------"""
class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())

    def intro_text(self):
        return """
        You notice something shiny in the corner of the apartment.
        It's a dagger! You pick it up.
        """


class Find5GoldRoom(GoldRoom):
    def __init__(self, x, y):
        super().__init__(x, y, 5)

    def intro_text(self):
        return """
        Someone dropped a 5 gold piece. You pick it up.
        """

"""Enemy Tiles"""
"""------------------------------------------------"""
class EasyZombieRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.EasyZombie())
        print(self.enemy.gold)

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            As you open the door, a Zombie suddenly comes out of the closet
            and swings at you
            """
        else:
            return """
            The corpse of a dead Zombie rots on the ground.
            """

"""Condition Rooms"""
"""------------------------------------------------"""

class LeaveApartment(ConditionRoom):
    def __init__(self, x, y):
        super().__init__(x, y, "Leave Apartment")

    def intro_text(self, player):
        if player.gold > 20:
            return """
            The Door to the outside. You walk out into the world.
            """
        else :
            return """
            You must secure the building before you leave!
            """

    def modify_player(self, player):
        if player.gold > 20:
            player.victory = True

"""Basic Rooms"""
"""------------------------------------------------"""
class StartingRoom(MapTile):
    def intro_text(self):
        return """
       You wake up in an apartment. You hear a sound across the hall.
        """

    def modify_player(self, the_player):
        # Room has no action on player
        pass

class EmptyHallway(MapTile):
    def intro_text(self):
        return """
        An empty apartment hallway
        """

    def modify_player(self, the_player):
        # Room has no action on player
        pass

class EmptyApartment(MapTile):
    def intro_text(self):
        return """
        An empty apartment with nothing of interest.
        """

    def modify_player(self, the_player):
        # Room has no action on player
        pass

class EmptyAptHallway(MapTile):
    def intro_text(self):
        return """
        An empty apartment hallway leading to an apartment
        """

    def modify_player(self, the_player):
        # Room has no action on player
        pass

class LockedDoor(MapTile):
    def intro_text(self):
        return """
        A locked door. You can not pass.
        """

    def modify_player(self, the_player):
        # Room has no action on player
        pass