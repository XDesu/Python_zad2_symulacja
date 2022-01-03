import configparser
import argparse

from entity.simulation import Simulation
import logging


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


def setup_logging(log_level: str, log_file_path: str):
    logging_format = '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    date_format = '%Y-%m-%d:%H:%M:%S'

    match log_level:
        case 'DEBUG':
            log_level = logging.DEBUG
        case 'INFO':
            log_level = logging.INFO
        case 'WARNING':
            log_level = logging.WARNING
        case 'ERROR':
            log_level = logging.ERROR
        case 'CRITICAL':
            log_level = logging.CRITICAL
        case _:
            return

    logging.basicConfig(filename=log_file_path,
                        level=log_level, format=logging_format, datefmt=date_format, filemode='w')


parser = argparse.ArgumentParser(
    description='Simulation of sheep and wolf movement')
parser.add_argument(
    '-c', '--config', metavar="FILE", help='configuration file path', default="")
parser.add_argument('-d', '--dir', metavar="DIR",
                    help='output directory for pos.json, alive.json and optionally chase.log', default=".")
parser.add_argument('-l', '--log', metavar="LEVEL",
                    help='log level [DEBUG, INFO, WARNING, ERROR or CRITICAL]', default="")
parser.add_argument('-r', '--rounds', metavar="NUM",
                    type=int, help='number of rounds', default=50)
parser.add_argument('-s', '--sheep', metavar="NUM", type=int,
                    help='number of sheeps', default=15)
parser.add_argument('-w', '--wait', action='store_true',
                    help='wait for user input after each round')


if __name__ == '__main__':
    args = parser.parse_args()
    ROUNDS = args.rounds
    SHEEPS = args.sheep
    WAIT = args.wait
    CONFIG_FILE = args.config
    LOG_LEVEL = args.log
    OUTPUT_DIR = args.dir

    LOG_LEVEL = "INFO"

    InitPosLimit, SheepMoveDist, WolfMoveDist = load_config(CONFIG_FILE)
    setup_logging(LOG_LEVEL, OUTPUT_DIR + '/chase.log')

    simulation = Simulation(ROUNDS, SHEEPS, InitPosLimit,
                            SheepMoveDist, WolfMoveDist)
    simulation.start_simulation(WAIT, OUTPUT_DIR)
