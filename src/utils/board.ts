import { Piece } from '../types/chess';

export const initialBoard = (): (Piece | null)[][] => {
  const board: (Piece | null)[][] = Array(8).fill(null).map(() => Array(8).fill(null));

  // Place pawns
  for (let i = 0; i < 8; i++) {
    board[1][i] = { type: 'pawn', color: 'black' };
    board[6][i] = { type: 'pawn', color: 'white' };
  }

  // Place other pieces
  const backRow: ('rook' | 'knight' | 'bishop' | 'queen' | 'king')[] = [
    'rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'
  ];

  for (let i = 0; i < 8; i++) {
    board[0][i] = { type: backRow[i], color: 'black' };
    board[7][i] = { type: backRow[i], color: 'white' };
  }

  return board;
};