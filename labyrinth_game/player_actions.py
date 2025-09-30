def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print(inventory)
    else:
        print('Интвентарь пуст')


def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"