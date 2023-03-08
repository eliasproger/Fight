from threading import Thread

import telebot
from telebot import types

from lib.unit import Unit
from lib.orm import SQLiteORM
from lib.player import Player
from lib.npc import NPC

orm = SQLiteORM("sqlite_python.db")
bot = telebot.TeleBot("6102591950:AAErdHGwvvB8kKCKtCZCPUaZBAJT4BlhG1A")
startKBoard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
arena_key = types.KeyboardButton(text='Арена')
shop_key = types.KeyboardButton(text='Рынок')
inventory_key = types.KeyboardButton(text='Инвентарь')
startKBoard.add(arena_key, shop_key, inventory_key)

player_cl = None


def create_player(chat_id, name):
    res = orm.select("Basic_Player", "*")
    HP, ATK, type, armor, level, energy, critical_chance, exp_for_lvl_up = res[0]
    id = orm.select("Player", "*")[-1][0]
    orm.insert("Player",
               (id, name, HP, ATK, type, armor, level, energy, 0, critical_chance, 0, exp_for_lvl_up, chat_id))
    orm.sqlite_connection.commit()
    player_cl = Player(HP, ATK, name, type, armor, level, id, energy, critical_chance, chat_id, exp_for_lvl_up)
    return player_cl


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

# energy_thread = Thread(target=player_cl.energy, args=(), daemon=True)

# for i in range(10):
#     insert("NPC", (20+i*2, 5+i, "Goblin" if i % 2 else "Porosya", "NPC", 100, 0, 10+i, 1))
#     sqlite_connection.commit()

npcs = orm.select("NPC", "*")


def arena():
    pass


def shop():
    pass


def inventory():
    pass


# energy_thread.start()
@bot.message_handler(commands=['start'])
def register_player(message):
    create_player(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, "Привіт", reply_markup=startKBoard)


@bot.message_handler(func=lambda message: True)
def text_handler(message):
    if message.text == "Арена":
        arena()
    elif message.text == "Рынок":
        shop()
    elif message.text == "Инвентарь":
        inventory()


@bot.message_handler(commands=['new'])
def new_player(message):
    res = orm.select("Basic_Player", "*")
    HP, ATK, type, armor, level, energy, critical_chance, exp_for_lvl_up = res[0]
    orm.update("Player",
               {"HP": HP, "ATK": ATK, "type": type, "armor": armor, "exp": 0, "current_energy": 0, "level": level,
                "energy": energy, "critical_chance": critical_chance, "exp_for_lvl_up": exp_for_lvl_up},
               {"chat_id": message.chat.id})

# while True:
#     for npc in npcs:
#         print(str(i := 1 + npcs.index(npc)) + ":" + " ", npc)
#     what_fight_index = int(input("Якого NPC Вибереш: ")) - 1
#     what_fight = npcs[what_fight_index]
#     HP, ATK, Name, Type, Armor, Level, ExpKill, LvlFight = what_fight
#     npc = NPC(HP, ATK, Name, Type, Armor, Level, ExpKill, LvlFight)
#     winner = Unit.fight(player, npc)
#     if winner.name == player.name:
#         npc.death(player)
#         npcs.remove(what_fight)
#         print(player.name, "Виграв")
#     else:
#         player.death(npc)
#         print(player.name, "Програв")
#         break
bot.infinity_polling()
