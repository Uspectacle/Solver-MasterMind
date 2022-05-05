from classes import *


def play():
    truth = ListOfColor(random=True)
    print('Use this format: 0167\n◉ = same place, ◎ = wrong place\n')
    for move in range(NUM_TRY):
        while True:
            prop = input(f'your {move} move: ')
            if len(prop) == SIZE and prop.isdigit():
                break
        prop = ListOfColor([Color(int(color)) for color in prop])
        same_color = truth.compare(prop)
        print('\t\t ', same_color, '\n')
        if same_color.same_place == SIZE:
            print('Not that bad')
            return
    print('You stink hard')


def distance(inp, order=0):
    if not order:
        return max(inp)
    out = [i**order for i in inp if i]
    return (sum(out)/len(out))**(1/order)


def search_move(list_of_prop=ALOC, possible_truth=ALOC, depth=NUM_TRY, order=-1):
    score, worst, future_possible_truth = [], [], []
    for ind, prop in enumerate(list_of_prop):
        current_regress = Faster_regress[str(prop)]
        len_next = []
        dict_new_possible_truth = {}
        for SC in ASC:
            possible_list = current_regress[str(SC)]
            new_possible_truth = [possible for possible in possible_list if possible in possible_truth]
            if depth and len(new_possible_truth) > 1:
                next_score, _ = search_move(possible_truth=new_possible_truth, depth=depth - 1, order=order)
                next_score_valid = [score for score in next_score if score != 0]
                len_next.append(min(next_score_valid)+len(new_possible_truth))
            else:
                len_next.append(len(new_possible_truth))
            dict_new_possible_truth[str(SC)] = new_possible_truth
        score.append(distance(len_next, order))
        future_possible_truth.append(dict_new_possible_truth)
    return score, future_possible_truth


def get_best_move(list_of_prop, possible_truth, depth, order):
    score, future_possible_truth = search_move(list_of_prop=list_of_prop,
                                               possible_truth=possible_truth,
                                               depth=depth,
                                               order=order)
    idx_sorted = [idx for _, idx in sorted(zip(score, range(len(list_of_prop))))]
    best_idx = idx_sorted[0]
    best_move = list_of_prop[best_idx]
    possible_truth = future_possible_truth[best_idx]
    return best_move, possible_truth


def main(depth, distance_order, file):
    print(f'-- MasterMind walkthrough with a depth of {depth} and distance-{distance_order}--\n\n')
    walkthrough = {turn: [] for turn in range(NUM_TRY-1)}
    walkthrough[0] = [(None, None, ALOC)]
    length_game = []
    for turn, walk in walkthrough.items():
        for last_move, last_SC, possible_truth in walk:
            if len(possible_truth) > 1:
                best_move, next_possible_truth = get_best_move(ALOC, possible_truth, depth, distance_order)
                file.write(f"\n[[{turn + 1}]]\t<{last_move},\t{f'{last_SC}':5s}\t[{len(possible_truth)}]>\t{best_move}\t(")
                print(f"\n[[{turn + 1}]]\t<{last_move},\t{f'{last_SC}':5s}\t[{len(possible_truth)}]>\t{best_move}\t(", end='')
                for SC in ASC:
                    if len(next_possible_truth[str(SC)]) and turn+1 in walkthrough:
                        walkthrough[turn+1].append((best_move, SC, next_possible_truth[str(SC)]))
                        file.write(f"{f'{SC}':5s}\t[{len(next_possible_truth[str(SC)])}],\t")
                        print(f"{f'{SC}':5s}\t[{len(next_possible_truth[str(SC)])}],\t", end='')
                file.write(')')
                print(')', end='')
            elif len(possible_truth) == 1:
                if str(last_SC) == '◉◉◉◉':
                    length_game.append(turn)
                else:
                    file.write(f"\n[[{turn + 1}]]\t<{last_move},\t{f'{last_SC}':5s}\t[{len(possible_truth)}]>\t>>>{possible_truth[0]}")
                    print(f"\n\n[[{turn + 1}]]\t<{last_move},\t{f'{last_SC}':5s}\t[{len(possible_truth)}]>\t>>>{possible_truth[0]}", end='')
                    length_game.append(turn+1)
    length_dict = {(k+1): 0 for k in range(NUM_TRY)}
    mean_turn = 0
    for turn in length_game:
        length_dict[turn] += 1
        mean_turn += turn
    mean_turn = mean_turn / len(length_game)
    file.write(f'\n\nturn mean : {mean_turn}\ndetail hist:\n{length_dict}')
    print(f'\n\nturn mean : {mean_turn}\ndetail hist:\n{length_dict}')


if __name__ == '__main__':
    print('\n-- SOLVER --')
    for d in [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3, 1.4, 1.6, 1.7, 1.8, 1.9, 6, 7, 8, 9, 10]:
        try:
            f = open(f'walk_depth0color8_d{d}.txt', 'w', encoding="utf-8")
            main(0, d, f)
            f.close()
        except:
            pass
