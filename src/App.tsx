import React, { useState } from 'react';
import { ChessBoard } from './components/ChessBoard';
import { GameStatus } from './components/GameStatus';
import { MoveHistory } from './components/MoveHistory';
import { ChessProvider } from './context/ChessContext';
import { Crown } from 'lucide-react';

function App() {
  return (
    <ChessProvider>
      <div className="min-h-screen bg-gray-900 text-white p-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold flex items-center justify-center gap-3">
            <Crown className="w-10 h-10 text-yellow-500" />
            React Chess
          </h1>
          <p className="text-gray-400 mt-2">Play against the computer with MinMax AI</p>
        </header>
        
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <ChessBoard />
          </div>
          <div className="space-y-6">
            <GameStatus />
            <MoveHistory />
          </div>
        </div>
      </div>
    </ChessProvider>
  );
}

export default App;