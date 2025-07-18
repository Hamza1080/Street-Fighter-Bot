import csv

def convert_txt_to_csv(txt_file_path, csv_file_path):
    with open(txt_file_path, 'r') as txt_file:
        reader = csv.reader(txt_file, delimiter='\t')
        rows = list(reader)
    
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

# Example usage:
convert_txt_to_csv('current_game_state0.txt', 'gamestate.csv')
