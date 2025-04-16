import React from 'react';
import { Piece } from '../types/chess';
import { getPieceIcon } from '../utils/pieceIcons';

interface SquareProps {
  piece: Piece | null;
  isLight: boolean;
  isSelected: boolean;
  isValidMove: boolean;
  onClick: () => void;
}

export const Square: React.FC<SquareProps> = ({
  piece,
  isLight,
  isSelected,
  isValidMove,
  onClick,
}) => {
  const baseClasses = `
    relative aspect-square flex items-center justify-center
    transition-colors duration-200
    ${isLight ? 'bg-amber-100' : 'bg-amber-800'}
    ${isSelected ? 'ring-2 ring-blue-500 ring-inset' : ''}
    ${isValidMove ? 'after:absolute after:w-3 after:h-3 after:rounded-full after:bg-blue-500/50' : ''}
    hover:brightness-110
  `;

  return (
    <div className={baseClasses} onClick={onClick}>
      {piece && (
        <div className={`text-3xl ${piece.color === 'white' ? 'text-white' : 'text-black'}`}>
          {getPieceIcon(piece)}
        </div>
      )}
    </div>
  );
};