import configparser
import argparse
import os

from entity.simulation import Simulation
import logging


def load_config(config_file_path: str = ""):
    config = configparser.ConfigParser()
    config.optionxform = str

    if config.read(config_file_path) == []:
        if config_file_path != "":
            logger.warning(
                f"Config file {config_file_path} not found, using default config")
        return 10.0, 0.5, 1.0
        config['Terrain'] = {}
        config['Terrain']['InitPosLimit'] = '10'
        config['Movement'] = {}
        config['Movement']['SheepMoveDist'] = '0.5'
        config['Movement']['WolfMoveDist'] = '1'

    InitPosLimit = float(config['Terrain']['InitPosLimit'])
    SheepMoveDist = float(config['Movement']['SheepMoveDist'])
    WolfMoveDist = float(config['Movement']['WolfMoveDist'])

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
        case '':
            return
        case _:
            raise Exception('Invalid log level')

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
    # parse arguments
    args = parser.parse_args()
    ROUNDS = args.rounds
    SHEEPS = args.sheep
    WAIT = args.wait
    CONFIG_FILE = args.config
    LOG_LEVEL = args.log
    OUTPUT_DIR = args.dir

    # create output dir if not exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # setup logging
    setup_logging(LOG_LEVEL, OUTPUT_DIR + '/chase.log')
    logger = logging.getLogger(__name__)

    InitPosLimit, SheepMoveDist, WolfMoveDist = load_config(CONFIG_FILE)

    # validate arguments
    if ROUNDS < 0:
        logger.critical('Number of rounds must be greater than 0')
        raise Exception('Number of rounds must be greater than 0')
    if SHEEPS < 0:
        logger.critical('Number of sheeps must be greater than 0')
        raise Exception('Number of rounds must be greater than 0')
    if WAIT not in [True, False]:
        logger.critical('Wait must be true or false')
        raise Exception('Wait must be true or false')
    if CONFIG_FILE != "" and CONFIG_FILE[-4:] != ".ini":
        logger.critical('Config file must end with .ini')
        raise Exception('Config file must end with .ini')
    if CONFIG_FILE != "" and not os.path.isfile(CONFIG_FILE):
        logger.critical('Config file does not exist')
        raise Exception('Config file does not exist')
    # check if init pos limit is number
    try:
        InitPosLimit = float(InitPosLimit)
    except:
        logger.critical('InitPosLimit must be a number')
        raise Exception('InitPosLimit must be a number')
    # check if sheep move dist is number
    try:
        SheepMoveDist = float(SheepMoveDist)
    except:
        logger.critical('SheepMoveDist must be a number')
        raise Exception('SheepMoveDist must be a number')
    # check if wolf move dist is number
    try:
        WolfMoveDist = float(WolfMoveDist)
    except:
        logger.critical('WolfMoveDist must be a number')
        raise Exception('WolfMoveDist must be a number')

    # create and run simulation
    simulation = Simulation(ROUNDS, SHEEPS, InitPosLimit,
                            SheepMoveDist, WolfMoveDist)
    simulation.start_simulation(WAIT, OUTPUT_DIR)
