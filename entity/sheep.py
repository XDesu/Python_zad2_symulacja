import random


class Sheep:

    def __init__(self, indentation_number: int, init_pos_limit: float, sheep_move_dist: float) -> None:
        '''Creates a Sheep with random position between -init_pos_limit and init_pos_limit'''
        # dodać rzucanie wyjątków jeżeli parametry < 0 lub ==None/null

        self.x = random.uniform(-init_pos_limit, init_pos_limit)
        self.y = random.uniform(-init_pos_limit, init_pos_limit)
        self.move_dist = sheep_move_dist
        self.is_alive = True
        self.id = indentation_number
        pass

    def get_position(self):
        if self.is_alive:
            return round(self.x, 3), round(self.y, 3)
        return None

    def move(self) -> None:
        '''Moves sheep in random direction with distance sheep_move_dist'''
        directions = ["N", "S", "E", "W"]
        match random.choice(directions):
            case "N":
                self.y += self.move_dist
                return
            case "S":
                self.y -= self.move_dist
                return
            case "E":
                self.x += self.move_dist
                return
            case "W":
                self.x -= self.move_dist
                return
        return
