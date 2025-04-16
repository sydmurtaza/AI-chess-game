import sys
from typing import List, Tuple, Optional
import random
from copy import deepcopy

# Constants
BOARD_SIZE = 8  # Size of the chessboard (8x8)

# ANSI color codes for terminal display
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BLACK = "\033[30m"
    BG_LIGHT = "\033[47m"  # Light background for squares
    BG_DARK = "\033[100m"  # Dark background for squares

# AI Constants
# Dictionary to assign values to pieces for board evaluation in the AI's decision-making
PIECE_VALUES = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 100
}

class Piece:
    def __init__(self, piece_type: str, color: str):
        """Initialize a chess piece with its type and color."""
        self.type = piece_type  # Type of the piece (e.g., 'pawn', 'king')
        self.color = color      # Color of the piece ('white' or 'black')
        self.has_moved = False  # Track if the piece has moved (useful for castling or pawn double moves)

class ChessGame:
    def __init__(self):
        """Initialize the chess game state."""
        self.board = self._initial_board()  # Set up the initial chessboard
        self.current_player = 'white'       # Start with White's turn
        self.move_history = []              # List to store the history of moves
        self.is_check = False               # Flag to indicate if the current player is in check
        self.is_checkmate = False           # Flag to indicate if the game has ended in checkmate
        self.is_stalemate = False           # Flag to indicate if the game has ended in stalemate

    def _initial_board(self):
        """Set up the initial chessboard with pieces in their starting positions."""
        # Create an 8x8 board with None (empty squares)
        board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        # Define the back row piece order (rook, knight, bishop, queen, king, bishop, knight, rook)
        back_row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        # Place Black pieces (pawns on row 1, back row pieces on row 0)
        for i in range(BOARD_SIZE):
            board[1][i] = Piece('pawn', 'black')
            board[0][i] = Piece(back_row[i], 'black')
        # Place White pieces (pawns on row 6, back row pieces on row 7)
        for i in range(BOARD_SIZE):
            board[6][i] = Piece('pawn', 'white')
            board[7][i] = Piece(back_row[i], 'white')
        return board

    def display_board(self):
        """Display the current state of the chessboard and game status in the console with enhanced formatting."""
        # Clear the console for a clean display (works on Unix-based systems and Windows)
        print("\033[H\033[J", end="")

        # Print a decorative header
        print(f"{Colors.BOLD}{Colors.CYAN}♟️  Console Chess  ♟️{Colors.RESET}")
        print(f"{Colors.BLUE}{'=' * 30}{Colors.RESET}\n")

        # Dictionary to map piece types to their display symbols
        piece_symbols = {
            'pawn': 'PA',
            'knight': 'KN',
            'bishop': 'BI',
            'rook': 'RO',
            'queen': 'QU',
            'king': 'KI'
        }

        # Print column labels (a-h) with a top border, adjusted for larger squares (5 chars wide)
        print(f"    {'┌' + '─────┬' * (BOARD_SIZE - 1) + '─────┐'}")
        print(f"    ", end="")
        for col in range(BOARD_SIZE):
            print(f"  {chr(97 + col)}   ", end="")
        print()

        # Print each row of the board with increased height (3 lines per row)
        for row in range(BOARD_SIZE):
            # First line of the square (top padding)
            print(f"{Colors.YELLOW}{8 - row:2d}{Colors.RESET} │", end="")
            for col in range(BOARD_SIZE):
                bg_color = Colors.BG_LIGHT if (row + col) % 2 == 0 else Colors.BG_DARK
                print(f"{bg_color}     {Colors.RESET}│", end="")
            print(f" {Colors.YELLOW}{8 - row:2d}{Colors.RESET}")

            # Second line of the square (piece or empty)
            print(f"   │", end="")
            for col in range(BOARD_SIZE):
                bg_color = Colors.BG_LIGHT if (row + col) % 2 == 0 else Colors.BG_DARK
                piece = self.board[row][col]
                if piece:
                    piece_color = Colors.WHITE if piece.color == 'white' else Colors.BLACK
                    symbol = piece_symbols[piece.type].upper() if piece.color == 'white' else piece_symbols[piece.type].lower()
                    print(f"{bg_color}{piece_color}{Colors.BOLD} {symbol:^3} {Colors.RESET}", end="")
                else:
                    print(f"{bg_color} {' ':^3} {Colors.RESET}", end="")
                print("│", end="")
            print()

            # Third line of the square (bottom padding)
            print(f"   │", end="")
            for col in range(BOARD_SIZE):
                bg_color = Colors.BG_LIGHT if (row + col) % 2 == 0 else Colors.BG_DARK
                print(f"{bg_color}     {Colors.RESET}│", end="")
            print()

            # Print separator between rows (except for the last row)
            if row < BOARD_SIZE - 1:
                print(f"    {'├' + '─────┼' * (BOARD_SIZE - 1) + '─────┤'}")

        # Print bottom border and column labels again
        print(f"    {'└' + '─────┴' * (BOARD_SIZE - 1) + '─────┘'}")
        print(f"    ", end="")
        for col in range(BOARD_SIZE):
            print(f"  {chr(97 + col)}   ", end="")
        print("\n")

        # Display game status with color
        if self.is_checkmate:
            winner = "Black (AI)" if self.current_player == 'white' else "White (You)"
            print(f"{Colors.RED}{Colors.BOLD}Checkmate! {winner} wins!{Colors.RESET}")
        elif self.is_stalemate:
            print(f"{Colors.YELLOW}{Colors.BOLD}Stalemate! Game is a draw!{Colors.RESET}")
        elif self.is_check:
            print(f"{Colors.RED}Check!{Colors.RESET}")

        # Display move history with a cleaner format
        if self.move_history:
            print(f"\n{Colors.BLUE}{Colors.BOLD}Move History:{Colors.RESET}")
            print(f"{Colors.BLUE}{'─' * 40}{Colors.RESET}")
            for i in range(0, len(self.move_history), 2):
                move_num = (i // 2) + 1
                white_move = self.move_history[i]
                black_move = self.move_history[i + 1] if i + 1 < len(self.move_history) else " "
                print(f"{Colors.CYAN}{move_num:2d}.{Colors.RESET} {Colors.WHITE}White: {white_move:<20}{Colors.RESET} {Colors.BLACK}Black: {black_move}{Colors.RESET}")
        print()

    def get_basic_moves(self, pos: Tuple[int, int], board) -> List[List[int]]:
        """Calculate all possible moves for a piece at the given position (ignoring checks)."""
        row, col = pos
        piece = board[row][col]
        if not piece:
            return []  # Return empty list if there's no piece at the position

        moves = []  # List to store possible moves
        # Define movement directions for pieces that move in straight or diagonal lines
        directions = {
            'rook': [(0, 1), (0, -1), (1, 0), (-1, 0)],  # Horizontal and vertical
            'bishop': [(1, 1), (1, -1), (-1, 1), (-1, -1)],  # Diagonal
            'queen': [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],  # Both
            'knight': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],  # L-shape
            'king': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # One square in any direction
        }

        # Handle pawn moves (forward moves and captures)
        if piece.type == 'pawn':
            direction = -1 if piece.color == 'white' else 1  # White moves up, Black moves down
            # Single step forward if the square is empty
            if 0 <= row + direction < 8 and not board[row + direction][col]:
                moves.append([row + direction, col])
                # Double step from starting position if both squares are empty
                if ((piece.color == 'white' and row == 6) or 
                    (piece.color == 'black' and row == 1)):
                    if not board[row + 2 * direction][col]:
                        moves.append([row + 2 * direction, col])
            # Diagonal captures
            for dcol in [-1, 1]:
                new_row, new_col = row + direction, col + dcol
                if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                    board[new_row][new_col] and 
                    board[new_row][new_col].color != piece.color):
                    moves.append([new_row, new_col])
        
        # Handle other pieces (rook, bishop, queen, knight, king)
        elif piece.type in directions:
            for dr, dc in directions[piece.type]:
                if piece.type == 'knight':
                    # Knights move in an L-shape and can jump over pieces
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < 8 and 0 <= new_col < 8):
                        target = board[new_row][new_col]
                        if not target or target.color != piece.color:
                            moves.append([new_row, new_col])
                else:
                    # Rooks, bishops, queens, and kings move along their respective directions
                    new_row, new_col = row + dr, col + dc
                    while 0 <= new_row < 8 and 0 <= new_col < 8:
                        target = board[new_row][new_col]
                        if not target:
                            moves.append([new_row, new_col])
                        elif target.color != piece.color:
                            moves.append([new_row, new_col])
                            break
                        else:
                            break
                        if piece.type == 'king':
                            break  # Kings only move one square
                        new_row, new_col = new_row + dr, new_col + dc

        return moves

    def is_square_attacked(self, board, square: List[int], attacking_color: str) -> bool:
        """Check if the given square is attacked by any piece of the attacking color."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece and piece.color == attacking_color:
                    moves = self.get_basic_moves([row, col], board)
                    if square in moves:
                        return True
        return False

    def is_king_in_check(self, board, color: str) -> bool:
        """Check if the king of the given color is in check."""
        king_pos = None
        # Find the king's position
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece and piece.type == 'king' and piece.color == color:
                    king_pos = [row, col]
                    break
            if king_pos:
                break
        opponent_color = 'black' if color == 'white' else 'white'
        return self.is_square_attacked(board, king_pos, opponent_color)

    def calculate_valid_moves(self, pos: Tuple[int, int], board=None) -> List[List[int]]:
        """Calculate all legal moves for a piece at the given position (considering checks)."""
        if board is None:
            board = self.board
        row, col = pos
        piece = board[row][col]
        if not piece:
            return []

        # Get all possible moves
        moves = self.get_basic_moves(pos, board)
        legal_moves = []
        # Filter moves to ensure they don't leave the king in check
        for move in moves:
            test_board = deepcopy(board)
            test_board[move[0]][move[1]] = test_board[row][col]
            test_board[row][col] = None
            if not self.is_king_in_check(test_board, piece.color):
                legal_moves.append(move)
        return legal_moves

    def is_checkmate_or_stalemate(self, board, color: str) -> Tuple[bool, bool]:
        """Check if the current position is checkmate or stalemate for the given color."""
        has_legal_moves = False
        # Check if the player has any legal moves
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece and piece.color == color:
                    moves = self.calculate_valid_moves([row, col], board)
                    if moves:
                        has_legal_moves = True
                        break
            if has_legal_moves:
                break
        is_check = self.is_king_in_check(board, color)
        # Checkmate: in check and no legal moves; Stalemate: not in check and no legal moves
        return (is_check and not has_legal_moves, not is_check and not has_legal_moves)

    def evaluate_board(self, board) -> float:
        """Evaluate the board for the AI by summing piece values (positive for White, negative for Black)."""
        score = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece:
                    value = PIECE_VALUES[piece.type]
                    score += value if piece.color == 'white' else -value
        return score

    def get_all_moves(self, board, color: str) -> List[Tuple[List[int], List[int]]]:
        """Get all possible legal moves for the given color."""
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece and piece.color == color:
                    valid_moves = self.calculate_valid_moves([row, col], board)
                    moves.extend([([row, col], move) for move in valid_moves])
        return moves

    def make_ai_move(self):
        """Make a move for the AI using the Min-Max algorithm with Alpha-Beta Pruning."""
        def minimax(board, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[Tuple[List[int], List[int]]]]:
            """Min-Max algorithm with Alpha-Beta Pruning to find the best move."""
            if depth == 0:
                return self.evaluate_board(board), None  # Base case: evaluate the board

            if maximizing:
                # Maximizing player (White)
                max_eval = float('-inf')
                best_move = None
                for from_pos, to_pos in self.get_all_moves(board, 'white'):
                    new_board = deepcopy(board)
                    new_board[to_pos[0]][to_pos[1]] = new_board[from_pos[0]][from_pos[1]]
                    new_board[from_pos[0]][from_pos[1]] = None
                    eval, _ = minimax(new_board, depth - 1, alpha, beta, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (from_pos, to_pos)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Alpha-Beta pruning
                return max_eval, best_move
            else:
                # Minimizing player (Black)
                min_eval = float('inf')
                best_move = None
                for from_pos, to_pos in self.get_all_moves(board, 'black'):
                    new_board = deepcopy(board)
                    new_board[to_pos[0]][to_pos[1]] = new_board[from_pos[0]][from_pos[1]]
                    new_board[from_pos[0]][from_pos[1]] = None
                    eval, _ = minimax(new_board, depth - 1, alpha, beta, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (from_pos, to_pos)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha-Beta pruning
                return min_eval, best_move

        print(f"{Colors.BLUE}AI is thinking...{Colors.RESET}")
        # Use Min-Max with a depth of 3 to find the best move for Black
        _, best_move = minimax(self.board, 3, float('-inf'), float('inf'), False)
        if best_move:
            from_pos, to_pos = best_move
            self.make_move(from_pos, to_pos)
        else:
            # Fallback: if no best move is found, choose a random move
            moves = self.get_all_moves(self.board, 'black')
            if moves:
                from_pos, to_pos = random.choice(moves)
                self.make_move(from_pos, to_pos)

    def make_move(self, from_pos: List[int], to_pos: List[int]):
        """Execute a move on the board and update the game state."""
        piece = self.board[from_pos[0]][from_pos[1]]
        self.board[to_pos[0]][to_pos[1]] = piece  # Move the piece to the new position
        self.board[from_pos[0]][from_pos[1]] = None  # Clear the original position
        piece.has_moved = True
        
        # Record the move in the history
        from_notation = f"{chr(97 + from_pos[1])}{8 - from_pos[0]}"
        to_notation = f"{chr(97 + to_pos[1])}{8 - to_pos[0]}"
        self.move_history.append(f"{piece.type} {from_notation}-{to_notation}")
        
        # Switch the current player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        # Update game state (check, checkmate, stalemate)
        self.is_check = self.is_king_in_check(self.board, self.current_player)
        self.is_checkmate, self.is_stalemate = self.is_checkmate_or_stalemate(self.board, self.current_player)

    def parse_move(self, move: str) -> Optional[Tuple[List[int], List[int]]]:
        """Parse a move in algebraic notation (e.g., 'e2e4') and return the from and to positions."""
        if len(move) != 4:
            return None  # Move must be exactly 4 characters
        
        try:
            # Convert algebraic notation to board coordinates
            from_file = ord(move[0].lower()) - ord('a')  # e.g., 'e' -> 4
            from_rank = 8 - int(move[1])                 # e.g., '2' -> 6
            to_file = ord(move[2].lower()) - ord('a')
            to_rank = 8 - int(move[3])
            
            # Validate coordinates
            if not (0 <= from_file < 8 and 0 <= from_rank < 8 and 0 <= to_file < 8 and 0 <= to_rank < 8):
                return None
                
            from_pos = [from_rank, from_file]
            to_pos = [to_rank, to_file]
            
            return from_pos, to_pos
        except (ValueError, IndexError):
            return None

    def run(self):
        """Main game loop to run the chess game in the console."""
        print(f"{Colors.BOLD}{Colors.CYAN}Welcome to Console Chess!{Colors.RESET}")
        print(f"{Colors.YELLOW}You are White (uppercase pieces). Enter moves in algebraic notation (e.g., 'e2e4').{Colors.RESET}")
        print(f"{Colors.YELLOW}Type 'quit' to exit.{Colors.RESET}\n")
        
        while True:
            self.display_board()  # Show the current board state
            
            # End the game if checkmate or stalemate is detected
            if self.is_checkmate or self.is_stalemate:
                print(f"{Colors.GREEN}Game Over! Press Enter to exit.{Colors.RESET}")
                input()
                break
                
            if self.current_player == 'white':
                # Human player's turn (White)
                print(f"{Colors.GREEN}{Colors.BOLD}Your turn (White). Enter your move (e.g., 'e2e4'):{Colors.RESET} ", end="")
                move_input = input().strip()
                
                if move_input.lower() == 'quit':
                    print(f"{Colors.YELLOW}Game ended.{Colors.RESET}")
                    break
                    
                move = self.parse_move(move_input)
                if not move:
                    print(f"{Colors.RED}Invalid move format. Use algebraic notation like 'e2e4'.{Colors.RESET}")
                    continue
                    
                from_pos, to_pos = move
                piece = self.board[from_pos[0]][from_pos[1]]
                
                # Validate the piece selection
                if not piece or piece.color != 'white':
                    print(f"{Colors.RED}Invalid move: No white piece at that position.{Colors.RESET}")
                    continue
                    
                # Validate the move
                valid_moves = self.calculate_valid_moves(from_pos)
                if to_pos not in valid_moves:
                    print(f"{Colors.RED}Invalid move: That move is not legal.{Colors.RESET}")
                    continue
                    
                self.make_move(from_pos, to_pos)
            else:
                # AI's turn (Black)
                self.make_ai_move()

if __name__ == "__main__":
    """Entry point to start the chess game."""
    game = ChessGame()
    game.run()