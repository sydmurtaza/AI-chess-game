import React, { createContext, useContext, useState, useCallback } from 'react';
import { initialBoard } from '../utils/board';
import { calculateValidMoves, isKingInCheck, findKing } from '../utils/moves';
import { getBestMove } from '../utils/ai';
import { Position, Piece, ChessContextType } from '../types/chess';

const ChessContext = createContext<ChessContextType | null>(null);

export const useChessContext = () => {
  const context = useContext(ChessContext);
  if (!context) {
    throw new Error('useChessContext must be used within a ChessProvider');
  }
  return context;
};

export const ChessProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [board, setBoard] = useState(initialBoard());
  const [selectedPiece, setSelectedPiece] = useState<{ piece: Piece; position: Position } | null>(null);
  const [currentPlayer, setCurrentPlayer] = useState<'white' | 'black'>('white');
  const [validMoves, setValidMoves] = useState<Position[]>([]);
  const [moveHistory, setMoveHistory] = useState<string[]>([]);
  const [isCheck, setIsCheck] = useState(false);
  const [isCheckmate, setIsCheckmate] = useState(false);
  const [isDraw, setIsDraw] = useState(false);
  const [isAIThinking, setIsAIThinking] = useState(false);

  const makeMove = useCallback((from: Position, to: Position, isAIMove: boolean = false) => {
    setBoard(currentBoard => {
      const newBoard = currentBoard.map(row => [...row]);
      const piece = newBoard[from[0]][from[1]];
      newBoard[to[0]][to[1]] = piece;
      newBoard[from[0]][from[1]] = null;
      
      // Add move to history
      const fromNotation = `${String.fromCharCode(97 + from[1])}${8 - from[0]}`;
      const toNotation = `${String.fromCharCode(97 + to[1])}${8 - to[0]}`;
      setMoveHistory(prev => [...prev, `${piece?.type} ${fromNotation}-${toNotation}`]);
      
      // Update current player
      const nextPlayer = isAIMove ? 'white' : 'black';
      setCurrentPlayer(nextPlayer);
      
      // Check for check/checkmate
      const kingPos = findKing(newBoard, nextPlayer);
      const inCheck = isKingInCheck(newBoard, kingPos, nextPlayer);
      setIsCheck(inCheck);
      
      return newBoard;
    });
  }, []);

  const handleSquareClick = useCallback((position: Position) => {
    // Prevent moves while AI is thinking
    if (isAIThinking || currentPlayer !== 'white') {
      return;
    }

    const piece = board[position[0]][position[1]];

    if (selectedPiece) {
      if (validMoves.some(move => move[0] === position[0] && move[1] === position[1])) {
        makeMove(selectedPiece.position, position);
        setSelectedPiece(null);
        setValidMoves([]);
        
        // AI move with updated board state
        setIsAIThinking(true);
        setTimeout(() => {
          if (!isCheckmate && !isDraw) {
            // Get the current board state after the player's move
            const [from, to] = getBestMove(board);
            makeMove(from, to, true);
          }
          setIsAIThinking(false);
        }, 500);
      } else {
        setSelectedPiece(null);
        setValidMoves([]);
      }
    } else if (piece && piece.color === 'white') {
      setSelectedPiece({ piece, position });
      setValidMoves(calculateValidMoves(board, position));
    }
  }, [board, selectedPiece, validMoves, currentPlayer, isCheckmate, isDraw, makeMove, isAIThinking]);

  const resetGame = useCallback(() => {
    setBoard(initialBoard());
    setSelectedPiece(null);
    setCurrentPlayer('white');
    setValidMoves([]);
    setMoveHistory([]);
    setIsCheck(false);
    setIsCheckmate(false);
    setIsDraw(false);
    setIsAIThinking(false);
  }, []);

  return (
    <ChessContext.Provider
      value={{
        board,
        selectedPiece,
        currentPlayer,
        validMoves,
        moveHistory,
        isCheck,
        isCheckmate,
        isDraw,
        handleSquareClick,
        resetGame,
      }}
    >
      {children}
    </ChessContext.Provider>
  );
};