import datetime


class Pearson:
    def __init__(self, name: str, surname: str, age: int):
        self.name = name
        self.surname = surname
        self.age = age
        self.__birth_year = 0
        self.password = ""

    @property
    def BirthYear(self):
        return self.__birth_year

    @BirthYear.setter
    def BirthYear(self, value):
        self.__birth_year = datetime.datetime.now().year - value

    @BirthYear.getter
    def BirthYear(self):
        if self.password == "password":
            return self.__birth_year
        else:
            return "Not have a permission"

    def drink(self, **kwargs):
        print(kwargs)
        return f"Drink {kwargs['something']}"


class UAMan(Pearson):

    def __init__(self, name: str, surname: str, age: int):
        super().__init__(name, surname, age)

    def hello(self):
        print(f"Привіт, мене звуть {self.name}")


class USAWoman(Pearson):

    def __init__(self, name: str, surname: str, age: int):
        super().__init__(name, surname, age)

    def hello(self):
        print(f"Hi, My name is {self.name}")

    @staticmethod
    def walk():
        print(f"I am go to park")

    def drink(self, **kwargs):
        super().drink(**kwargs)
        print(int(kwargs["value"]) - 10)
        return f"Drink {kwargs['something']}"


man = UAMan("Artem", "Ivanov", 20)
woman = USAWoman("Sandra", "Ivanov", 20)

man.hello()
woman.hello()

USAWoman.walk()
woman.password = "password"
print(woman.drink(something="water", value="1", value2="2"))


# Unit - имеет поля : HP, current_HP, ATK, name, type, armor, level
# Unit иеет функции:
# bit_unit(self, another_unit) - берет на вход другой юнит и отнимает его HP по формуле : HP - (another_unit.ATK - (armor)%)
# death - заготовка для переопределения
# fight - статический метод для стражения получает на вход два экземпляра Unit (player, NPC) - бой идет по циклу первый атакует игрок, бой идет пока у игрока или у нпс HP > 0 при достижении HP < 0 у одного из противников должен выполнятся метод death и цикл обрывается возвращая экземпляр победителя
# Player - наследник от Unit имеет поля : id, energy, current_energy, critical_chance, chat_id, exp_for_lvl_up, exp
# NPC - наследник от Unit имеет поля: exp_for_kill, lvl_for_fight.
# Player имеет функионал:
# При повишении level, exp_for_lvl_up увеличивается на 20
# При достижении exp = exp_for_lvl_up: level += 1 при exp < 0: level -= 1, exp_for_lvl_up - 20, exp = exp_for_lvl_up - exp описать свойствами для exp
# death(self, NPC) уменьшает опыт игрока = exp - NPC.exp_for_kill /2
# NPC - имеет функции:
# death(self, player) - добавляет к player.exp  exp_for_kill

