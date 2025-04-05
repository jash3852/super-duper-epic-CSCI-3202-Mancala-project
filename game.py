from mancala import Mancala
    
num_games = 100
wins = 0
losses = 0
ties = 0
p1_turns_by_game = []
p2_turns_by_game = []

for _ in range(num_games):
    game = Mancala()

    while not game.winning_eval():
        game.play(game.random_move_generator())

    p1_turns_by_game.append(game.p1_turn_counter)
    p2_turns_by_game.append(game.p2_turn_counter)

    if game.board[game.p1_mancala_index] > game.board[game.p2_mancala_index]:
        wins += 1
    elif game.board[game.p2_mancala_index] > game.board[game.p1_mancala_index]:
        losses += 1
    else:
        ties += 1

print(f"Games Won: {(wins / num_games):.1%}")
print(f"Games Lost: {(losses / num_games):.1%}")
print(f"Games Tied: {(ties / num_games):.1%}")
print("Average Player 1 Turns per Game:", sum(p1_turns_by_game) / len(p1_turns_by_game))
print("Average Player 2 Turns per Game:", sum(p2_turns_by_game) / len(p2_turns_by_game))