from lib.unit import Unit
class NPC(Unit):
    def __init__(self, HP, ATK, name, type, armor, level, exp_for_kill, lvl_for_fight):
        super().__init__(HP, ATK, name, type, armor, level)
        self.exp_for_kill = exp_for_kill
        self.lvl_for_fight = lvl_for_fight

    def death(self, player):
        player._exp += self.exp_for_kill
