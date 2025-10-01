from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import describe_current_room, solve_puzzle


def process_command(game_state, command_line):
    parts = command_line.strip().split()
    if not parts:
        return
    cmd, *args = parts
    arg = ' '.join(args)
    match cmd:
        case 'look':
            describe_current_room(game_state)
        case 'inventory':
            show_inventory(game_state)
        case 'go':
            move_player(game_state, arg)
        case 'take':
            take_item(game_state, arg)
        case 'use':
            use_item(game_state, arg)
        case 'solve':
            solve_puzzle(game_state)
        case 'quit' | 'exit':
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите help для списка команд.")
            
    
def main():
    game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
    }

    print('Добро пожаловать в Лабиринт сокровищ!')
    describe_current_room(game_state)
    while not game_state['game_over']:
        command = get_input("> ")
        process_command(game_state, command)



if __name__ == "__main__":
    main()
