

from math import sqrt
from entity.sheep import Sheep


class Wolf:

    def __init__(self, wolf_move_dist: float) -> None:
        '''Creates wolf with position at (0,0)'''
        # dodać rzucanie wyjątków jeżeli parametr < 0 lub ==None/null

        self.x = 0.0
        self.y = 0.0
        self.move_dist = wolf_move_dist
        pass

    def get_position(self) -> tuple[float, float]:
        '''returns a current position of the wolf'''
        return self.x, self.y

    def calc_distance_from_sheep(self, sheep: Sheep) -> float:
        '''returns the distance between the wolf and a given sheep'''
        wx, wy = self.x, self.y
        sx, sy = sheep.get_position()

        distance = sqrt((sx - wx)**2 + (sy - wy)**2)
        return distance
