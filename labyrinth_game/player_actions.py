from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import (
    describe_current_room,
    random_event,
)


def get_input(prompt="> "):
    """Функция отлова сообщений игрока"""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    """Функция, которая показывает инвентарь игрока"""
    inventory = game_state['player_inventory']
    if inventory:
        print(inventory)
    else:
        print('Интвентарь пуст')


def move_player(game_state, direction):
    """Функция, которая перемещает игрока"""
    current_room = game_state['current_room']
    exits = ROOMS[current_room]['exits']
    if direction in exits:
        if exits[direction] == 'treasure_room':
            if 'rusty_key' not in game_state['player_inventory']:
                print('Дверь заперта. Нужен ключ, чтобы пройти дальше.')
                return
            else:
                print('Вы используете найденный ключ, ' \
                'чтобы открыть путь в комнату сокровищ.')
                game_state['current_room'] = exits[direction]
                game_state['steps_taken'] += 1
                describe_current_room(game_state)
                random_event(game_state)
        else:
            game_state['current_room'] = exits[direction]
            game_state['steps_taken'] += 1
            describe_current_room(game_state)
            random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Логика подбора предметов из комнат"""
    current_room = game_state['current_room']
    items = ROOMS[current_room]['items']
    if item_name in items:
        if item_name == 'treasure_chest':
            print('Вы не можете поднять сундук, он слишком тяжелый.')
        game_state['player_inventory'].append(item_name)
        ROOMS[current_room]['items'].remove(item_name)
        print(f'Вы подняли: {item_name}')
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """Логика использования предметов"""
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return
    if item_name == 'torch':
        print("Cтало светлее.")
    elif item_name == 'sword':
        print("Вы стали увереннее в себе")
    elif item_name == 'bronze box':
        print("Вы открыли бронзовую шкатулку.")
        if 'rusty_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty_key')
        else:
            return
    # Я так понял, что это убрали. 
    # elif item_name in ['treasure_chest']:
    #     attempt_open_treasure(game_state)
    else:
        print("Вы не знаете, как использовать этот предмет.")