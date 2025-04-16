AI Chess Game

Console Chess Game
A command-line chess game built in Python where you can play against an AI opponent. The game features a visually appealing CLI with colored pieces, a larger board display, and a Min-Max algorithm with Alpha-Beta pruning for the AI's moves.
Features

Play Against AI: Challenge an AI opponent that uses the Min-Max algorithm with Alpha-Beta pruning to make strategic moves.
Enhanced CLI Display:
Larger board with increased width and height for better visibility.
Colored pieces (White in white, Black in black) with a checkerboard pattern.
Descriptive piece symbols (e.g., PA for Pawn, KI for King) to avoid confusion.


Move History: Tracks and displays all moves made by both players in a clean format.
Game Status Detection:
Detects check, checkmate, and stalemate conditions.
Announces the winner or declares a draw at the end of the game.


User-Friendly Interface:
Clear prompts and error messages with color coding.
Supports algebraic notation for moves (e.g., e2e4).



Installation

Clone the Repository:
git clone  https://github.com/sydmurtaza/AI-chess-game.git
cd AI-chess-game


Ensure Python is Installed:

This game requires Python 3.6 or higher. Check your Python version with:
python3 --version


If Python is not installed, download and install it from python.org.


No Additional Dependencies:

The game uses only the Python standard library, so no additional packages are required.



Usage

Run the Game:

Navigate to the project directory and run the script:
python3 console_chess_game.py




Play the Game:

You play as White (uppercase pieces), and the AI plays as Black (lowercase pieces).
Enter your moves in algebraic notation (e.g., e2e4 to move a pawn from e2 to e4).
Type quit to exit the game at any time.



Gameplay Instructions

Board Display:

The board is an 8x8 grid with rows labeled 1-8 and columns labeled a-h.
Piece symbols:
White Pieces (uppercase): PA (Pawn), KN (Knight), BI (Bishop), RO (Rook), QU (Queen), KI (King)
Black Pieces (lowercase): pa (Pawn), kn (Knight), bi (Bishop), ro (Rook), qu (Queen), ki (King)


Squares are colored in a checkerboard pattern for better visibility.


Making Moves:

When it's your turn, you'll see a prompt: Your turn (White). Enter your move (e.g., 'e2e4'):.
Enter your move in the format from_square to to_square (e.g., e2e4).
The game will validate your move and display an error if it's invalid.


AI Moves:

The AI (Black) will automatically make a move after your turn using the Min-Max algorithm with Alpha-Beta pruning.
You'll see AI is thinking... while the AI calculates its move.


Game End:

The game ends when a checkmate or stalemate is detected.
Checkmate: The game announces the winner (e.g., Checkmate! Black (AI) wins!).
Stalemate: The game declares a draw (e.g., Stalemate! Game is a draw!).


Requirements

Python 3.6 or higher.
A terminal that supports ANSI color codes (e.g., Windows Terminal, macOS Terminal, Linux terminals) for the best visual experience.
If your terminal doesn't support ANSI codes, the game will still work, but colors and formatting may not display correctly.



AI Implementation
The AI uses the Min-Max algorithm with Alpha-Beta pruning to determine its moves:

Min-Max: Evaluates the game tree to a depth of 3, maximizing the AI's score while minimizing the player's score.
Alpha-Beta Pruning: Optimizes the search by pruning branches that won't affect the final decision, making the AI faster.
Board Evaluation: Assigns values to pieces (e.g., Pawn = 1, Queen = 9) and calculates a score based on the pieces remaining on the board.

Contributing
Feel free to fork this repository, make improvements, and submit a pull request. Some ideas for enhancements:

Add support for castling and en passant.
Improve the AI by increasing the search depth or adding a more sophisticated evaluation function.
Add a graphical interface using a library like Pygame.

