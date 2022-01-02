from typing import List
from entity.wolf import Wolf
from entity.sheep import Sheep
import json
import csv


class Simulation:

    def __init__(self, rounds_number: int, sheep_number: int, init_pos_limit: float, sheep_move_dist: float, wolf_move_dist: float):
        self.rounds_number = rounds_number
        self.sheep_number = sheep_number
        self.init_pos_limit = init_pos_limit
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.current_round = 0
        self.was_sheep_eaten = False
        self.targeted_sheep: Sheep = None
        self.positions = []

        self.sheeps: List[Sheep] = []
        for i in range(self.sheep_number):
            self.sheeps.append(
                Sheep(i, self.init_pos_limit, self.sheep_move_dist))
        self.wolf: Wolf = Wolf(self.wolf_move_dist)

    def __str__(self):
        to_return = f"Round {self.current_round}:\n"
        to_return += f"  Wolf: {self.wolf.get_position()}\n"
        to_return += f"  Sheeps alive: {len(self.get_alive_sheeps())}\n"
        # jeśli wilk goni którąś owcę - informację o tym fakcie wraz z określeniem, która to owca (jej numer porządkowy);
        if self.targeted_sheep:
            to_return += f"  Wolf targeted sheep #{self.targeted_sheep.id}\n"
        # jeżeli któraś z owiec została pożarta - informację o tym fakcie wraz z określeniem, która to była owca (jej numer porządkowy).
        if self.was_sheep_eaten:
            to_return += f"  Wolf ate sheep #{self.targeted_sheep.id}\n"
        return to_return

    def get_alive_sheeps(self):
        alive_sheeps = []
        for sheep in self.sheeps:
            if sheep.is_alive:
                alive_sheeps.append(sheep)
        return alive_sheeps

    def next_round(self):
        self.current_round += 1
        alive_sheeps = self.get_alive_sheeps()
        if len(alive_sheeps) == 0:
            return

        for sheep in alive_sheeps:
            sheep.move()
        self.targeted_sheep = self.wolf.move(
            alive_sheeps)
        self.was_sheep_eaten = not self.targeted_sheep.is_alive

    def start_simulation(self, pause_between_rounds: bool):
        while self.current_round < self.rounds_number:
            print(self)
            self.was_sheep_eaten = False
            self.targeted_sheep = None
            if pause_between_rounds:
                input()

            self.next_round()
            self.save_number_of_alive_sheeps_to_file('alive.csv')
            self.save_positions_to_file('pos.json')
        print(self)
        self.save_number_of_alive_sheeps_to_file('alive.csv')
        self.save_positions_to_file('pos.json')
        self.was_sheep_eaten = False
        self.targeted_sheep = None

    def save_number_of_alive_sheeps_to_file(self, filename: str):
        # clean file if first round
        if (self.current_round == 1):
            with open(filename, 'w') as f:
                f.truncate()
        # update file
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([self.current_round, len(self.get_alive_sheeps())])

    def save_positions_to_file(self, filename: str):
        # clean file if first round
        if (self.current_round == 1):
            with open(filename, 'w') as f:
                f.truncate()

        # get stats
        round_stats = {}
        round_stats['round_no'] = self.current_round
        round_stats['wolf_pos'] = self.wolf.get_position()
        round_stats['sheep_pos'] = []
        for sheep in self.sheeps:
            round_stats['sheep_pos'].append(sheep.get_position())
        self.positions.append(round_stats)

        # save stats
        with open(filename, 'w') as f:
            json.dump(self.positions, f, ensure_ascii=False, indent=4)
