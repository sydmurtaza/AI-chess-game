import React from 'react';
import { useChessContext } from '../context/ChessContext';
import { RefreshCw } from 'lucide-react';

export const GameStatus: React.FC = () => {
  const { currentPlayer, isCheck, isCheckmate, isDraw, resetGame } = useChessContext();

  return (
    <div className="bg-gray-800 p-6 rounded-lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Game Status</h2>
        <button
          onClick={resetGame}
          className="p-2 rounded-full hover:bg-gray-700 transition-colors"
          title="Reset Game"
        >
          <RefreshCw className="w-5 h-5" />
        </button>
      </div>
      
      <div className="space-y-2">
        <p className="text-lg">
          Current Turn: <span className="font-bold">{currentPlayer === 'white' ? 'White' : 'Black'}</span>
        </p>
        
        {isCheck && !isCheckmate && (
          <p className="text-yellow-500 font-bold">Check!</p>
        )}
        
        {isCheckmate && (
          <p className="text-red-500 font-bold">
            Checkmate! {currentPlayer === 'white' ? 'Black' : 'White'} wins!
          </p>
        )}
        
        {isDraw && (
          <p className="text-blue-500 font-bold">Draw!</p>
        )}
      </div>
    </div>
  );
};