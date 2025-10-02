import math

from labyrinth_game.constants import (
    COMMANDS,
    EVENT_PROBABILITY,
    FIND_COIN_EVENT,
    PSEUDO_RANDOM_MULTIPLIER,
    PSEUDO_RANDOM_SPREAD,
    ROOMS,
    SCARE_EVENT,
    TRAP_DAMAGE_MODULO,
    TRAP_DEATH_THRESHOLD,
    TRAP_EVENT,
    TRAP_EVENT_TYPE_MODULO,
)


def describe_current_room(game_state):
    """Описание комнаты"""
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
    """Решение загадок"""
    room_name = game_state['current_room']
    puzzle = ROOMS[room_name]['puzzle']
    if room_name == 'treasure_room':
        attempt_open_treasure(game_state)
        return
    if puzzle:
        print(puzzle[0])
        answer = input('Введите овтет: ').strip().lower()
        ok = False
        if puzzle[1] == '10':
            if answer in ['10', 'десять']:
                ok = True
        else:
            if answer == puzzle[1].lower():
                ok = True
        
        if ok:
            print("Вы успешно решили загадку!")
            ROOMS[room_name]['puzzle'] = None

            if room_name == 'hall':
                reward = 'treasure_key'
            elif room_name == 'library':
                reward = 'rusty_key'
            elif room_name == 'trap_room':
                reward == 'treasure_key'
            elif room_name == 'armory':
                reward == 'rusty_key'

            if reward not in game_state['player_inventory']:
                game_state['player_inventory'].append(reward)
                print(f"Вы получили награду: {reward}")
        else:
            print("Неверно. Попробуйте снова.")
            if room_name == 'trap_room':
                trigger_trap(game_state)
    else:
        print('Загадок здесь нет.')


def attempt_open_treasure(game_state):
    """Открытие суперского кейса, который даёт победу"""
    room = ROOMS[game_state['current_room']]
    items = room['items']
    inventory = game_state['player_inventory']

    # Я не понял, нужно это или нет.
    # if ('treasure_chest' not in items and 'treasure_chest' not in inventory):
    #     print("Сундук уже открыт или отсутствует.")
    #     return
    
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        items.remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
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
                if 'treasure_chest' in items:
                    items.remove('treasure_chest')
                game_state['game_over'] = True
            else:
                print('Неверный код!')
        else:
            print('Вы отступаете от сундука.')


def show_help(commands: dict = COMMANDS):
    """Помощь игроку в командах"""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")


def pseudo_random(seed, modulo):
    """Псевдо рандом, хотя и нет"""
    x = math.sin(seed * PSEUDO_RANDOM_MULTIPLIER) * PSEUDO_RANDOM_SPREAD
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state):
    """Логика ловушек"""
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    seed = game_state['steps_taken']
    if inventory:
        idx_for_delete_item = pseudo_random(seed, len(inventory))
        name_of_deleted_item = inventory.pop(idx_for_delete_item)
        print(f"Вы потеряли предмет: {name_of_deleted_item}!")
    else:
        damage_roll = pseudo_random(seed, TRAP_DAMAGE_MODULO)
        if damage_roll < TRAP_DEATH_THRESHOLD:
            print("Вы попали в ловушку и не выжили. Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Ловушка сработала, но вы живы.")


def random_event(game_state: dict):
    """Случайное событие, которые как бы не случайное"""
    room = game_state['current_room']
    steps =  game_state['steps_taken']
    current_room = ROOMS[room]
    if pseudo_random(steps, EVENT_PROBABILITY) != 0:
        return

    event_type = pseudo_random(steps + 1, TRAP_EVENT_TYPE_MODULO)

    if event_type == FIND_COIN_EVENT: # Находка монетки
        print("Вы находите на полу монетку.")
        current_room['items'].append('coin')

    elif event_type == SCARE_EVENT: # Испуг
        print("Вы слышите шорох. Вам должно быть страшно.")
        if 'sword' in game_state['player_inventory']:
            print("Но ваш меч отпугнул существо.")

    elif event_type == TRAP_EVENT:  # Ловушка
        if (room == 'trap_room'
            and 'torch' not in game_state['player_inventory']):
            print("Опасность! Ловушка может сработать.")
            trigger_trap(game_state)