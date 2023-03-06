from threading import Thread

from unit import Unit
from orm import SQLiteORM
from player import Player
from npc import NPC

orm = SQLiteORM("sqlite_python.db")


def create_player(id, chat_id, name):
    res = orm.select("Basic_Player", "*")
    HP, ATK, type, armor, level, energy, critical_chance, exp_for_lvl_up = res[0]
    return Player(HP, ATK, name, type, armor, level, id, energy, critical_chance, chat_id, exp_for_lvl_up)

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

npcs = orm.select("NPC", "*")

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
