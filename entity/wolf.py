import logging

from math import sqrt
from entity.sheep import Sheep

logger = logging.getLogger(__name__)


class Wolf:

    def __init__(self, wolf_move_dist: float) -> None:
        '''Creates wolf with position at (0,0)'''
        logger.debug(f"Creating wolf with move distance {wolf_move_dist}")

        self.x = 0.0
        self.y = 0.0
        self.move_dist = wolf_move_dist

        logger.info(f"Wolf created in position x:{self.x} y:{self.y}")
        pass

    def __str__(self) -> str:
        to_return = f"Wolf at position x:{self.x} y:{self.y}"
        return to_return

    def get_position(self) -> tuple[float, float]:
        '''returns a current position of the wolf'''
        x = round(self.x, 3)
        y = round(self.y, 3)
        logger.debug(f"returns x:{x} y:{y}")
        return x, y

    def calc_distance_from_sheep(self, sheep: Sheep) -> float:
        '''returns the distance between the wolf and a given sheep'''
        logger.debug(f"Calculating distance from sheep {{{sheep}}}")

        wx, wy = self.x, self.y
        sx, sy = sheep.get_position()

        distance = sqrt((sx - wx)**2 + (sy - wy)**2)

        logger.debug(f"Distance from wolf to sheep {{{sheep}}} is {distance}")
        return distance

    def move(self, sheeps: list[Sheep]) -> Sheep:
        '''
        moves towards the closest sheep.
        return targeted sheep
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
            f"Closest sheep is {{{closest_sheep}}} with distance {closest_distance}")

        sx, sy = closest_sheep.get_position()
        if closest_distance <= self.move_dist:
            self.x = sx
            self.y = sy
            closest_sheep.is_alive = False
            logger.info(
                f"Wolf moved to sheep {{{closest_sheep}}} and killed it")
            return closest_sheep

        # calculate unit vector
        s_length = sqrt(sx**2 + sy**2)
        sx_unit, sy_unit = sx/s_length, sy/s_length
        # set unit vector towards sheep from wolf
        sx_unit *= -1 if abs(sx) - abs(self.x) < 0 else 1
        sy_unit *= -1 if abs(sy) - abs(self.y) < 0 else 1
        # move wolf in that direction
        self.x += self.move_dist * sx_unit
        self.y += self.move_dist * sy_unit

        logger.info(f"Wolf moved to x:{self.x} y:{self.y}")
        return closest_sheep
