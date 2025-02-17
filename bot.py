import argparse
import json
import os

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0
attackTo = 'attackTo.txt'  # isi file : <x>;<y>;<direction>;
attacked = 'attacked.txt'  # isi file: <nilai i>


def write_file(x, y, direction):
    f_out = open(attackTo, 'w')
    f_out.write("{};{};{};".format(x, y, direction))
    f_out.close()


# ------Ini buat nyatet pertama kali dia serang, biar bisa backtrack-------
def write_i(i):
    f_out = open(attacked, 'w')
    f_out.write(str(i))
    f_out.close()


def read_file():
    f_in = open(attackTo, 'r')
    for char in f_in:
        fields = char.split(';')
        x = int(fields[0])
        y = int(fields[1])
        direction = fields[2]
    f_in.close()
    return (x, y, direction)


def read_i():
    f_in = open(attacked, 'r')
    i = f_in.read()
    i = int(i)
    f_in.close()
    return i


def main(player_key):
    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        # hapus file eksternal saat phase1 (jika ada)
        if (os.path.isfile(attackTo)):
            os.remove(attackTo)
        if (os.path.isfile(attacked)):
            os.remove(attacked)
        place_ships()
    else:
        if state['Round'] == 19:
            if (map_size % 2 == 0):
                xs, ys = map_size // 2, map_size // 2 - 1
            else:
                xs, ys = map_size // 2, map_size // 2
            output_spec(xs, ys, 4)
        elif state['Round'] == 33:
            if map_size % 2 == 0:
                xs, ys = map_size - 2, 1
                output_spec(xs, ys, 4)
            else:
                xs, ys = map_size - 2, 1
                output_spec(xs, ys, 3)
        elif state['Round'] == 49:
            xs, ys = map_size - 2, map_size - 2
            output_spec(xs, ys, 5)
        elif state['Round'] == 63:
            output_spec(2 , map_size - 2, 7)
        else:
            greedy(state['OpponentMap']['Cells'])


# def fire_shot(opponent_map):
#     # To send through a command please pass through the following <code>,<x>,<y>
#     targets = []
#     for cell in opponent_map:
#         if not cell['Damaged'] and not cell['Missed']:
#             valid_cell = cell['X'], cell['Y']
#             targets.append(valid_cell)
#     target = choice(targets)
#     output_shot(*target)
#     return


