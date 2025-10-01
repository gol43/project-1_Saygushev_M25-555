from labyrinth_game.constants import ROOMS
import math


def describe_current_room(game_state):
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    
    print(f'== {room_name.upper()} ==')
    print(room['description'])
    if room['items']:
        print(f'Заметные предметы: {room["items"]}')
    print(f'Выходы: {room["exits"]}')
    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    room_name = game_state['current_room']
    puzzle = ROOMS[room_name]['puzzle']
    if room_name == 'treasure_room':
        attempt_open_treasure(game_state)
        return
    if puzzle:
        print(puzzle[0])
        answer = input('Введите овтет: ').strip().lower()
        if answer == puzzle[1]:
            print("Вы успешно решили загадку!")
            ROOMS[room_name]['puzzle'] = None
            game_state['player_inventory'].append('treasure_key')
        else:
            print("Неверно. Попробуйте снова.")
    else:
        print('Загадок здесь нет.')


def attempt_open_treasure(game_state):
    room = ROOMS[game_state['current_room']]
    items = room['items']
    inventory = game_state['player_inventory']

    if ('treasure chest' not in items and 'treasure chest' not in inventory):
        print("Сундук уже открыт или отсутствует.")
        return
    
    if ('treasure_key' in inventory or 'rusty_key' in inventory):
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        items.remove('treasure chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    message = "Сундук заперт. ... Ввести код? (да/нет)\nВаше решение: "
    answer = input(message).strip().lower()

    if answer == 'да':
        puzzle_text, puzzle_answer = room['puzzle']
        message = (
            "Введите код:\n"
            f"P.S. код это решение загадки:\n{puzzle_text} "
        )
        code = input(message).strip().lower()

        if puzzle_answer and code == puzzle_answer.lower():
            print("Вы открыли сундук с кодом! Победа!")
            if 'treasure chest' in items:
                items.remove('treasure chest')
            game_state['game_over'] = True
        else:
            print('Неверный код!')
    else:
        print('Вы отступаете от сундука.')


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 


def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    seed = game_state['steps_taken']
    if inventory:
        idx_for_delete_item = pseudo_random(seed, len(inventory))
        name_of_deleted_item = inventory.pop(idx_for_delete_item)
        print(f"Вы потеряли предмет: {name_of_deleted_item}!")
    else:
        damage_roll = pseudo_random(seed, 10)
        if damage_roll < 3:
            print("Вы попали в ловушку и не выжили. Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Ловушка сработала, но вы живы.")


def random_event(game_state: dict):
    room = game_state['current_room']
    steps =  game_state['steps_taken']
    current_room = ROOMS[room]
    if pseudo_random(steps, 10) != 0:
        return

    event_type = pseudo_random(steps + 1, 3)

    if event_type == 0: # Находка монетки
        print("Вы находите на полу монетку.")
        current_room['items'].append('coin')

    elif event_type == 1: # Испуг
        print("Вы слышите шорох. Вам должно быть страшно.")
        if 'sword' in game_state['player_inventory']:
            print("Но ваш меч отпугнул существо.")

    elif event_type == 2:  # Ловушка
        if (room == 'trap_room'
            and 'torch' not in game_state['player_inventory']):
            print("Опасность! Ловушка может сработать.")
            trigger_trap(game_state)