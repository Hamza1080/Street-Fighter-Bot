from command import Command
import numpy as np
from buttons import Buttons
import csv
import os
import keyboard  # pip install keyboard
import joblib
import pandas as pd


# def datatocsv(current_game_state, csv_file='dataset\\game_data.csv'):
#     # Prepare the row of data
#     row = [
#         current_game_state.timer,
#         current_game_state.fight_result,
#         current_game_state.has_round_started,
#         current_game_state.is_round_over,

#         current_game_state.player1.player_id,
#         current_game_state.player1.health,
#         current_game_state.player1.x_coord,
#         current_game_state.player1.y_coord,
#         current_game_state.player1.is_jumping,
#         current_game_state.player1.is_crouching,
#         current_game_state.player1.is_player_in_move,
#         current_game_state.player1.move_id,
#         int(current_game_state.player1.player_buttons.up),
#         int(current_game_state.player1.player_buttons.down),
#         int(current_game_state.player1.player_buttons.right),
#         int(current_game_state.player1.player_buttons.left),
#         int(current_game_state.player1.player_buttons.A),
#         int(current_game_state.player1.player_buttons.B),
#         int(current_game_state.player1.player_buttons.Y),
#         int(current_game_state.player1.player_buttons.R),
#         int(current_game_state.player1.player_buttons.L),

#         current_game_state.player2.player_id,
#         current_game_state.player2.health,
#         current_game_state.player2.x_coord,
#         current_game_state.player2.y_coord,
#         current_game_state.player2.is_jumping,
#         current_game_state.player2.is_crouching,
#         current_game_state.player2.is_player_in_move,
#         current_game_state.player2.move_id,
#         int(current_game_state.player2.player_buttons.up),
#         int(current_game_state.player2.player_buttons.down),
#         int(current_game_state.player2.player_buttons.right),
#         int(current_game_state.player2.player_buttons.left),
#         int(current_game_state.player2.player_buttons.A),
#         int(current_game_state.player2.player_buttons.B),
#         int(current_game_state.player2.player_buttons.Y),
#         int(current_game_state.player2.player_buttons.R),
#         int(current_game_state.player2.player_buttons.L)
#     ]

#     header = [
#         'timer', 'fight_result', 'has_round_started', 'is_round_over',

#         # Player 1 state
#         'Player1_ID', 'Player1_health', 'Player1_x_coord', 'Player1_y_coord',
#         'Player1_is_jumping', 'Player1_is_crouching', 'Player1_is_player_in_move', 'Player1_move_id',
#         'Player1_button_up', 'Player1_button_down', 'Player1_button_right', 'Player1_button_left',
#         'Player1_button_A', 'Player1_button_B', 'Player1_button_Y', 'Player1_button_R', 'Player1_button_L',

#         # Player 2 state
#         'Player2_ID', 'Player2_health', 'Player2_x_coord', 'Player2_y_coord',
#         'Player2_is_jumping', 'Player2_is_crouching', 'Player2_is_player_in_move', 'Player2_move_id',
#         'Player2_button_up', 'Player2_button_down', 'Player2_button_right', 'Player2_button_left',
#         'Player2_button_A', 'Player2_button_B', 'Player2_button_Y', 'Player2_button_R', 'Player2_button_L'
#     ]


#     file_exists = os.path.isfile(csv_file)

#     with open(csv_file, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         if not file_exists:
#             writer.writerow(header)
#         writer.writerow(row)   

button_targets = [
    'player1_buttons up',
    'player1_buttons down',
    'player1_buttons right',
    'player1_buttons left',
    'player1.player_buttons.A',
    'player1.player_buttons.B',
    'player1.player_buttons.Y',
    'player1.player_buttons.R',
    'player1.player_buttons.L'
]
loaded_models = {
    target: joblib.load(f"dataset/saved_models/{target.replace(' ', '_').replace('.', '')}_model.pkl")
    for target in button_targets
}

