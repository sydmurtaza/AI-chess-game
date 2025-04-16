import pygame
import sys
from typing import List, Tuple, Optional, Dict

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (130, 151, 105)
VALID_MOVE = (119, 149, 86)

class Piece:
    def __init__(self, piece_type: str, color: str):
        self.type = piece_type
        self.color = color

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Python Chess")
        self.clock = pygame.time.Clock()
        
        # Load piece images
        self.piece_images = self._load_piece_images()
        
        # Game state
        self.board = self._initial_board()
        self.selected_piece = None
        self.valid_moves = []
        self.current_player = 'white'
        self.move_history = []
        self.is_check = False
        self.is_checkmate = False
        self.is_draw = False
        self.is_ai_thinking = False

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

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                
                # Highlight selected piece and valid moves
                if (self.selected_piece and 
                    self.selected_piece[0] == row and 
                    self.selected_piece[1] == col):
                    color = HIGHLIGHT
                elif [row, col] in self.valid_moves:
                    color = VALID_MOVE
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )
                
                # Draw pieces
                piece = self.board[row][col]
                if piece:
                    piece_surface = self.piece_images[piece.color][piece.type]
                    piece_rect = piece_surface.get_rect(center=(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2
                    ))
                    self.screen.blit(piece_surface, piece_rect)

    def calculate_valid_moves(self, pos: Tuple[int, int]) -> List[List[int]]:
        row, col = pos
        piece = self.board[row][col]
        if not piece:
            return []

        moves = []
        
        # Basic pawn moves (simplified for example)
        if piece.type == 'pawn':
            if piece.color == 'white':
                if row > 0 and not self.board[row - 1][col]:
                    moves.append([row - 1, col])
                    if row == 6 and not self.board[row - 2][col]:
                        moves.append([row - 2, col])
            else:
                if row < 7 and not self.board[row + 1][col]:
                    moves.append([row + 1, col])
                    if row == 1 and not self.board[row + 2][col]:
                        moves.append([row + 2, col])
        
        # Add other piece moves here...
        return moves

    def make_move(self, from_pos: List[int], to_pos: List[int], is_ai_move: bool = False):
        piece = self.board[from_pos[0]][from_pos[1]]
        self.board[to_pos[0]][to_pos[1]] = piece
        self.board[from_pos[0]][from_pos[1]] = None
        
        # Update move history
        from_notation = f"{chr(97 + from_pos[1])}{8 - from_pos[0]}"
        to_notation = f"{chr(97 + to_pos[1])}{8 - to_pos[0]}"
        self.move_history.append(f"{piece.type} {from_notation}-{to_notation}")
        
        # Update current player
        self.current_player = 'white' if is_ai_move else 'black'

    def get_best_move(self) -> Tuple[List[int], List[int]]:
        # Implement the MinMax algorithm with Alpha-Beta pruning here
        # For now, return a simple move
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece.color == 'black':
                    moves = self.calculate_valid_moves([row, col])
                    if moves:
                        return [row, col], moves[0]
        return [0, 0], [0, 0]

    def handle_click(self, pos: Tuple[int, int]):
        if self.is_ai_thinking or self.current_player != 'white':
            return

        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        
        if self.selected_piece:
            if [row, col] in self.valid_moves:
                self.make_move([self.selected_piece[0], self.selected_piece[1]], [row, col])
                self.selected_piece = None
                self.valid_moves = []
                
                # AI move
                self.is_ai_thinking = True
                if not self.is_checkmate and not self.is_draw:
                    from_pos, to_pos = self.get_best_move()
                    self.make_move(from_pos, to_pos, True)
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

            self.draw_board()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()