import React from 'react';
import { TrendingUp, RefreshCw } from 'lucide-react';

export default function Dashboard({ prices, onRefresh }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
      {/* BTC Price Card */}
      <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-4 sm:p-6 border border-white/20 hover:border-blue-500/50 transition-all">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="bg-orange-500/20 p-3 rounded-xl">
              <svg className="w-6 h-6 text-orange-500" viewBox="0 0 24 24" fill="currentColor">
                <path d="M23.638 14.904c-1.602 6.43-8.113 10.34-14.542 8.736C2.67 22.05-1.244 15.525.362 9.105 1.962 2.67 8.475-1.243 14.9.358c6.43 1.605 10.342 8.115 8.738 14.548v-.002zm-6.35-4.613c.24-1.59-.974-2.45-2.64-3.03l.54-2.153-1.315-.33-.525 2.107c-.345-.087-.705-.167-1.064-.25l.526-2.127-1.32-.33-.54 2.165c-.285-.067-.565-.132-.84-.2l-1.815-.45-.35 1.407s.975.225.955.236c.535.136.63.486.615.766l-1.477 5.92c-.075.166-.24.406-.614.314.015.02-.96-.24-.96-.24l-.66 1.51 1.71.426.93.242-.54 2.19 1.32.327.54-2.17c.36.1.705.19 1.05.273l-.51 2.154 1.32.33.545-2.19c2.24.427 3.93.257 4.64-1.774.57-1.637-.03-2.58-1.217-3.196.854-.193 1.5-.76 1.68-1.93h.01zm-3.01 4.22c-.404 1.64-3.157.75-4.05.53l.72-2.9c.896.23 3.757.67 3.33 2.37zm.41-4.24c-.37 1.49-2.662.735-3.405.55l.654-2.64c.744.18 3.137.524 2.75 2.084v.006z"/>
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-400">Bitcoin</p>
              <p className="text-xs text-gray-500">BTCUSDT</p>
            </div>
          </div>
          <TrendingUp className="w-5 h-5 text-green-400" />
        </div>
        <div className="flex items-baseline space-x-2">
          <p className="text-2xl sm:text-3xl font-bold text-white">
            ${prices.btc ? parseFloat(prices.btc).toLocaleString() : '0'}
          </p>
          <p className="text-xs sm:text-sm text-green-400">+2.4%</p>
        </div>
      </div>

      {/* ETH Price Card */}
      <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-4 sm:p-6 border border-white/20 hover:border-purple-500/50 transition-all">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="bg-purple-500/20 p-3 rounded-xl">
              <svg className="w-6 h-6 text-purple-500" viewBox="0 0 24 24" fill="currentColor">
                <path d="M11.944 17.97L4.58 13.62 11.943 24l7.37-10.38-7.372 4.35h.003zM12.056 0L4.69 12.223l7.365 4.354 7.365-4.35L12.056 0z"/>
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-400">Ethereum</p>
              <p className="text-xs text-gray-500">ETHUSDT</p>
            </div>
          </div>
          <TrendingUp className="w-5 h-5 text-green-400" />
        </div>
        <div className="flex items-baseline space-x-2">
          <p className="text-2xl sm:text-3xl font-bold text-white">
            ${prices.eth ? parseFloat(prices.eth).toLocaleString() : '0'}
          </p>
          <p className="text-xs sm:text-sm text-green-400">+1.8%</p>
        </div>
      </div>

      {/* Refresh Button */}
      <div className="md:col-span-2">
        <button
          onClick={onRefresh}
          className="w-full bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl py-3 px-4 text-white font-medium transition-all flex items-center justify-center space-x-2"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Refresh Prices</span>
        </button>
      </div>
    </div>
  );
}
