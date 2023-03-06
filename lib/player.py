import time

from unit import Unit


class Player(Unit):
    def __init__(self, HP, ATK, name, type, armor, level, id, energy, critical_chance, chat_id, exp_for_lvl_up):
        super().__init__(HP, ATK, name, type, armor, level)
        self.id = id
        self._energy = energy
        self.current_energy = energy
        self.critical_chance = critical_chance
        self.chat_id = chat_id
        self._exp_for_lvl_up = exp_for_lvl_up
        self._exp = 0

    @property
    def exp_for_lvl_up(self):
        return self._exp_for_lvl_up

    @exp_for_lvl_up.setter
    def exp_for_lvl_up(self, value):
        self._exp_for_lvl_up = value
        if self.level > 1:
            self.exp += value - (self.level - 1) * 20

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        self._exp += value
        if self._exp >= self.exp_for_lvl_up:
            self.level += 1
            self.exp = self._exp - self.exp_for_lvl_up
            self.exp_for_lvl_up += 20
        elif self._exp < 0:
            self.level -= 1
            self.exp = self.exp_for_lvl_up - self._exp
            self.exp_for_lvl_up -= 20

    def energy(self):
        while True:
            if self.current_energy > 0:
                self.current_energy -= 2
            else:
                self.current_energy = 0
            time.sleep(1)
            if (self._energy - self.current_energy) >= 3:  # 3 это добавления энергии в секунду
                self.current_energy += 3
            else:
                self.current_energy += self._energy - self.current_energy

    def death(self, NPC):
        self._exp -= NPC.exp_for_kill / 2