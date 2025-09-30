from labyrinth_game.player_actions import get_input
from labyrinth_game.utils import describe_current_room

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}


def main():
    print('Добро пожаловать в Лабиринт сокровищ!')
    describe_current_room(game_state)
    while not game_state['game_over']:
        command = get_input("> ")
        if command == 'exit':
            print("\nВыход из игры.")
            game_state['game_over'] = True


if __name__ == "__main__":
    main()
