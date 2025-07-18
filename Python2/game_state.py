from player import Player

class GameState:

    def __init__(self, input_dict):

        self.dict_to_object(input_dict)

    def dict_to_object(self, input_dict):

        self.player1 = Player(input_dict['p1'])
        self.player2 = Player(input_dict['p2'])
        self.timer = input_dict['timer']
        self.fight_result = input_dict['result']
        self.has_round_started = input_dict['round_started']
        self.is_round_over = input_dict['round_over']

class GameState:
    def __init__(self, input_dict):
        self.dict_to_object(input_dict)

    def dict_to_object(self, input_dict):
        # Initialize player objects
        self.player1 = Player(input_dict['p1'])
        self.player2 = Player(input_dict['p2'])
        # Extract game-related state data
        self.timer = input_dict['timer']
        self.fight_result = input_dict['result']
        self.has_round_started = input_dict['round_started']
        self.is_round_over = input_dict['round_over']


    def to_dict(self):
        # Convert the GameState object back to a dictionary form
        state_dict = {
            # General game state features
            # 'timer': self.timer,w
            'fight_result': 1 if self.fight_result == 'OVER' else 0,
            'has_round_started': 1 if self.has_round_started == 'STARTED' else 0,
            'is_round_over': 1 if self.is_round_over == 'OVER' else 0,

            # # Player 1 features
            'Player1_ID': self.player1.player_id,
            'health': self.player1.health  ,
            'x_coord': self.player1.x_coord - self.player2.x_coord,
            'y_coord': self.player1.y_coord - self.player2.y_coord,
            'is_jumping': int(self.player1.is_jumping),
            'is_crouching': int(self.player1.is_crouching),
            'is_player_in_move': int(self.player1.is_player_in_move),
            'move_id': self.player1.move_id,
            'player1_buttons up': int(self.player1.player_buttons.up),
            'player1_buttons down': int(self.player1.player_buttons.down),
            'player1_buttons right': int(self.player1.player_buttons.right),
            'player1_buttons left': int(self.player1.player_buttons.left),
            'player1.player_buttons.A': int(self.player1.player_buttons.A),
            'player1.player_buttons.B': int(self.player1.player_buttons.B),
            'player1.player_buttons.Y': int(self.player1.player_buttons.Y),
            # 'player1.player_buttons.X': self.player1.player_buttons.X,
            'player1.player_buttons.R': int(self.player1.player_buttons.R),
            'player1.player_buttons.L': int(self.player1.player_buttons.L),

            # Player 2 features
            'Player2_ID': self.player2.player_id,
            'Player2 health': self.player2.health,
            # 'Player2 x_coord': self.player2.x_coord,
            # 'Player2 y_coord': self.player2.y_coord,
            'Player2 is_jumping': int(self.player2.is_jumping),
            'Player2 is_crouching': int(self.player2.is_crouching),
            'Player2 is_player_in_move': int(self.player2.is_player_in_move),
            'Player2 move_id': self.player2.move_id
        }
        return state_dict