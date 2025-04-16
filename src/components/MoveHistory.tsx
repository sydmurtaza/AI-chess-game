import React from 'react';
import { useChessContext } from '../context/ChessContext';

export const MoveHistory: React.FC = () => {
  const { moveHistory } = useChessContext();

  return (
    <div className="bg-gray-800 p-6 rounded-lg">
      <h2 className="text-xl font-semibold mb-4">Move History</h2>
      
      <div className="h-[400px] overflow-y-auto space-y-2">
        {moveHistory.map((move, index) => (
          <div
            key={index}
            className="flex items-center text-sm"
          >
            <span className="w-8 text-gray-500">{Math.floor(index / 2) + 1}.</span>
            <span className="flex-1">{move}</span>
          </div>
        ))}
      </div>
    </div>
  );
};