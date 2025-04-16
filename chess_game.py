import pygame
import sys
from typing import List, Tuple, Optional, Dict
import random
from copy import deepcopy

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
FPS = 60

# Enhanced Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (238, 238, 210)  # Warm light color
DARK_SQUARE = (118, 150, 86)    # Forest green
HIGHLIGHT = (186, 202, 68)      # Subtle highlight
VALID_MOVE = (214, 214, 189)    # Soft indicator
TEXT_COLOR = (50, 50, 50)
COORDINATES_COLOR = (120, 120, 120)
STATUS_BAR_BG = (45, 45, 45)
STATUS_BAR_TEXT = (220, 220, 220)

# AI Constants
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
        self.type = piece_type
        self.color = color
        self.has_moved = False

class ChessGame:
    def __init__(self):
        # Initialize display with padding for coordinates
        self.padding = 40  # Padding for coordinates
        self.total_width = WINDOW_SIZE + 2 * self.padding
        self.total_height = WINDOW_SIZE + 2 * self.padding + 100  # Extra 100 for status bar
        self.screen = pygame.display.set_mode((self.total_width, self.total_height))
        pygame.display.set_caption("Python Chess vs AI")
        self.clock = pygame.time.Clock()
        
        # Load piece images
        self.piece_images = self._load_piece_images()
        
        # Game state
        self.board = self._initial_board()
        self.selected_piece = None
        self.valid_moves = []
        self.current_player = 'white'  # Human always plays white
        self.move_history = []
        self.is_check = False
        self.is_checkmate = False
        self.is_draw = False
        self.is_ai_thinking = False
        
        # Initialize fonts
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.coord_font = pygame.font.SysFont('Arial', 16)

    def _load_piece_images(self) -> Dict:
        pieces = {}
        piece_chars = {
            'white': {'king': '♔', 'queen': '♕', 'rook': '♖', 
                     'bishop': '♗', 'knight': '♘', 'pawn': '♙'},
            'black': {'king': '♚', 'queen': '♛', 'rook': '♜', 
                     'bishop': '♝', 'knight': '♞', 'pawn': '♟'}
        }
        
        font = pygame.font.SysFont('segoe ui symbol', 64)
        for color in ['white', 'black']:
            pieces[color] = {}
            for piece_type, char in piece_chars[color].items():
                text_color = WHITE if color == 'white' else BLACK
                surface = font.render(char, True, text_color)
                pieces[color][piece_type] = surface
        
        return pieces

    def _initial_board(self):
        board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Place pawns
        for i in range(BOARD_SIZE):
            board[1][i] = Piece('pawn', 'black')
            board[6][i] = Piece('pawn', 'white')
        
        # Place other pieces
        back_row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for i in range(BOARD_SIZE):
            board[0][i] = Piece(back_row[i], 'black')
            board[7][i] = Piece(back_row[i], 'white')
        
        return board

    def calculate_valid_moves(self, pos: Tuple[int, int], board=None) -> List[List[int]]:
        if board is None:
            board = self.board
            
        row, col = pos
        piece = board[row][col]
        if not piece:
            return []

        moves = []
        directions = {
            'rook': [(0, 1), (0, -1), (1, 0), (-1, 0)],
            'bishop': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            'queen': [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            'knight': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],
            'king': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        }

        if piece.type == 'pawn':
            direction = -1 if piece.color == 'white' else 1
            # Forward move
            if 0 <= row + direction < 8 and not board[row + direction][col]:
                moves.append([row + direction, col])
                # Initial two-square move
                if ((piece.color == 'white' and row == 6) or 
                    (piece.color == 'black' and row == 1)):
                    if not board[row + 2 * direction][col]:
                        moves.append([row + 2 * direction, col])
            
            # Captures
            for dcol in [-1, 1]:
                new_row, new_col = row + direction, col + dcol
                if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                    board[new_row][new_col] and 
                    board[new_row][new_col].color != piece.color):
                    moves.append([new_row, new_col])
        
        elif piece.type in directions:
            for dr, dc in directions[piece.type]:
                if piece.type == 'knight':
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < 8 and 0 <= new_col < 8):
                        target = board[new_row][new_col]
                        if not target or target.color != piece.color:
                            moves.append([new_row, new_col])
                else:
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
                            break
                        new_row, new_col = new_row + dr, new_col + dc

        return moves

    def evaluate_board(self, board) -> float:
        score = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece:
                    value = PIECE_VALUES[piece.type]
                    if piece.color == 'white':
                        score += value
                    else:
                        score -= value
        return score

    def get_all_moves(self, board, color: str) -> List[Tuple[List[int], List[int]]]:
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece and piece.color == color:
                    valid_moves = self.calculate_valid_moves([row, col], board)
                    moves.extend([([row, col], move) for move in valid_moves])
        return moves

    def make_ai_move(self):
        def minimax(board, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[Tuple[List[int], List[int]]]]:
            if depth == 0:
                return self.evaluate_board(board), None

            if maximizing:
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
                        break
                return max_eval, best_move
            else:
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
                        break
                return min_eval, best_move

        _, best_move = minimax(self.board, 3, float('-inf'), float('inf'), False)
        if best_move:
            from_pos, to_pos = best_move
            self.make_move(from_pos, to_pos)
        else:
            # Fallback to random move if no good move found
            moves = self.get_all_moves(self.board, 'black')
            if moves:
                from_pos, to_pos = random.choice(moves)
                self.make_move(from_pos, to_pos)

    def draw_coordinates(self):
        # Draw file coordinates (a-h)
        for i in range(BOARD_SIZE):
            # Bottom coordinates
            text = chr(97 + i)
            surface = self.coord_font.render(text, True, COORDINATES_COLOR)
            x = self.padding + i * SQUARE_SIZE + SQUARE_SIZE // 2 - surface.get_width() // 2
            y = self.padding + WINDOW_SIZE + 5
            self.screen.blit(surface, (x, y))
            
            # Top coordinates
            y = self.padding - 20
            self.screen.blit(surface, (x, y))

        # Draw rank coordinates (1-8)
        for i in range(BOARD_SIZE):
            # Left coordinates
            text = str(8 - i)
            surface = self.coord_font.render(text, True, COORDINATES_COLOR)
            x = self.padding - 20
            y = self.padding + i * SQUARE_SIZE + SQUARE_SIZE // 2 - surface.get_height() // 2
            self.screen.blit(surface, (x, y))
            
            # Right coordinates
            x = self.padding + WINDOW_SIZE + 5
            self.screen.blit(surface, (x, y))

    def draw_board(self):
        # Draw chess board background
        pygame.draw.rect(
            self.screen,
            (30, 30, 30),
            (0, 0, self.total_width, self.total_height)
        )

        # Draw board squares with padding
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                
                # Highlight selected piece and valid moves
                if (self.selected_piece and 
                    self.selected_piece[0] == row and 
                    self.selected_piece[1] == col):
                    color = HIGHLIGHT
                elif [row, col] in self.valid_moves:
                    # Draw move indicator circle
                    base_color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                    pygame.draw.rect(
                        self.screen,
                        base_color,
                        (self.padding + col * SQUARE_SIZE, 
                         self.padding + row * SQUARE_SIZE, 
                         SQUARE_SIZE, SQUARE_SIZE)
                    )
                    # Draw circle indicator
                    circle_center = (
                        self.padding + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        self.padding + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    )
                    pygame.draw.circle(self.screen, VALID_MOVE, circle_center, SQUARE_SIZE // 4)
                    continue
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    (self.padding + col * SQUARE_SIZE, 
                     self.padding + row * SQUARE_SIZE, 
                     SQUARE_SIZE, SQUARE_SIZE)
                )
                
                # Draw pieces
                piece = self.board[row][col]
                if piece:
                    piece_surface = self.piece_images[piece.color][piece.type]
                    piece_rect = piece_surface.get_rect(center=(
                        self.padding + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        self.padding + row * SQUARE_SIZE + SQUARE_SIZE // 2
                    ))
                    self.screen.blit(piece_surface, piece_rect)

        # Draw coordinates
        self.draw_coordinates()

        # Draw status bar
        status_rect = pygame.Rect(0, self.total_height - 100, self.total_width, 100)
        pygame.draw.rect(self.screen, STATUS_BAR_BG, status_rect)
        
        # Draw current player with enhanced styling
        player_text = f"Current Player: {'You (White)' if self.current_player == 'white' else 'AI (Black)'}"
        text_surface = self.font.render(player_text, True, STATUS_BAR_TEXT)
        self.screen.blit(text_surface, (20, self.total_height - 80))
        
        # Draw game status with enhanced styling
        status_text = ""
        if self.is_ai_thinking:
            status_text = "AI is thinking..."
        elif self.is_check:
            status_text = "Check!"
        elif self.is_checkmate:
            status_text = "Checkmate!"
        elif self.is_draw:
            status_text = "Draw!"
        
        if status_text:
            status_surface = self.font.render(status_text, True, STATUS_BAR_TEXT)
            self.screen.blit(status_surface, (20, self.total_height - 40))

        # Draw last move if available
        if self.move_history:
            last_move = f"Last move: {self.move_history[-1]}"
            last_move_surface = self.small_font.render(last_move, True, STATUS_BAR_TEXT)
            self.screen.blit(last_move_surface, (self.total_width - 250, self.total_height - 40))

    def make_move(self, from_pos: List[int], to_pos: List[int]):
        piece = self.board[from_pos[0]][from_pos[1]]
        self.board[to_pos[0]][to_pos[1]] = piece
        self.board[from_pos[0]][from_pos[1]] = None
        piece.has_moved = True
        
        # Update move history
        from_notation = f"{chr(97 + from_pos[1])}{8 - from_pos[0]}"
        to_notation = f"{chr(97 + to_pos[1])}{8 - to_pos[0]}"
        self.move_history.append(f"{piece.type} {from_notation}-{to_notation}")
        
        # Switch current player
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def handle_click(self, pos: Tuple[int, int]):
        if self.current_player == 'black' or self.is_ai_thinking:
            return

        # Adjust click position for padding
        adjusted_x = pos[0] - self.padding
        adjusted_y = pos[1] - self.padding
        
        # Check if click is within board boundaries
        if (adjusted_x < 0 or adjusted_x >= WINDOW_SIZE or 
            adjusted_y < 0 or adjusted_y >= WINDOW_SIZE):
            return
        
        col = adjusted_x // SQUARE_SIZE
        row = adjusted_y // SQUARE_SIZE
        
        if self.selected_piece:
            if [row, col] in self.valid_moves:
                self.make_move([self.selected_piece[0], self.selected_piece[1]], [row, col])
                self.selected_piece = None
                self.valid_moves = []
                
                # AI's turn
                self.is_ai_thinking = True
                self.make_ai_move()
                self.is_ai_thinking = False
            else:
                self.selected_piece = None
                self.valid_moves = []
        else:
            piece = self.board[row][col]
            if piece and piece.color == 'white':
                self.selected_piece = [row, col]
                self.valid_moves = self.calculate_valid_moves([row, col])

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)

            self.screen.fill(BLACK)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()