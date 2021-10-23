import random


class Sheep:

    def __init__(self, init_pos_limit: float, sheep_move_dist: float) -> None:
        '''Creates a Sheep with random position between -init_pos_limit and init_pos_limit'''
        # dodać rzucanie wyjątków jeżeli parametry < 0 lub ==None/null

        self.x = random.uniform(-init_pos_limit, init_pos_limit)
        self.y = random.uniform(-init_pos_limit, init_pos_limit)
        self.move_dist = sheep_move_dist
        pass

    def get_position(self):
        return self.x, self.y
