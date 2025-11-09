import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { History, RefreshCw, TrendingUp, TrendingDown } from 'lucide-react';

export default function OrderHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/order_history?limit=10');
      if (response.data.success) {
        setHistory(response.data.history);
      }
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
    const interval = setInterval(loadHistory, 30000);
    return () => clearInterval(interval);
  }, []);

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 p-4 sm:p-6">
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <div className="flex items-center space-x-2">
          <History className="w-5 h-5 text-blue-400" />
          <h3 className="text-lg sm:text-xl font-bold text-white">Order History</h3>
        </div>
        <button
          onClick={loadHistory}
          disabled={loading}
          className="p-2 hover:bg-white/10 rounded-lg transition-colors"
        >
          <RefreshCw className={`w-5 h-5 text-gray-400 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto scrollbar-hide">
        {history.length === 0 ? (
          <p className="text-center text-gray-400 py-8">No order history</p>
        ) : (
          history.map((order, idx) => (
            <div
              key={idx}
              className="bg-white/5 rounded-lg p-4 border border-white/10 hover:border-white/20 transition-all"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2">
                  {order.side === 'BUY' ? (
                    <TrendingUp className="w-4 h-4 text-green-400" />
                  ) : (
                    <TrendingDown className="w-4 h-4 text-red-400" />
                  )}
                  <div>
                    <p className="font-semibold text-white">{order.symbol}</p>
                    <p className="text-xs text-gray-400">{order.order_type}</p>
                  </div>
                </div>
                <span className={`text-xs px-2 py-1 rounded ${
                  order.status === 'FILLED' 
                    ? 'bg-green-500/20 text-green-400' 
                    : 'bg-yellow-500/20 text-yellow-400'
                }`}>
                  {order.status}
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <span className="text-gray-400">Side:</span>
                  <span className={`ml-2 font-medium ${
                    order.side === 'BUY' ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {order.side}
                  </span>
                </div>
                <div>
                  <span className="text-gray-400">Qty:</span>
                  <span className="ml-2 text-white">{order.quantity}</span>
                </div>
                {order.price && (
                  <div className="col-span-2">
                    <span className="text-gray-400">Price:</span>
                    <span className="ml-2 text-white">${parseFloat(order.price).toLocaleString()}</span>
                  </div>
                )}
                <div className="col-span-2">
                  <span className="text-gray-400 text-xs">{formatDate(order.timestamp)}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
