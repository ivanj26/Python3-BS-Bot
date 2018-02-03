import argparse
import json
import os
from random import choice

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0


def main(player_key):
    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(state['OpponentMap']['Cells'])


def output_shot(x, y):
    #Possible code buat nembak (ganti nilai move):
    #(Berapa Energy-nya, Kapal apa yang bisa gunain)

    #(Energy = 0)                    0 = Do Nothing
    #(Energy = 1 , All Ships)        1 = fire shot - Fires a shot given a center location
    #(Energy = 8 ronde, Destroyer)   2 = fire double shot vertical
    #(Energy = 10 ronde, Carrier)    3 = fire corner shot horizontal - Fires two shots given a center location
    #(Energy = 10 ronde, Carrier)    4 = fire corner shot - Fires four shots given a center location
    #(Energy = 14 ronde, Cruiser)    5 = fire horizontal cross shot - Fires five shots given a center location
    #(Energy = 12 ronde, Battleship) 6 = fire diagonal cross shot - Fires five shots given a center location
    #(Energy = 10 ronde, Submarine)  7 = fire seeker missile - Finds the nearst ship with an euclidian distance of 2 units or less away, given a center location
    #(Energy = ?)                    8 = place shield

    '''
    #Shield Rules (Placement):
    :param <x: pos>:
    :param <y: pos>:
    To Place a shield you have to pass through the following command:
        8,<x:pos>,<y:pos> where the x and y pos are the center points of the shield.
    When a shield is hit, it will show an '@' symbol where the shot landed on the respective map while the shield is active.
    When the shield expires there will be no history where any shots landed.
    '''

    move = 1
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass


def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    targets = []
    for cell in opponent_map:
        if not cell['Damaged'] and not cell['Missed']:
            valid_cell = cell['X'], cell['Y']
            targets.append(valid_cell)
    target = choice(targets)
    output_shot(*target)
    return


def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    ships = ['Battleship 1 0 north',
             'Carrier 3 1 East',
             'Cruiser 4 2 north',
             'Destroyer 7 3 north',
             'Submarine 1 8 East'
             ]

    with open(os.path.join(output_path, place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
