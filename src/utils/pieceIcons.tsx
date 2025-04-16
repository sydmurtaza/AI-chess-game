import React from 'react';
import { Piece } from '../types/chess';

export const getPieceIcon = (piece: Piece): string => {
  const icons = {
    white: {
      king: '♔',
      queen: '♕',
      rook: '♖',
      bishop: '♗',
      knight: '♘',
      pawn: '♙'
    },
    black: {
      king: '♚',
      queen: '♛',
      rook: '♜',
      bishop: '♝',
      knight: '♞',
      pawn: '♟'
    }
  };

  return icons[piece.color][piece.type];
};