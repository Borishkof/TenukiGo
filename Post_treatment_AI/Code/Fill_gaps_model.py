#Imports
import numpy as np
from keras.models import load_model

#Load the model
model=load_model('modelCNN.keras')
#Define the possible moves
import numpy as np


def fill_gaps(model, sequence_with_gap, gap_start, gap_end, black_possible_moves, white_possible_moves):
    """
    Fill the gaps in the sequence with the best moves chosen from the list of possible moves.

    Args:
        model: The trained model to predict the best move.
        sequence_with_gap (list of np.array): The sequence of board states with gaps (missing moves).
        gap_start (int): The start index of the gap.
        gap_end (int): The end index of the gap.
        black_possible_moves (list of tuple): Possible moves for black.
        white_possible_moves (list of tuple): Possible moves for white.

    Returns:
        filled_sequence (list of np.array): The sequence with the gaps filled.
    """
    filled_sequence = sequence_with_gap.copy()  # Avoid modifying the original sequence

    # Determine the current player based on the difference between the last two states before the gap
    state_before_gap_1 = sequence_with_gap[gap_start - 1]
    state_before_gap_2 = sequence_with_gap[gap_start - 2]

    # Subtract the two states to find the last move
    difference = state_before_gap_1 - state_before_gap_2
    current_player = 2 if np.any(difference == 1) else 2  # 1 for black, 2 for white

    # Copy possible moves to avoid mutating the original lists
    black_moves = black_possible_moves.copy()
    white_moves = white_possible_moves.copy()

    # Iterate over each gap in the sequence
    for gap_index in range(gap_start, gap_end):
        # Extract the current state of the board at this gap
        current_board_state = filled_sequence[gap_index - 1]

        # Choose the appropriate move list based on the current player
        possible_moves = black_moves if current_player == 1 else white_moves

        # Recalculate valid moves for the current board state
        valid_moves = [
            move for move in possible_moves
            if current_board_state[move[0], move[1]] == 0
        ]

        # Initialize a list to store the candidate boards
        candidate_boards = []
        candidate_moves = []

        # For each valid move, simulate placing a stone and prepare the candidate board
        for move in valid_moves:
            x, y = move
            candidate_board = current_board_state.copy()
            candidate_board[x, y] = current_player  # Place current player's stone
            candidate_boards.append(candidate_board)
            candidate_moves.append(move)  # Keep track of the valid move

        # If no valid candidate boards, continue (no valid move)
        if not candidate_boards:
            print(f"No valid moves for gap index {gap_index}, skipping.")
            continue

        # Convert candidate_boards to a numpy array
        candidate_boards = np.array(candidate_boards)

        # Ensure the correct shape for the model (add the channel dimension)
        candidate_boards = np.expand_dims(candidate_boards, axis=-1)  # Shape: (batch_size, 19, 19, 1)
        candidate_boards = candidate_boards.astype(np.float32)

        # Predict the probabilities for each candidate board
        probabilities = model.predict(candidate_boards)

        # Get the index of the best move based on the highest probability
        best_move_idx = np.argmax(probabilities[:, current_player - 1])  # Current player determines the index
        best_move = candidate_moves[best_move_idx]

        # Update the board state with the best move
        x, y = best_move
        filled_sequence[gap_index] = current_board_state.copy()
        filled_sequence[gap_index][x, y] = current_player  # Place current player's stone

        # Remove the chosen move from the appropriate possible_moves list
        if current_player == 1:
            black_moves.remove(best_move)
        else:
            white_moves.remove(best_move)

        # Update the next board state in the sequence
        if gap_index + 1 < len(filled_sequence):
            filled_sequence[gap_index + 1] = filled_sequence[gap_index].copy()

        # Switch player for the next move (alternate between 1 and 2)
        current_player = 3 - current_player  # If 1 (black), becomes 2 (white), and vice versa

        print(f"Filling gap index {gap_index} with move {best_move} by player {current_player}")

    return filled_sequence