def greedy(opponent_map):
    # Sementara ini ada dua mode -> 1. Checker Mode , 2. Aggresive Mode (!CheckerMode)
    # Range opponent_map 0 <= x <= 99
    i = 0
    isFoundValid = False
    isCheckerMode = True

    if (os.path.isfile(attackTo)):
        (x, y, direction) = read_file()
        if (direction != 'Unknown'):
            isCheckerMode = False
        if (x != 999):  # dummy x dan y
            i = x * map_size + y
        else:
            i = read_i()

    while (i < (map_size * map_size)) and (not isFoundValid):
        cell = opponent_map[i]

        # Checker Mode
        if (((cell['X'] % 2 == 0) and (cell['Y'] % 2 == 0)) or (
                (cell['X'] % 2 == 1) and (cell['Y'] % 2 == 1)) and isCheckerMode):
            '''
				Check: bila pernah ada kapal yang terkena di titik (x,y) 
					  maka check kanan, kiri, bawah, atas
			'''

            if (not cell['Damaged']) and (not cell['Missed']):
                isFoundValid = True
                valid_cell = cell['X'], cell['Y']
            elif (cell['Damaged']):  # Bila (x,y) pernah hit (pertama kali kena), direction masih 'Unknown'
                write_file(cell['X'], cell['Y'], 'Unknown')

                # check atas
                if (i % map_size) != (map_size - 1):
                    cell_atas = opponent_map[i + 1]
                    if cell_atas['Damaged']:
                        write_i(i)
                        x = int(cell_atas['X'])
                        y = int(cell_atas['Y'])
                        i = x * map_size + y
                        direction = 'North'
                        isCheckerMode = False
                    elif (not cell_atas['Damaged']) and (not cell_atas['Missed']):
                        isFoundValid = True
                        valid_cell = cell_atas['X'], cell_atas['Y']

                # check bawah
                if (i % map_size) != 0 and not (isFoundValid) and isCheckerMode:
                    cell_bawah = opponent_map[i - 1]
                    if cell_bawah['Damaged']:
                        write_i(i)
                        x = int(cell_bawah['X'])
                        y = int(cell_bawah['Y'])
                        i = x * map_size + y
                        direction = 'South'
                        isCheckerMode = False
                    elif (not cell_bawah['Damaged']) and (not cell_bawah['Missed']):
                        isFoundValid = True
                        valid_cell = cell_bawah['X'], cell_bawah['Y']

                # check kiri
                if (i / map_size) >= 1 and not (isFoundValid) and isCheckerMode:
                    cell_kiri = opponent_map[i - map_size]
                    if cell_kiri['Damaged']:
                        write_i(i)
                        x = int(cell_kiri['X'])
                        y = int(cell_kiri['Y'])
                        i = x * map_size + y
                        direction = 'West'
                        isCheckerMode = False
                    elif (not cell_kiri['Damaged']) and (not cell_kiri['Missed']):
                        isFoundValid = True
                        valid_cell = cell_kiri['X'], cell_kiri['Y']

                # check kanan
                if ((i + map_size) < (map_size * map_size)) and not (isFoundValid) and isCheckerMode:
                    cell_kanan = opponent_map[i + map_size]
                    if cell_kanan['Damaged']:
                        write_i(i)
                        x = int(cell_kanan['X'])
                        y = int(cell_kanan['Y'])
                        i = x * map_size + y
                        direction = 'East'
                        isCheckerMode = False
                    elif (not cell_kanan['Damaged']) and (not cell_kanan['Missed']):
                        isFoundValid = True
                        valid_cell = cell_kanan['X'], cell_kanan['Y']

        # !CheckerMode -> Aggresive Mode (Nyerang beruntun sesuai direction yang ada & direction ga mungkin 'Unknown')
        if (not isCheckerMode):
            if (direction == 'North'):
                if (i % map_size == (map_size - 1)):
                    isCheckerMode = True
                else:
                    if (opponent_map[i]['Missed']):
                        isCheckerMode = True
                        write_i(i)
                    else:
                        i += 1
            elif (direction == 'West'):
                if (i / map_size) < 1:
                    isCheckerMode = True
                else:
                    if (opponent_map[i]['Missed']):
                        isCheckerMode = True
                    else:
                        i -= map_size
            elif (direction == 'East'):
                if ((i + map_size) >= (map_size * map_size)):
                    isCheckerMode = True
                else:
                    if (opponent_map[i]['Missed']):
                        isCheckerMode = True
                    else:
                        i += map_size
            elif (direction == 'South'):
                if (i % map_size == 0):
                    isCheckerMode = True
                else:
                    if (opponent_map[i]['Missed']):
                        isCheckerMode = True
                    else:
                        i -= 1
            if (not isCheckerMode):
                cell = opponent_map[i]
                if (not cell['Damaged'] and not cell['Missed']):
                    write_file(cell['X'], cell['Y'], direction)
                    valid_cell = cell['X'], cell['Y']
                    isFoundValid = True
            else:
                if (direction != 'North'):
                    i = read_i()
                write_file(999, 999, 'Unknown')

        i += 1

    # kalau checker udah habis (ga bisa digunain)
    # Versi 1 (kalau mau diganti sok)
    if (i >= map_size * map_size):
        write_i(99)
        j = 0
        isFoundValid = False

        # nyari sisa kapal musuh yang belum kena kalau belum menang
        while (j < map_size * map_size) and not isFoundValid:
            cell = opponent_map[j]

            if not cell['Damaged'] and not cell['Missed']:
                # check atas ada kapal yang kena atau ga
                if ((i % map_size) != (map_size - 1)):
                    cell_atas = opponent_map[j + 1]
                    if (cell_atas['Damaged']):
                        isFoundValid = True
                        valid_cell = cell['X'], cell['Y']

                # check bawah ada kapal yang kena atau ga
                if ((i % map_size) != (map_size - 1)) and not isFoundValid:
                    cell_bawah = opponent_map[j - 1]
                    if (cell_bawah['Damaged']):
                        isFoundValid = True
                        valid_cell = cell['X'], cell['Y']

                # check kiri ada kapal yang kena atau ga
                if (i / map_size) >= 1 and not isFoundValid:
                    cell_kiri = opponent_map[j - 10]
                    if (cell_kiri['Damaged']):
                        isFoundValid = True
                        valid_cell = cell['X'], cell['Y']

                # check kanan ada kapal yang kena atau ga
                if (i + map_size) < (map_size * map_size) and not isFoundValid:
                    cell_kanan = opponent_map[j + 10]
                    if (cell_kanan['Damaged']):
                        isFoundValid = True
                        valid_cell = cell['X'], cell['Y']
            j += 1

    output_spec(*valid_cell, 1)
    return

def output_spec(x, y, mv):
    # Possible code buat nembak (ganti nilai move):
    # (Berapa Energy-nya, Kapal apa yang bisa gunain)

    # (Energy = 0)                    0 = Do Nothing
    # (Energy = 1 , All Ships)        1 = fire shot - Fires a shot given a center location
    # (Energy = 24, Destroyer)        2 = fire double shot vertical
    # (Energy = 30, Carrier)          3 = fire corner shot horizontal - Fires two shots given a center location
    # (Energy = 30, Carrier)          4 = fire corner shot - Fires four shots given a center location
    # (Energy = 42, Cruiser)          4 = fire horizontal cross shot - Fires five shots given a center location
    # (Energy = 36, Battleship)       5 = fire diagonal cross shot - Fires five shots given a center location
    # (Energy = 36, Submarine)        6 = fire seeker missile - Finds the nearst ship with an euclidian distance of 2 units or less away, given a center location
    # (Energy = ?)                    8 = place shield
    '''
    #Shield Rules (Placement):
    :param <x: pos>:
    :param <y: pos>:
    To Place a shield you have to pass through the following command:
        8,<x:pos>,<y:pos> where the x and y pos are the center points of the shield.
    When a shield is hit, it will show an '@' symbol where the shot landed on the respective map while the shield is active.
    When the shield expires there will be no history where any shots landed.
    '''
    move = mv
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass


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
