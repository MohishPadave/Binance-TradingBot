import React, { useState } from 'react';
import { Lock, Zap } from 'lucide-react';

export default function ConnectionCard({ onConnect, loading }) {
  const [apiKey, setApiKey] = useState('QN6mQ5PxWbZhZ8h7UBYiwnvpZqAfbwAQ4h8pozxtXgTkkpqfWnkGJNdYD1uhz9in');
  const [apiSecret, setApiSecret] = useState('uqU8sqEe8hldYXWSYtv4mwHYLG59dFtUvpH5hdne4ohWqnMOy1ETQjQiDrxeIz86');

  const handleSubmit = (e) => {
    e.preventDefault();
    onConnect(apiKey, apiSecret);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl mb-4">
            <Zap className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">Binance Futures Bot</h1>
          <p className="text-gray-400">Connect to start trading on testnet</p>
        </div>

        <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                API Key
              </label>
              <input
                type="text"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                placeholder="Enter your API key"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                API Secret
              </label>
              <input
                type="password"
                value={apiSecret}
                onChange={(e) => setApiSecret(e.target.value)}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                placeholder="Enter your API secret"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Connecting...</span>
                </>
              ) : (
                <>
                  <Lock className="w-5 h-5" />
                  <span>Connect to Binance</span>
                </>
              )}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-white/10">
            <p className="text-xs text-gray-400 text-center">
              🔒 Secure connection to Binance Testnet
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
