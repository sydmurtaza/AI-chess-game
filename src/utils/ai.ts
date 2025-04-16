import { Piece, Position, PieceColor } from '../types/chess';
import { calculateValidMoves } from './moves';

// Piece values for evaluation
const PIECE_VALUES = {
  pawn: 1,
  knight: 3,
  bishop: 3,
  rook: 5,
  queen: 9,
  king: 100
};

// Position evaluation tables for each piece type
const POSITION_VALUES = {
  pawn: [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
    [0.5, 1, 1, -2, -2, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0]
  ],
  knight: [
    [-5, -4, -3, -3, -3, -3, -4, -5],
    [-4, -2, 0, 0, 0, 0, -2, -4],
    [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
    [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
    [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
    [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
    [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]
  ],
  bishop: [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
    [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
    [-1, 0, 1, 1, 1, 1, 0, -1],
    [-1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
  ],
  rook: [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0.5, 1, 1, 1, 1, 1, 1, 0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [0, 0, 0, 0.5, 0.5, 0, 0, 0]
  ],
  queen: [
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-1, 0, 0.5, 0, 0, 0, 0, -1],
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
  ],
  king: [
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 3, 1, 0, 0, 1, 3, 2]
  ]
};

// Evaluate the current board position
const evaluatePosition = (board: (Piece | null)[][]): number => {
  let score = 0;

  for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
      const piece = board[i][j];
      if (piece) {
        const baseValue = PIECE_VALUES[piece.type];
        const positionValue = POSITION_VALUES[piece.type][piece.color === 'white' ? i : 7 - i][j];
        const value = baseValue + positionValue;
        score += piece.color === 'white' ? value : -value;
      }
    }
  }

  return score;
};

// Get all valid moves for a piece
const getAllValidMoves = (board: (Piece | null)[][], color: PieceColor): [Position, Position][] => {
  const moves: [Position, Position][] = [];

  for (let i = 0; i < 8; i++) {
    for (let j = 0; j < 8; j++) {
      const piece = board[i][j];
      if (piece && piece.color === color) {
        const validMoves = calculateValidMoves(board, [i, j]);
        validMoves.forEach(move => {
          moves.push([[i, j], move]);
        });
      }
    }
  }

  return moves;
};

// Make a move on the board
const makeMove = (board: (Piece | null)[][], from: Position, to: Position): (Piece | null)[][] => {
  const newBoard = board.map(row => [...row]);
  const piece = newBoard[from[0]][from[1]];
  newBoard[to[0]][to[1]] = piece;
  newBoard[from[0]][from[1]] = null;
  return newBoard;
};

// MinMax algorithm with Alpha-Beta pruning
const minMax = (
  board: (Piece | null)[][],
  depth: number,
  alpha: number,
  beta: number,
  maximizingPlayer: boolean
): [number, [Position, Position] | null] => {
  if (depth === 0) {
    return [evaluatePosition(board), null];
  }

  const moves = getAllValidMoves(board, maximizingPlayer ? 'black' : 'white');
  let bestMove: [Position, Position] | null = null;

  if (maximizingPlayer) {
    let maxEval = -Infinity;
    for (const [from, to] of moves) {
      const newBoard = makeMove(board, from, to);
      const [evaluation] = minMax(newBoard, depth - 1, alpha, beta, false);
      if (evaluation > maxEval) {
        maxEval = evaluation;
        bestMove = [from, to];
      }
      alpha = Math.max(alpha, evaluation);
      if (beta <= alpha) break;
    }
    return [maxEval, bestMove];
  } else {
    let minEval = Infinity;
    for (const [from, to] of moves) {
      const newBoard = makeMove(board, from, to);
      const [evaluation] = minMax(newBoard, depth - 1, alpha, beta, true);
      if (evaluation < minEval) {
        minEval = evaluation;
        bestMove = [from, to];
      }
      beta = Math.min(beta, evaluation);
      if (beta <= alpha) break;
    }
    return [minEval, bestMove];
  }
};

// Get the best move for the AI
export const getBestMove = (board: (Piece | null)[][]): [Position, Position] => {
  const [_, bestMove] = minMax(board, 3, -Infinity, Infinity, true);
  return bestMove || [[0, 0], [0, 0]]; // Fallback move if no valid moves found
};