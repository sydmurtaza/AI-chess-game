import { Piece, Position } from '../types/chess';

export const calculateValidMoves = (board: (Piece | null)[][], position: Position): Position[] => {
  const piece = board[position[0]][position[1]];
  if (!piece) return [];

  const moves: Position[] = [];
  
  // Basic move calculation (to be expanded)
  switch (piece.type) {
    case 'pawn':
      if (piece.color === 'white') {
        if (position[0] > 0 && !board[position[0] - 1][position[1]]) {
          moves.push([position[0] - 1, position[1]]);
          if (position[0] === 6 && !board[position[0] - 2][position[1]]) {
            moves.push([position[0] - 2, position[1]]);
          }
        }
      } else {
        if (position[0] < 7 && !board[position[0] + 1][position[1]]) {
          moves.push([position[0] + 1, position[1]]);
          if (position[0] === 1 && !board[position[0] + 2][position[1]]) {
            moves.push([position[0] + 2, position[1]]);
          }
        }
      }
      break;
    // Add other piece moves
  }

  return moves;
};

export const isKingInCheck = (board: (Piece | null)[][], kingPosition: Position, kingColor: 'white' | 'black'): boolean => {
  // Implementation to check if the king is in check
  return false;
};

export const findKing = (board: (Piece | null)[][], color: 'white' | 'black'): Position => {
  for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
      const piece = board[i][j];
      if (piece?.type === 'king' && piece.color === color) {
        return [i, j];
      }
    }
  }
  throw new Error(`${color} king not found`);
};