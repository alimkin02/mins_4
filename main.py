import random
import numpy as np

class Unit:
    def __init__(self, name, max_health, damage, block_damage, heal_amount):
        self.name = name
        self.current_health = max_health
        self.max_health = max_health
        self.damage = damage
        self.block_damage = min(block_damage, damage)  # Убедимся, что блок не превышает урона
        self.heal_amount = min(heal_amount, max_health // 2)  # Не даем восстанавливать более половины здоровья
        self.current_action = 0

    def attack(self, target):

        print(f"{self.name} атакует {target.name} и наносит {self.damage} урона.")
        target.current_health -= self.damage
        target.print_cur_stat()

    def block_attack(self, target):

        print(f"{self.name} блокирует {target.name}")
        self.current_health = min(self.current_health + self.block_damage, self.max_health)
        self.print_cur_stat()

    def heal(self):
        print(f"{self.name} восстанавливает {self.heal_amount} здоровья.")
        if self.current_health != self.max_health:
            print(f"{self.name} уже на максимальном здоровье.")
            return
        self.current_health = min(self.max_health, self.current_health + self.heal_amount)
        self.print_cur_stat()

    def print_cur_stat(self):
        print("---------------------------------")
        print(f"Текущая статистика \033[32m{self.name}:\033[0m")
        print(f"Здоровье в результате действия: \033[32m{self.current_health}\033[0m")
        print(f"Наносимый урон: \033[32m{self.damage}\033[0m")
        print(f"Блокируемый урон: \033[32m{self.block_damage}\033[0m")
        print(f"Восстанавливающееся здоровье: \033[32m{self.heal_amount}\033[0m")
        print("---------------------------------")

    def get_name(self):
        return self.name

    def get_max_health(self):
        return self.max_health

    def get_damage(self):
        return self.damage

    def get_block_damage(self):
        return self.block_damage

    def get_heal_amount(self):
        return self.heal_amount

    def get_current_action(self):
        return self.current_action

    def set_name(self, name):
        self.name = name

    def set_max_health(self, max_health):
        self.max_health = max_health

    def ser_damage(self, damage):
        self.damage = damage

    def set_block_damage(self, block_damage):
        self.block_damage = block_damage

    def set_heal_amount(self, heal_amount):
        self.heal_amount = heal_amount

    def is_dead(self):
        return self.current_health <= 0


class Bot(Unit):
    def __init__(self, name, max_health, damage, block_damage, heal_amount, transition_matrix):
        super().__init__(name, max_health, damage, block_damage, heal_amount)
        self.transition_matrix = transition_matrix

    def get_transition_matrix(self):
        return self.transition_matrix

    def set_transition_matrix(self, transition_matrix):
        self.transition_matrix = transition_matrix

    def get_attack_row(self):
        return self.get_transition_matrix()[0]

    def get_block_row(self):
        return self.get_transition_matrix()[1]

    def get_heal_row(self):
        return self.get_transition_matrix()[2]

    def set_attack_row(self, attack_row):
        self.transition_matrix[0] = attack_row

    def set_block_row(self, block_row):
        self.transition_matrix[1] = block_row

    def set_heal_row(self, heal_row):
        self.transition_matrix[2] = heal_row

    def choose_action(self):
        # В соответствии с матрицей переходов выбираем действие
        actions = ["attack", "block", "heal"]
        probabilities = self.transition_matrix[self.current_action]
        action = random.choices(actions, weights=probabilities, k=1)[0]
        self.current_action = actions.index(action)

class Player(Unit):
    def choose_action(self):
        # Пользователь выбирает действие
        while True:
            print("Выберите действие:")
            print("\033[32m1\033[0m. Атаковать")
            print("\033[32m2\033[0m. Блокировать атаку")
            print("\033[32m3\033[0m. Восстановить здоровье")
            choice = input("Введите номер действия: ")
            if choice in ['1', '2', '3']:
                self.current_action = int(choice) - 1
                return
            else:
                print("Некорректный ввод. Попробуйте снова.")

def main():
    # Характеристики юнитов и матрица переходов для бота
    player = Player("Игрок", 100, 20, 10, 30)
    mtx = np.array([[0.7, 0.2, 0.1],
                   [0.8, 0.05, 0.15],
                   [0.65, 0.05, 0.3]])
    bot = Bot("Бот", 100, 15, 5, 25, mtx)

    bot.attack(player)

    # Игровой цикл
    while not player.is_dead() and not bot.is_dead():

        # Ход игрока
        player.choose_action()
        if player.get_current_action() == 0:
            player.attack(bot)
        elif player.get_current_action() == 1:
            player.block_attack(bot)
        else:
            player.heal()

        if bot.is_dead():
            print("\033[32mИгрок победил!\033[0m")
            break

        # Проверка на победу игрока после его хода

        # Ход бота
        bot.choose_action()
        if bot.get_current_action() == 0:
            bot.attack(player)
        elif bot.get_current_action() == 1:
            bot.block_attack(player)
        else:
            bot.heal()

        # Проверка на победу бота после его хода
        if player.is_dead():
            print("\033[32mБот победил!\033[0m")
            break

if __name__ == "__main__":
    main()
