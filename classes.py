from random import choice

print('-- INITIALIZATION --')
NUM_COLOR = 8
SIZE = 4
NUM_TRY = 10


class Color(str):
    def __new__(cls, color: int = None, random: bool = False):
        assert (color is not None) != random
        if random:
            color = choice(range(NUM_COLOR))
        assert color in range(NUM_COLOR)
        new = str.__new__(cls, color)
        return new


def all_colors() -> list:
    return [Color(color) for color in range(NUM_COLOR)]


AC = all_colors()


class SameColor:
    def __init__(self, wrong_place: int = 0, same_place: int = 0):
        assert wrong_place + same_place <= SIZE
        assert not (wrong_place == 1 and same_place == SIZE - 1)
        self.wrong_place = wrong_place
        self.same_place = same_place

    def __eq__(self, other):
        return (self.wrong_place == other.wrong_place) and (self.same_place == other.same_place)

    def __str__(self):
        return '◉' * self.same_place + '◎' * self.wrong_place if self.wrong_place or self.same_place else '_'


def all_same_color() -> list:
    print('Building all_same_color ... ', end='')
    out = []
    for same_place in range(SIZE + 1):
        for wrong_place in range(SIZE + 1):
            try:
                out.append(SameColor(wrong_place, same_place))
            except:
                pass
    print('\rBuilding all_same_color Done')
    return out


ASC = all_same_color()


class ListOfColor(list):
    def __init__(self, list_of_colors: list = None, random: bool = False):
        assert (list_of_colors is not None) != random
        if random:
            list_of_colors = [Color(random=True) for _ in range(SIZE)]
        super().__init__(list_of_colors)

    def get_positions(self) -> dict:
        positions = {color: [] for color in AC}
        for ind, color in enumerate(self):
            positions[color].append(ind)
        return positions

    def compare(self, other) -> SameColor:
        total_same_color = SameColor()
        positions_1 = self.get_positions()
        positions_2 = other.get_positions()
        for color in AC:
            same_color = min(len(positions_2[color]), len(positions_1[color]))
            same_place = 0
            for ind, position in enumerate(positions_1[color]):
                if position in positions_2[color]:
                    same_place += 1
            total_same_color.same_place += same_place
            total_same_color.wrong_place += same_color - same_place
        return total_same_color

    def regress(self, list_of_other: list, same_color: SameColor) -> list:
        possible_other = []
        for other in list_of_other:
            if same_color == self.compare(other):
                possible_other.append(other)
        return possible_other

    def copy_and_append(self, color: Color):
        return ListOfColor([color for color in self + [color]])

    def __str__(self):
        return ''.join(self)


def all_list_of_color(size: int = SIZE) -> list:
    if size == SIZE:
        print('Building all_list_of_color ... ', end='')
    if size == 1:
        return [ListOfColor([color]) for color in AC]
    all_list = []
    all_smaller = all_list_of_color(size - 1)
    for color in AC:
        for smaller in all_smaller:
            all_list.append(smaller.copy_and_append(color))
    if size == SIZE:
        print('\rBuilding all_list_of_color Done')
    return all_list


ALOC = all_list_of_color()

# First_move = [ListOfColor([Color(0), Color(0), Color(0), Color(0)]),
#               ListOfColor([Color(0), Color(0), Color(0), Color(1)]),
#               ListOfColor([Color(0), Color(0), Color(1), Color(1)]),
#               ListOfColor([Color(0), Color(0), Color(1), Color(2)]),
#               ListOfColor([Color(0), Color(1), Color(2), Color(3)])]


def all_regress() -> dict:
    print('Building Faster_regress ... ', end="")
    out = {}
    for ind, list_of_color in enumerate(ALOC):
        out[str(list_of_color)] = {str(same_color): list_of_color.regress(ALOC, same_color) for same_color in ASC}
        if not (ind+1) % 10:
            print(f'\rBuilding Faster_regress ... {ind+1} / {len(ALOC)}', end="")
    print('\rBuilding Faster_regress Done')
    return out


Faster_regress = all_regress()


def get_best_idx(my_list):
    idx = []
    my_list_unique = []
    for i, item in enumerate(my_list):
        if item not in my_list_unique:
            my_list_unique.append(item)
            idx.append(i)
    return [idx for _, idx in sorted(zip(my_list_unique, idx))]
