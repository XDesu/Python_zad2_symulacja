import random
import logging

logger = logging.getLogger(__name__)


class Sheep:

    def __init__(self, indentification_number: int, init_pos_limit: float, sheep_move_dist: float) -> None:
        '''Creates a Sheep with random position between -init_pos_limit and init_pos_limit'''
        logger.debug(
            f"Creating sheep with id {indentification_number}, move distance {sheep_move_dist} and init pos limit {init_pos_limit}")

        self.x = random.uniform(-init_pos_limit, init_pos_limit)
        self.y = random.uniform(-init_pos_limit, init_pos_limit)
        self.move_dist = sheep_move_dist
        self.is_alive = True
        self.id = indentification_number

        logger.info(
            f"Sheep #{self.id} created in position x:{self.x} y:{self.y}")
        return

    def __str__(self) -> str:
        to_return = f"Sheep {self.id} at position x:{self.x} y:{self.y} (alive: {self.is_alive})"
        return to_return

    def __repr__(self) -> str:
        to_return = f"Sheep(id:{self.id}, x:{self.x}, y:{self.y}, move_dist:{self.move_dist}, is_alive:{self.is_alive})"
        return to_return

    def get_position(self) -> tuple[float, float] | None:
        if self.is_alive:
            x = round(self.x, 3)
            y = round(self.y, 3)
            logger.debug(f"returns x:{x} y:{y}")
            return x, y
        logger.debug(f"returns None, because sheep is dead")
        return None

    def move(self) -> None:
        '''Moves sheep in random direction with distance sheep_move_dist'''
        logger.debug(f"Moving sheep #{self.id} from x:{self.x} y:{self.y}")
        directions = ["N", "S", "E", "W"]
        match random.choice(directions):
            case "N":
                self.y += self.move_dist
            case "S":
                self.y -= self.move_dist
            case "E":
                self.x += self.move_dist
            case "W":
                self.x -= self.move_dist
        logger.info(f"Sheep #{self.id} moved to x:{self.x} y:{self.y}")
        return