class Bot:

    def __init__(self):
        #< - v + < - v - v + > - > + Y
        self.fire_code=["<","!<","v+<","!v+!<","v","!v","v+>","!v+!>",">+Y","!>+!Y"]
        self.exe_code = 0
        self.start_fire=True
        self.remaining_code=[]
        self.my_command = Command()
        self.buttn= Buttons()

    # def fight(self, current_game_state, player):
    #     # Convert game state to dictionary
    #     input_data = current_game_state.to_dict()  # Ensure this exists
    #     input_df = pd.DataFrame([input_data])

    #     # Predict each button
    #     predictions = {}
    #     for target in button_targets:
    #         input_features = input_df.drop(columns=[target], errors='ignore')
    #         model = loaded_models[target]
    #         predictions[target] = model.predict(input_features)[0]
    #     print(predictions)
    #     # Reset button state
    #     self.buttn.up = self.buttn.down = self.buttn.left = self.buttn.right = False
    #     self.buttn.Y = self.buttn.A = self.buttn.B = self.buttn.R = self.buttn.L = False

    #     # Build command list based on predicted buttons
    #     command = []

    #     # if predictions['player1_buttons down'] and predictions['player1_buttons left']:
    #     #     command.append("v+<")
    #     # elif predictions['player1_buttons down'] and predictions['player1_buttons right']:
    #     #     command.append("v+>")
    #     # elif predictions['player1_buttons down'] and predictions['player1.player_buttons.R']:
    #     #     command.append("v+R")
    #     # elif predictions['player1_buttons up'] and predictions['player1_buttons right'] and predictions['player1.player_buttons.Y']:
    #     #     command.append(">+^+Y")
    #     # elif predictions['player1_buttons up'] and predictions['player1_buttons.right'] and predictions['player1.player_buttons.B']:
    #     #     command.append(">+^+B")
    #     # elif predictions['player1_buttons up'] and predictions['player1_buttons.right'] and predictions['player1.player_buttons.A']:
    #     #     command.append(">+^+A")
    #     # elif predictions['player1_buttons up'] and predictions['player1_buttons.left'] and predictions['player1.player_buttons.Y']:
    #     #     command.append("<+^+Y")
    #     # elif predictions['player1_buttons up'] and predictions['player1_buttons.left'] and predictions['player1.player_buttons.B']:
    #     #     command.append("<+^+B")

 
    #     if not command:
    #         if predictions['player1_buttons up']:
    #             command.append("^")
    #         elif predictions['player1_buttons down']:
    #             command.append("v")

    #         if predictions['player1_buttons left']:
    #             command.append("<")
    #         elif predictions['player1_buttons right']:
    #             command.append(">")
                
    #         if predictions['player1.player_buttons.Y']:
    #             command.append("Y")
    #         elif predictions['player1.player_buttons.A']:
    #             command.append("A")
    #         elif predictions['player1.player_buttons.B']:
    #             command.append("B")
    #         elif predictions['player1.player_buttons.R']:
    #             command.append("R")
    #         elif predictions['player1.player_buttons.L']:
    #             command.append("L")


    #     current_player = current_game_state.player1 if player == "1" else current_game_state.player2

    #     # Execute command if found
    #     if command:
    #         self.run_command(command, current_player)

    #     # Update button state in command object
    #     if player == "1":
    #         self.my_command.player_buttons = self.buttn
    #     else:
    #         self.my_command.player2_buttons = self.buttn

    #     return self.my_command
    def fight(self, current_game_state, player):
        if not hasattr(self, 'combo_presence_model'):
            self.combo_presence_model = joblib.load("dataset/saved_models/combo_presence_model.pkl")
            self.combo_model = joblib.load("dataset/saved_models/combo_mlp_model.pkl")
            self.combo_scaler = joblib.load("dataset/saved_models/combo_scaler.pkl")

        for attr in vars(self.buttn):
            setattr(self.buttn, attr, False)

        current_player = current_game_state.player1 if player == "1" else current_game_state.player2

        state_dict = current_game_state.to_dict()
        df = pd.DataFrame([state_dict])


        X = df.drop(columns=[col for col in df.columns if 'buttons' in col or col == 'combo_id'])

        proba = self.combo_presence_model.predict_proba(X)[0][1]
        combo_needed = int(proba > 0.004)  

        print("combo needed?", combo_needed)

        if combo_needed:
            X_scaled = self.combo_scaler.transform(X)
            predicted_combo_id = int(self.combo_model.predict(X_scaled)[0])
            print("Predicted combo ID:", predicted_combo_id)

            combo_map = {
                2: [">+^+Y", ">+^+Y", ">+^+Y", "!>+!^+!Y"],
                3: [">", "-", "!>", "v+>", "-", "!v+!>", "v", "-", "!v", "v+<", "-", "!v+!<", "<+Y", "-", "!<+!Y"],
                4: [">+^+B", ">+^+B", "!>+!^+!B"],
                5: ["<+^+B", "<+^+B", "!<+!^+!B"],
                6: ["<+^+Y", "<+^+Y", "!<+!^+!Y"],
                7: ["<+^+B", "<+^+B", "!<+!^+!B"]
            }

            if predicted_combo_id in combo_map:
                self.run_command(combo_map[predicted_combo_id], current_player)
                combo_id = predicted_combo_id
            else:
                combo_id = -1
        else:

            predictions = {}
            for target in button_targets:
                input_features = df.drop(columns=[target], errors='ignore')
                model = loaded_models[target]
                predictions[target] = model.predict(input_features)[0]
            print(predictions)

            command = []

            if predictions['player1_buttons up']:
                command.append("^")
            elif predictions['player1_buttons down']:
                command.append("v")

            if predictions['player1_buttons left']:
                command.append(">")
            elif predictions['player1_buttons right']:
                command.append("<")

            if predictions['player1.player_buttons.Y']:
                command.append("Y")
            elif predictions['player1.player_buttons.A']:
                command.append("A")
            elif predictions['player1.player_buttons.B']:
                command.append("B")
            elif predictions['player1.player_buttons.L']:
                command.append("L")
            elif predictions['player1.player_buttons.R']:
                command.append("R")

            if command:
                self.run_command(command, current_player)

        self.my_command.player_buttons = self.buttn

        return self.my_command


    # def fight(self, current_game_state, player):

    #     # Load models once
    #     if not hasattr(self, 'combo_presence_model'):
    #         self.combo_presence_model = joblib.load("dataset/saved_models/combo_presence_model.pkl")
    #         self.combo_model = joblib.load("dataset/saved_models/combo_mlp_model.pkl")
    #         self.combo_scaler = joblib.load("dataset/saved_models/combo_scaler.pkl")

    #     # Reset button states
    #     for attr in vars(self.buttn):
    #         setattr(self.buttn, attr, False)

    #     current_player = current_game_state.player1 if player == "1" else current_game_state.player2

    #     # Convert game state to dataframe
    #     state_dict = current_game_state.to_dict()
    #     df = pd.DataFrame([state_dict])

    #     # Drop button and combo columns for prediction
    #     X = df.drop(columns=[col for col in df.columns if 'buttons' in col or col == 'combo_id'])

    #     # Predict whether a combo is needed
    #     # Get the predicted probability for class 1 (combo needed)
    #     proba = self.combo_presence_model.predict_proba(X)[0][1]

    #     # Use a low threshold to favor predicting 1 (combo needed)
    #     combo_needed = int(proba > 0.02)  # You can tweak the threshold

    #     print("combo needed?",combo_needed)
    #     if combo_needed:
    #         # Predict the combo ID
    #         X_scaled = self.combo_scaler.transform(X)
    #         predicted_combo_id = int(self.combo_model.predict(X_scaled)[0])
    #         print("Predicted combo ID:", predicted_combo_id)

    #         # Map predicted combo ID to actual combo sequence
    #         combo_map = {
    #             2: [">+^+Y",">+^+Y",">+^+Y","!>+!^+!Y"],
    #             3: [">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],
    #             4: [">+^+B",">+^+B","!>+!^+!B"],
    #             5: ["<+^+B","<+^+B","!<+!^+!B"],
    #             6: ["<+^+Y", "<+^+Y", "!<+!^+!Y"],
    #             7: ["<+^+B", "<+^+B", "!<+!^+!B"]
    #         }

    #         if predicted_combo_id in combo_map:
    #             self.run_command(combo_map[predicted_combo_id], current_player)
    #             combo_id = predicted_combo_id
    #         else:
    #             combo_id = -1
    #     else:
    #         combo_id = -1
    #         # Example: Basic reaction if not using model
    #         if state_dict['Player2 is_jumping'] == 1:
    #             self.buttn.up = True
    #         if state_dict['Player2 is_crouching'] == 1:
    #             self.buttn.down = True
    #         # Extend logic or use another model for fine-grained button prediction

    #     # Apply button command
    #     if player == "1":
    #         self.my_command.player_buttons = self.buttn
    #         # datatocsv(current_game_state, combo_id)
    #     else:
    #         self.my_command.player2_buttons = self.buttn

    #     return self.my_command


    # def fight(self, current_game_state, player):
    #     datatocsv(current_game_state)

    #     # Reset all button states
    #     self.buttn.up = False
    #     self.buttn.down = False
    #     self.buttn.left = False
    #     self.buttn.right = False
    #     self.buttn.Y = False
    #     self.buttn.A = False
    #     self.buttn.B = False
    #     self.buttn.R = False
    #     self.buttn.L = False

    #     current_player = current_game_state.player1 if player == "1" else current_game_state.player2

    #     if self.exe_code != 0:
    #         self.run_command([], current_player)

    #     command = []

    #     # Check for combo inputs first
    #     if keyboard.is_pressed('down') and keyboard.is_pressed('left'):
    #         command.append("v+<")
    #     elif keyboard.is_pressed('down') and keyboard.is_pressed('right'):
    #         command.append("v+>")
    #     elif keyboard.is_pressed('down') and keyboard.is_pressed('r'):
    #         command.append("v+R")
    #     elif keyboard.is_pressed('right') and keyboard.is_pressed('up') and keyboard.is_pressed('y'):
    #         command.append(">+^+Y")
    #     elif keyboard.is_pressed('right') and keyboard.is_pressed('up') and keyboard.is_pressed('b'):
    #         command.append(">+^+B")
    #     elif keyboard.is_pressed('right') and keyboard.is_pressed('up') and keyboard.is_pressed('a'):
    #         command.append(">+^+A")
    #     elif keyboard.is_pressed('left') and keyboard.is_pressed('up') and keyboard.is_pressed('y'):
    #         command.append("<+^+Y")
    #     elif keyboard.is_pressed('left') and keyboard.is_pressed('up') and keyboard.is_pressed('b'):
    #         command.append("<+^+B")
    #     else:
    #         # Single key inputs: update buttons directly
    #         if keyboard.is_pressed('down'): self.buttn.down = True
    #         if keyboard.is_pressed('up'): self.buttn.up = True
    #         if keyboard.is_pressed('left'): self.buttn.left = True
    #         if keyboard.is_pressed('right'): self.buttn.right = True
    #         if keyboard.is_pressed('a'): self.buttn.Y = True
    #         if keyboard.is_pressed('b'): self.buttn.A = True
    #         if keyboard.is_pressed('z'): self.buttn.B = True
    #         if keyboard.is_pressed('w'): self.buttn.R = True
    #         if keyboard.is_pressed('e'): self.buttn.L = True

    #     # Run command if there is one
    #     if command:
    #         self.run_command(command, current_player)

    #     # Update player button state
    #     if player == "1":
    #         self.my_command.player_buttons = self.buttn
    #     else:
    #         self.my_command.player2_buttons = self.buttn

    #     return self.my_command

    # def fight(self,current_game_state,player):
    #     #python Videos\gamebot-competition-master\PythonAPI\controller.py 1

    #     #call a function that can save data to csv here just need to send current_game_state :)
    #     datatocsv(current_game_state)

    #     if player=="1":
    #         #print("1").
    #         #v - < + v - < + B spinning

    #         if( self.exe_code!=0  ):
    #            self.run_command([],current_game_state.player1)
    #         diff=current_game_state.player2.x_coord - current_game_state.player1.x_coord
    #         if (  diff > 60 ) :
    #             toss=np.random.randint(3)
    #             if (toss==0):
    #                 #self.run_command([">+^+Y",">+^+Y",">+^+Y","!>+!^+!Y"],current_game_state.player1)
    #                 self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player1)
    #             elif ( toss==1 ):
    #                 self.run_command([">+^+B",">+^+B","!>+!^+!B"],current_game_state.player1)
    #             else: #fire
    #                 self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player1)
    #         elif (  diff < -60 ) :
    #             toss=np.random.randint(3)
    #             if (toss==0):#spinning
    #                 #self.run_command(["<+^+Y","<+^+Y","<+^+Y","!<+!^+!Y"],current_game_state.player1)
    #                 self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player1)
    #             elif ( toss==1):#
    #                 self.run_command(["<+^+B","<+^+B","!<+!^+!B"],current_game_state.player1)
    #             else: #fire
    #                 self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player1)
    #         else:
    #             toss=np.random.randint(2)  # anyFightActionIsTrue(current_game_state.player2.player_buttons)
    #             if ( toss>=1 ):
    #                 if (diff>0):
    #                     self.run_command(["<","<","!<"],current_game_state.player1)
    #                 else:
    #                     self.run_command([">",">","!>"],current_game_state.player1)
    #             else:
    #                 self.run_command(["v+R","v+R","v+R","!v+!R"],current_game_state.player1)
    #         self.my_command.player_buttons=self.buttn

    #     elif player=="2":

    #         if( self.exe_code!=0  ):
    #            self.run_command([],current_game_state.player2)
    #         diff=current_game_state.player1.x_coord - current_game_state.player2.x_coord
    #         if (  diff > 60 ) :
    #             toss=np.random.randint(3)
    #             if (toss==0):
    #                 #self.run_command([">+^+Y",">+^+Y",">+^+Y","!>+!^+!Y"],current_game_state.player2)
    #                 self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player2)
    #             elif ( toss==1 ):
    #                 self.run_command([">+^+B",">+^+B","!>+!^+!B"],current_game_state.player2)
    #             else:
    #                 self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player2)
    #         elif ( diff < -60 ) :
    #             toss=np.random.randint(3)
    #             if (toss==0):
    #                 #self.run_command(["<+^+Y","<+^+Y","<+^+Y","!<+!^+!Y"],current_game_state.player2)
    #                 self.run_command(["<","-","!<","v+<","-","!v+!<","v","-","!v","v+>","-","!v+!>",">+Y","-","!>+!Y"],current_game_state.player2)
    #             elif ( toss==1):
    #                 self.run_command(["<+^+B","<+^+B","!<+!^+!B"],current_game_state.player2)
    #             else:
    #                 self.run_command([">","-","!>","v+>","-","!v+!>","v","-","!v","v+<","-","!v+!<","<+Y","-","!<+!Y"],current_game_state.player2)
    #         else:
    #             toss=np.random.randint(2)  # anyFightActionIsTrue(current_game_state.player2.player_buttons)
    #             if ( toss>=1 ):
    #                 if (diff<0):
    #                     self.run_command(["<","<","!<"],current_game_state.player2)
    #                 else:
    #                     self.run_command([">",">","!>"],current_game_state.player2)
    #             else:
    #                 self.run_command(["v+R","v+R","v+R","!v+!R"],current_game_state.player2)
    #         self.my_command.player2_buttons=self.buttn
    #     return self.my_command



    def run_command( self , com , player   ):

        if self.exe_code-1==len(self.fire_code):
            self.exe_code=0
            self.start_fire=False
            # print ("compelete")
            #exit()
            # print ( "left:",player.player_buttons.left )
            # print ( "right:",player.player_buttons.right )
            # print ( "up:",player.player_buttons.up )
            # print ( "down:",player.player_buttons.down )
            # print ( "Y:",player.player_buttons.Y )

        elif len(self.remaining_code)==0 :

            self.fire_code=com
            #self.my_command=Command()
            self.exe_code+=1

            self.remaining_code=self.fire_code[0:]

        else:
            self.exe_code+=1
            if self.remaining_code[0]=="v+<":
                self.buttn.down=True
                self.buttn.left=True
                # print("v+<")
            elif self.remaining_code[0]=="!v+!<":
                self.buttn.down=False
                self.buttn.left=False
                # print("!v+!<")
            elif self.remaining_code[0]=="v+>":
                self.buttn.down=True
                self.buttn.right=True
                # print("v+>")
            elif self.remaining_code[0]=="!v+!>":
                self.buttn.down=False
                self.buttn.right=False
                # print("!v+!>")

            elif self.remaining_code[0]==">+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.right=True
                # print(">+Y")
            elif self.remaining_code[0]=="!>+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.right=False
                # print("!>+!Y")

            elif self.remaining_code[0]=="<+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.left=True
                # print("<+Y")
            elif self.remaining_code[0]=="!<+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.left=False
                # print("!<+!Y") 

            elif self.remaining_code[0]== ">+^+L" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                # print(">+^+L")
            elif self.remaining_code[0]== "!>+!^+!L" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.L= False #not (player.player_buttons.L)
                # print("!>+!^+!L")

            elif self.remaining_code[0]== ">+^+Y" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                # print(">+^+Y")
            elif self.remaining_code[0]== "!>+!^+!Y" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.Y= False #not (player.player_buttons.L)
                # print("!>+!^+!Y")


            elif self.remaining_code[0]== ">+^+R" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                # print(">+^+R")
            elif self.remaining_code[0]== "!>+!^+!R" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.R= False #ot (player.player_buttons.R)
                # print("!>+!^+!R")

            elif self.remaining_code[0]== ">+^+A" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                # print(">+^+A")
            elif self.remaining_code[0]== "!>+!^+!A" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.A= False #not (player.player_buttons.A)
                # print("!>+!^+!A")

            elif self.remaining_code[0]== ">+^+B" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                # print(">+^+B")
            elif self.remaining_code[0]== "!>+!^+!B" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.B= False #not (player.player_buttons.A)
                # print("!>+!^+!B")

            elif self.remaining_code[0]== "<+^+L" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                # print("<+^+L")
            elif self.remaining_code[0]== "!<+!^+!L" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.L= False  #not (player.player_buttons.Y)
                # print("!<+!^+!L")

            elif self.remaining_code[0]== "<+^+Y" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                # print("<+^+Y")
            elif self.remaining_code[0]== "!<+!^+!Y" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.Y= False  #not (player.player_buttons.Y)
                # print("!<+!^+!Y")

            elif self.remaining_code[0]== "<+^+R" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                # print("<+^+R")
            elif self.remaining_code[0]== "!<+!^+!R" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                # print("!<+!^+!R")

            elif self.remaining_code[0]== "<+^+A" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                # print("<+^+A")
            elif self.remaining_code[0]== "!<+!^+!A" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.A= False  #not (player.player_buttons.Y)
                # print("!<+!^+!A")

            elif self.remaining_code[0]== "<+^+B" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                # print("<+^+B")
            elif self.remaining_code[0]== "!<+!^+!B" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.B= False  #not (player.player_buttons.Y)
                # print("!<+!^+!B")

            elif self.remaining_code[0]== "v+R" :
                self.buttn.down=True
                self.buttn.R= not (player.player_buttons.R)
                # print("v+R")
            elif self.remaining_code[0]== "!v+!R" :
                self.buttn.down=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                # print("!v+!R")

            else:
                if self.remaining_code[0] == "v":
                    self.buttn.down = True
                elif self.remaining_code[0] == "!v":
                    self.buttn.down = False
                elif self.remaining_code[0] == "<":
                    self.buttn.left = True
                elif self.remaining_code[0] == "!<":
                    self.buttn.left = False
                elif self.remaining_code[0] == ">":
                    self.buttn.right = True
                elif self.remaining_code[0] == "!>":
                    self.buttn.right = False
                elif self.remaining_code[0] == "^":
                    self.buttn.up = True
                elif self.remaining_code[0] == "!^":
                    self.buttn.up = False
                elif self.remaining_code[0] == "A":
                    self.buttn.A = True
                elif self.remaining_code[0] == "!A":
                    self.buttn.A = False
                elif self.remaining_code[0] == "B":
                    self.buttn.B = True
                elif self.remaining_code[0] == "!B":
                    self.buttn.B = False
                elif self.remaining_code[0] == "Y":
                    self.buttn.Y = True
                elif self.remaining_code[0] == "!Y":
                    self.buttn.Y = False
                elif self.remaining_code[0] == "R":
                    self.buttn.R = True
                elif self.remaining_code[0] == "!R":
                    self.buttn.R = False
                elif self.remaining_code[0] == "L":
                    self.buttn.L = True
                elif self.remaining_code[0] == "!L":
                    self.buttn.L = False
            self.remaining_code=self.remaining_code[1:]
        return
