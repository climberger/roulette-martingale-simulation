import random


def get_roulette_result():
    return random.randint(0, 36)


def is_red(result):
    return result % 2 == 1


def is_a_win(bet_colour, result):

    if result == 0:
        return False

    is_red_bool = is_red(result)

    if bet_colour == "red":
        return is_red_bool
    else:
        return not is_red_bool


def play_game(budget, max_bet, base_bet):
    bet_colour = "red"
    continue_game = True
    bet_amount = base_bet
    lost_amount = 0
    cash_back = 0

    while continue_game:
        result = get_roulette_result()

        is_win = is_a_win(bet_colour, result)

        won = 0
        over_max_bet = 0
        over_budget = 0

        if is_win:
            cash_back = bet_amount
            continue_game = False
            won = 1
        else:
            lost_amount = lost_amount + bet_amount
            bet_amount = bet_amount * 2
            if bet_amount > max_bet:
                continue_game = False
                over_max_bet = 1
            if bet_amount > budget:
                continue_game = False
                over_budget = 1
            else:
                budget = budget - bet_amount

    won_amount = cash_back - lost_amount
    result = (won_amount, won, over_max_bet, over_budget)
    return result


budget = 100000
max_bet = 10000
base_bet = 10

number_of_max_games = 1000000000
win_sum = 0

sub_count = 0
no_of_sub_batches = 0
report_for_steps = 500000

won_games = 0
aborted_games = 0
games_over_max_bet = 0
games_over_budget = 0

fmt = "{index}\t\t{played_games}\t\t\t{won_games}\t\t{aborted_games}\t{rel_won}\t{rel_ab}"
print("Index\tPlayed games\tWon games\tAborted\t%Won\t%Ab.")

for x in range(0, number_of_max_games):

    sub_count = sub_count + 1
    game_result = play_game(budget, max_bet, base_bet)
    win_sum = win_sum + game_result[0]

    if game_result[1] == 1:
        won_games = won_games + 1
    else:
        aborted_games = aborted_games + 1

    games_over_max_bet = games_over_max_bet + game_result[2]
    games_over_budget = games_over_budget + game_result[3]

    if sub_count == report_for_steps:
        total_number_of_games = x + 1
        no_of_sub_batches = no_of_sub_batches + 1
        sub_count = 0
        report_data = {
            'index': str(no_of_sub_batches),
            'played_games': total_number_of_games,
            'won_games': won_games,
            'aborted_games': aborted_games,
            'games_over_max_bet': games_over_max_bet,
            'games_over_budget': games_over_budget,
            'rel_won': "{:10.7f}".format(won_games / total_number_of_games),
            'rel_ab': "{:10.7f}".format(aborted_games / total_number_of_games)
        }
        report = fmt.format(**report_data)
        print(report)


average_won_amount = win_sum / number_of_max_games

print("Average won sum is:" + str(average_won_amount))
