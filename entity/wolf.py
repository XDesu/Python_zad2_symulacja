import logging

from math import dist
from sys import maxsize
from entity.sheep import Sheep

logger = logging.getLogger(__name__)


def get_unit_vector_from_p1_to_p2(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """
    zwróć wektor jednostkowy z p1 do p2
    """
    logger.debug(f"get_unit_vector_from_p1_to_p2(p1:{p1}, p2:{p2})")

    len = dist(p1, p2)
    if len == 0:
        return 0, 0
    p3 = (p2[0] - p1[0], p2[1] - p1[1])
    p3 = (p3[0] / len, p3[1] / len)

    logger.debug(f"returns p3:{p3}")
    return p3


class Wolf:

    def __init__(self, wolf_move_dist: float) -> None:
        '''stwórz wilka na pozycji (0,0)'''
        logger.debug(f"Creating wolf with move distance {wolf_move_dist}")

        self.x = 0.0
        self.y = 0.0
        self.move_dist = wolf_move_dist

        logger.info(f"Wolf created in position x:{self.x} y:{self.y}")
        return

    def __str__(self) -> str:
        to_return = f"Wolf at position x:{self.x} y:{self.y}"
        return to_return

    def __repr__(self) -> str:
        to_return = f"Wolf(x:{self.x}, y:{self.y}, move_dist:{self.move_dist})"
        return to_return

    def get_position(self) -> tuple[float, float]:
        '''zwróć aktualną pozycję wilka'''
        x = round(self.x, 3)
        y = round(self.y, 3)
        logger.debug(f"returns x:{x} y:{y}")
        return x, y

    def calc_distance_from_sheep(self, sheep: Sheep) -> float:
        '''zwróć odległość pomiędzy wilkiem a wskazaną owcą'''
        logger.debug(f"Calculating distance from sheep {{{sheep}}}")

        # jeżeli martwa owca znajduje się w zasięgu wilka
        # to zwróć "nieskończoną" odległość
        if sheep.get_position() == None:
            logger.error(f"Dead sheep {sheep} in wolf distance calculation")
            return maxsize

        distance = dist(self.get_position(), sheep.get_position())

        # wx, wy = self.x, self.y
        # sx, sy = sheep.get_position()
        # distance = sqrt((sx - wx)**2 + (sy - wy)**2)

        logger.debug(
            f"Distance from wolf to sheep {sheep.__repr__()} is {distance}")
        return distance

    def kill_sheep(self, sheep: Sheep) -> Sheep:
        '''zabij owcę'''
        logger.debug(f"Killing sheep {sheep.__repr__()}")
        sheep.is_alive = False
        return sheep

    def move(self, sheeps: list[Sheep]) -> Sheep:
        '''
        porusz wilka w kierunku najbliższej owcy.
        zjedz owcę, gdy znajduje się w zasięgu wilka.
        zwróć namierzoną owcę
        '''
        logger.debug(f"Moving wolf towards closest sheep. Sheeps: {sheeps}")

        closest_sheep = sheeps[0]
        closest_distance = self.calc_distance_from_sheep(closest_sheep)

        for sheep in sheeps:
            distance = self.calc_distance_from_sheep(sheep)
            if distance < closest_distance:
                closest_sheep = sheep
                closest_distance = distance

        logger.info(
            f"Closest sheep is {closest_sheep.__repr__()} with distance {closest_distance}")

        s_pos = closest_sheep.get_position()
        move_to = (0, 0)
        # jeżeli, owca znajduje się w zasięgu wilka to ją zjedz.
        if closest_distance <= self.move_dist:
            move_to = s_pos
            self.kill_sheep(closest_sheep)
        else:
            move_to = get_unit_vector_from_p1_to_p2((self.x, self.y), s_pos)
            move_to = (move_to[0] * self.move_dist,
                       move_to[1] * self.move_dist)
            move_to = (self.x + move_to[0], self.y + move_to[1])

        # przemieść wilka
        self.x = move_to[0]
        self.y = move_to[1]

        logger.info(f"Wolf moved to x:{self.x} y:{self.y}")
        return closest_sheep
