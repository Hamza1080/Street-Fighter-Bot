import socket
import json
from game_state import GameState
#from bot import fight
import sys
from bot import Bot
import csv
import os

def datatocsv(current_game_state, csv_file='dataset\\game_data.csv'):
    # Prepare the row of data
    row = [
        current_game_state.timer,
        current_game_state.fight_result,
        current_game_state.has_round_started,
        current_game_state.is_round_over,

        current_game_state.player1.player_id,
        current_game_state.player1.health,
        current_game_state.player1.x_coord,
        current_game_state.player1.y_coord,
        current_game_state.player1.is_jumping,
        current_game_state.player1.is_crouching,
        current_game_state.player1.is_player_in_move,
        current_game_state.player1.move_id,
        int(current_game_state.player1.player_buttons.up),
        int(current_game_state.player1.player_buttons.down),
        int(current_game_state.player1.player_buttons.right),
        int(current_game_state.player1.player_buttons.left),

        current_game_state.player2.player_id,
        current_game_state.player2.health,
        current_game_state.player2.x_coord,
        current_game_state.player2.y_coord,
        current_game_state.player2.is_jumping,
        current_game_state.player2.is_crouching,
        current_game_state.player2.is_player_in_move,
        current_game_state.player2.move_id,
        int(current_game_state.player2.player_buttons.up),
        int(current_game_state.player2.player_buttons.down),
        int(current_game_state.player2.player_buttons.right),
        int(current_game_state.player2.player_buttons.left)
    ]

    header = [
        'timer', 'fight_result', 'has_round_started', 'is_round_over',
        'Player1_ID', 'health', 'x_coord', 'y_coord', 'is_jumping', 'is_crouching', 'is_player_in_move', 'move_id',
        'player1_buttons up', 'player1_buttons down', 'player1_buttons right', 'player1_buttons left',
        'Player2_ID', 'Player2 health', 'Player2 x_coord', 'Player2 y_coord', 'Player2 is_jumping',
        'Player2 is_crouching', 'Player2 is_player_in_move', 'Player2 move_id',
        'player2_buttons up', 'player2_buttons down', 'player2_buttons right', 'player2_buttons left'
    ]

    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)   
    return

def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    # print("Waiting to receive data from emulator...")
    pay_load = client_socket.recv(4096)
    # print("Data received.")
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)

    return game_state

def main():
    if (sys.argv[1]=='1'):
        client_socket = connect(9999)
    elif (sys.argv[1]=='2'):
        client_socket = connect(10000)
    current_game_state = None
    #print( current_game_state.is_round_over )
    bot=Bot()

    while (current_game_state is None) or (not current_game_state.is_round_over):

        current_game_state = receive(client_socket)
        # datatocsv(current_game_state)
        bot_command = bot.fight(current_game_state,sys.argv[1])
        # print(current_game_state,sys.argv[1])
        send(client_socket, bot_command)
if __name__ == '__main__':
   main()
