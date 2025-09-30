from labyrinth_game.constants import ROOMS


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
