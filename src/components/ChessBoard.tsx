import React from 'react';
import { useChessContext } from '../context/ChessContext';
import { Square } from './Square';

export const ChessBoard: React.FC = () => {
  const { board, selectedPiece, validMoves, handleSquareClick } = useChessContext();

  return (
    <div className="aspect-square bg-gray-800 p-4 rounded-lg shadow-xl">
      <div className="grid grid-cols-8 gap-1 h-full">
        {board.map((row, i) =>
          row.map((piece, j) => {
            const isLight = (i + j) % 2 === 0;
            const isSelected = selectedPiece?.position[0] === i && selectedPiece?.position[1] === j;
            const isValidMove = validMoves.some(move => move[0] === i && move[1] === j);

            return (
              <Square
                key={`${i}-${j}`}
                piece={piece}
                isLight={isLight}
                isSelected={isSelected}
                isValidMove={isValidMove}
                onClick={() => handleSquareClick([i, j])}
              />
            );
          })
        )}
      </div>
    </div>
  );
};