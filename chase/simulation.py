from chase.wolf import Wolf
from chase.sheep import Sheep
import json
import csv
import logging

logger = logging.getLogger(__name__)


class Simulation:

    def __init__(self, rounds_number: int, sheep_number: int, init_pos_limit: float, sheep_move_dist: float, wolf_move_dist: float) -> None:
        '''
        stwórz symulację ze wskazanymi parametrami
        '''

        logger.debug(f"Creating simulation with parameters: rounds_number={rounds_number},"
                     f"sheep_number={sheep_number}, init_pos_limit={init_pos_limit},"
                     f"sheep_move_dist={sheep_move_dist},"
                     f"wolf_move_dist={wolf_move_dist}"
                     )

        self.rounds_number = rounds_number
        self.sheep_number = sheep_number
        self.init_pos_limit = init_pos_limit
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.current_round = 0
        self.was_sheep_eaten = False
        self.targeted_sheep: Sheep = None
        self.positions = []

        self.sheeps: list[Sheep] = []
        for i in range(self.sheep_number):
            self.sheeps.append(
                Sheep(i, self.init_pos_limit, self.sheep_move_dist))
        self.wolf: Wolf = Wolf(self.wolf_move_dist)

        logger.debug("Simulation created with:"
                     f"rounds_number={self.rounds_number},"
                     f"sheep_number={self.sheep_number},"
                     f"init_pos_limit={self.init_pos_limit},"
                     f"sheep_move_dist={self.sheep_move_dist},"
                     f"wolf_move_dist={self.wolf_move_dist},"
                     f"current_round={self.current_round},"
                     f"was_sheep_eaten={self.was_sheep_eaten},"
                     f"targeted_sheep={self.targeted_sheep},"
                     f"positions={self.positions},"
                     f"sheeps={self.sheeps},"
                     f"wolf={self.wolf.__repr__()}"
                     )

        return

    def __str__(self) -> str:
        to_return = f"Round {self.current_round}:\n"
        to_return += f"  Wolf: {self.wolf.get_position()}\n"
        to_return += f"  Sheeps alive: {len(self.get_alive_sheeps())}\n"

        # jeśli wilk goni owcę -\
        # - informację o tym fakcie wraz z określeniem, \
        # która to owca (jej numer porządkowy);
        if self.targeted_sheep:
            to_return += f"  Wolf targeted sheep #{self.targeted_sheep.id}\n"

        # jeżeli któraś z owiec została pożarta -\
        # - informację o tym fakcie wraz z określeniem, \
        # która to była owca (jej numer porządkowy).
        if self.was_sheep_eaten:
            to_return += f"  Wolf ate sheep #{self.targeted_sheep.id}\n"

        return to_return

    def get_alive_sheeps(self) -> list[Sheep]:
        '''
        zwróć tablicę zawierającą owce, które żyją 
        '''
        alive_sheeps = []
        for sheep in self.sheeps:
            if sheep.is_alive:
                alive_sheeps.append(sheep)
        logger.debug(f"returns {alive_sheeps}")
        return alive_sheeps

    def next_round(self) -> None:
        '''
        sprawdź warunki zakończenia symulacji.
        porusz owcami i wilkiem.
        '''
        self.current_round += 1
        alive_sheeps = self.get_alive_sheeps()

        # jeżeli nie ma owiec, zakończ symulację
        if len(alive_sheeps) == 0:
            logger.info(f"No sheeps alive, simulation ends")
            return

        for sheep in alive_sheeps:
            sheep.move()

        self.targeted_sheep = self.wolf.move(alive_sheeps)
        self.was_sheep_eaten = not self.targeted_sheep.is_alive

        logger.debug(f"Wolf targeted sheep #{self.targeted_sheep.id}")

        # jeżeli wilk zjadł owcę, to wskaż ją
        if self.was_sheep_eaten:
            logger.debug(f"Wolf ate sheep #{self.targeted_sheep.id}")

        return

    def start_simulation(self, pause_between_rounds: bool, output_dir: str) -> None:
        '''
        zapis danych do */alive.csv i */pos.json.
        przeprowadź wskazaną ilość rund symulacji
        '''
        logger.info("Starting simulation with parameters:"
                    f"pause_between_rounds={pause_between_rounds},"
                    f"output_dir={output_dir}"
                    )

        alive_file = output_dir + '/alive.csv'
        positions_file = output_dir + '/pos.json'

        logger.info(f"Saving alive sheeps to {alive_file}")
        logger.info(f"Saving positions to {positions_file}")

        print(self)

        for _ in range(self.rounds_number):
            logger.info(
                f"Starting round {self.current_round + 1} of {self.rounds_number}")
            self.next_round()
            logger.debug(f"Finished round {self.current_round}")

            print(self)
            self.targeted_sheep = None
            self.was_sheep_eaten = False

            if pause_between_rounds:
                logger.debug(f"Pausing between rounds")
                input("Press Enter to continue...")

            self.save_number_of_alive_sheeps_to_file(alive_file)
            self.save_positions_to_file(positions_file)

        self.was_sheep_eaten = False
        self.targeted_sheep = None
        logger.info(f"Simulation ended")
        return

    def save_number_of_alive_sheeps_to_file(self, filename: str) -> None:
        '''
        zapisz do pliku żywe owce
        '''
        # wyczyść plik w pierwszej rundzie
        if (self.current_round == 1):
            logger.debug(f"Cleaning file {filename}")
            with open(filename, 'w') as f:
                f.truncate()
        # zaktualizuj plik
        logger.debug(f"Saving alive sheeps to {filename}")
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([self.current_round, len(self.get_alive_sheeps())])

        return

    def save_positions_to_file(self, filename: str) -> None:
        '''
        zapisz wszystkie pozycje do pliku
        '''
        # wyczyśc plik w pierwszej rundzie
        if (self.current_round == 1):
            logger.debug(f"Cleaning file {filename}")
            with open(filename, 'w') as f:
                f.truncate()

        # pozyskaj statystyki
        round_stats = {}
        round_stats['round_no'] = self.current_round
        round_stats['wolf_pos'] = self.wolf.get_position()
        round_stats['sheep_pos'] = []
        for sheep in self.sheeps:
            round_stats['sheep_pos'].append(sheep.get_position())
        self.positions.append(round_stats)

        # zapisz statystyki
        logger.debug(f"Saving positions to {filename}")
        with open(filename, 'w') as f:
            json.dump(self.positions, f, ensure_ascii=False, indent=4)
        return
