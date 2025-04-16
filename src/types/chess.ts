export type PieceType = 'pawn' | 'rook' | 'knight' | 'bishop' | 'queen' | 'king';
export type PieceColor = 'white' | 'black';
export type Position = [number, number];

export interface Piece {
  type: PieceType;
  color: PieceColor;
}

export interface ChessContextType {
  board: (Piece | null)[][];
  selectedPiece: { piece: Piece; position: Position } | null;
  currentPlayer: PieceColor;
  validMoves: Position[];
  moveHistory: string[];
  isCheck: boolean;
  isCheckmate: boolean;
  isDraw: boolean;
  handleSquareClick: (position: Position) => void;
  resetGame: () => void;
}