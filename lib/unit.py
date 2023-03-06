class Unit:
    def __init__(self, HP: int, ATK, name: str, type, armor, level: int):
        self.HP = HP
        self.current_HP = HP
        self.ATK = ATK
        self.name = name
        self.type = type
        self.armor = armor
        self.level = level

    def bit_unit(self, another_unit: object):
        self.current_HP -= (another_unit.ATK - (self.armor / 100))

    def death(self):
        pass

    @staticmethod
    def fight(player, NPC):
        while player.current_HP > 0 and NPC.current_HP > 0:
            player.bit_unit(NPC)
            if player.current_HP > 0:
                NPC.bit_unit(player)
        if player.current_HP > 0:
            return player
        else:
            return NPC
