import xml.etree.ElementTree as ET
import json
import csv

def extract_player_info(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    players_info = []
    
    for group in root.findall(".//Group"):
        group_name = group.get('Event')
        for player in group.findall(".//Player"):
            born_date = player.get('Born')
            if born_date:
                if born_date == '1899.12.30':
                    born_date = ""
                else:
                    born_date = f"{born_date[8:10]}.{born_date[5:7]}.{born_date[0:4]}"
            player_info = {
                'fornavn': player.get('Gn'),
                'etternavn': player.get('Ln'),
                'navn': f"{player.get('Gn')} {player.get('Ln')}",
                'fodt': born_date,
                'epost': player.get('Email'),
                'mobil': player.get('Phone'),
                't_gruppe': group_name,
                'gruppe': player.get('Group'),
                'club': player.get('Club')
            }
            players_info.append(player_info)
    
    return players_info

def save_as_json(players_info, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(players_info, f, ensure_ascii=False, indent=4)

def save_as_csv(players_info, output_file):
    keys = players_info[0].keys()
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(players_info)

if __name__ == "__main__":
    FILE = 'eksempel'
    xml_file = FILE + '.xml'

    players_info = extract_player_info(xml_file)
    save_as_csv(players_info, FILE + '.csv')
    save_as_json(players_info, FILE + '.json')
    
    print(f"Player information saved to {FILE}.json and .csv")
