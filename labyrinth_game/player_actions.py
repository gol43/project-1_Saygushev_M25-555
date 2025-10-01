from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import attempt_open_treasure, describe_current_room


def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print(inventory)
    else:
        print('Интвентарь пуст')


def move_player(game_state, direction):
    current_room = game_state['current_room']
    exits = ROOMS[current_room]['exits']
    if direction in exits:
        game_state['current_room'] = exits[direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    current_room = game_state['current_room']
    items = ROOMS[current_room]['items']
    if item_name in items:
        game_state['player_inventory'].append(item_name)
        ROOMS[current_room]['items'].remove(item_name)
        print(f'Вы подняли: {item_name}')
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return
    if item_name == 'torch':
        print("Cтало светлее.")
    elif item_name == 'sword':
        print("Вы стали увереннее в себе")
    elif item_name == 'bronze box':
        print("Вы открыли бронзовую шкатулку.")
        if 'rusty key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty key')
        else:
            return
    elif item_name in ['treasure chest']:
        attempt_open_treasure(game_state)
    else:
        print("Вы не знаете, как использовать этот предмет.")