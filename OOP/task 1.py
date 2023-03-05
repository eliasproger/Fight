import random
import time
from threading import Thread
import sqlite3


# region Classes
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


class NPC(Unit):
    def __init__(self, HP, ATK, name, type, armor, level, exp_for_kill, lvl_for_fight):
        super().__init__(HP, ATK, name, type, armor, level)
        self.exp_for_kill = exp_for_kill
        self.lvl_for_fight = lvl_for_fight

    def death(self, player):
        player._exp += self.exp_for_kill


# endregion

sqlite_connection = sqlite3.connect('sqlite_python.db')
cursor = sqlite_connection.cursor()


# region Functions
def select(table_name: str, columns: str):
    req = f"SELECT {columns} FROM {table_name};"
    cursor.execute(req)
    return cursor.fetchall()


def insert(table_name: str, new_values: tuple):
    req = f"INSERT INTO {table_name} VALUES{new_values};"
    cursor.execute(req)


def update(table_name, set_column, set_value, where_column, where_value):
    req = f"UPDATE {table_name} SET {set_column} = {set_value} WHERE {where_column} = {where_value}"
    cursor.execute(req)


def delete(table_name, where_column, where_value):
    req = f"DELETE FROM {table_name} WHERE {where_column} = {where_value}"


def create_player(id, chat_id, name):
    res = select("Basic_Player", "*")
    HP, ATK, type, armor, level, energy, critical_chance, exp_for_lvl_up = res[0]
    return Player(HP, ATK, name, type, armor, level, id, energy, critical_chance, chat_id, exp_for_lvl_up)


# endregion

# region Table Create Requests
base_player_create = """CREATE TABLE Basic_Player
                (HP INTEGER, 
                 ATK INTEGER, 
                 type TEXT, 
                 armor INTEGER, 
                 level INTEGER, 
                 energy INTEGER, 
                 critical_chance INTEGER, 
                 exp_for_lvl_up INTEGER)"""

player_tabel_create = """CREATE TABLE Player
                (id INTEGER PRIMARY KEY, 
                 name TEXT, 
                 HP INTEGER, 
                 ATK INTEGER, 
                 type TEXT, 
                 armor INTEGER, 
                 level INTEGER, 
                 energy INTEGER, 
                 current_energy INTEGER, 
                 critical_chance INTEGER, 
                 exp INTEGER, 
                 exp_for_lvl_up INTEGER, 
                 chat_id TEXT)"""

npc_table_create = """CREATE TABLE NPC
             (HP int, ATK int, name text, type text, armor int,
              level int, exp_for_kill int, lvl_for_fight int)"""
# endregion


player = create_player(1, 46564564, "Ponchik")
energy_thread = Thread(target=player.energy, args=(), daemon=True)

# for i in range(10):
#     insert("NPC", (20+i*2, 5+i, "Goblin" if i % 2 else "Porosya", "NPC", 100, 0, 10+i, 1))
#     sqlite_connection.commit()

npcs = select("NPC", "*")

energy_thread.start()
while True:
    for npc in npcs:
        print(str(i := 1 + npcs.index(npc)) + ":" + " ", npc)
    what_fight_index = int(input("Якого NPC Вибереш: ")) - 1
    what_fight = npcs[what_fight_index]
    HP, ATK, Name, Type, Armor, Level, ExpKill, LvlFight = what_fight
    npc = NPC(HP, ATK, Name, Type, Armor, Level, ExpKill, LvlFight)
    winner = Unit.fight(player, npc)
    if winner.name == player.name:
        npc.death(player)
        npcs.remove(what_fight)
        print(player.name, "Виграв")
    else:
        player.death(npc)
        print(player.name, "Програв")
        break
