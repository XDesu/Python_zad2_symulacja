import configparser
import argparse

from entity.simulation import Simulation

# problemy do rozwiązania:
# - jak radzimy sobie z ustawieniami domyślnymi?
#   - zmienne w main (brzydkie i chyba trochę nie eleganckie)
#   - domyślne wartości kontruktorów (niebezpieczeństwo, że ktoś może podać None/null)
#   - jakiś plik defaults.py z wartościami domyślnymi (tylko wtedy gdzie go umieścić? Problem struktury folderów)

# czy tworzymy klasę "łąki", która będzie się zajmować iteracją między etapami i tylko udostępniać
# obiekty / informacje już sformatowane, czy przyjmujemy konwencje, że udostępniamy klasy
# i nie obchodzi nas to czy będą dobrze używane

# doci piszemy po polsku czy angielsku?


def load_config(config_file_path: str = ""):
    config = configparser.ConfigParser()
    config.optionxform = str

    if config.read(config_file_path) == []:
        config['Terrain'] = {}
        config['Terrain']['InitPosLimit'] = '10'
        config['Movement'] = {}
        config['Movement']['SheepMoveDist'] = '0.5'
        config['Movement']['WolfMoveDist'] = '1'
        if config_file_path != "":
            with open(config_file_path, 'w') as configfile:
                config.write(configfile)

    InitPosLimit = float(config['Terrain']['InitPosLimit'])
    SheepMoveDist = float(config['Movement']['SheepMoveDist'])
    if (SheepMoveDist < 0.0):
        raise Exception('Sheep Movement distance cannot be negative')
    WolfMoveDist = float(config['Movement']['WolfMoveDist'])
    if (WolfMoveDist < 0.0):
        raise Exception('Wolf Movement distance cannot be negative')

    return InitPosLimit, SheepMoveDist, WolfMoveDist


if __name__ == '__main__':
    rounds = 50
    sheeps = 15
    InitPosLimit, SheepMoveDist, WolfMoveDist = load_config()
    simulation = Simulation(rounds, sheeps, InitPosLimit,
                            SheepMoveDist, WolfMoveDist)
    simulation.start_simulation(False)
