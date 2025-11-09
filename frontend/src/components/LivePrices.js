import React, { useState, useEffect } from 'react';
import { Activity, TrendingUp, TrendingDown } from 'lucide-react';
import { API_URL } from '../config';

export default function LivePrices() {
  const [prices, setPrices] = useState({
    BTCUSDT: { price: 0, change: 0, high: 0, low: 0 },
    ETHUSDT: { price: 0, change: 0, high: 0, low: 0 }
  });
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Simulate WebSocket connection (in production, use actual WebSocket)
    const updatePrices = async () => {
      try {
        const [btcRes, ethRes] = await Promise.all([
          fetch(`${API_URL}/api/price/BTCUSDT`).then(r => r.json()),
          fetch(`${API_URL}/api/price/ETHUSDT`).then(r => r.json())
        ]);

        if (btcRes.success && ethRes.success) {
          setPrices(prev => ({
            BTCUSDT: {
              price: btcRes.price,
              change: ((btcRes.price - prev.BTCUSDT.price) / prev.BTCUSDT.price * 100) || 0,
              high: Math.max(btcRes.price, prev.BTCUSDT.high),
              low: prev.BTCUSDT.low === 0 ? btcRes.price : Math.min(btcRes.price, prev.BTCUSDT.low)
            },
            ETHUSDT: {
              price: ethRes.price,
              change: ((ethRes.price - prev.ETHUSDT.price) / prev.ETHUSDT.price * 100) || 0,
              high: Math.max(ethRes.price, prev.ETHUSDT.high),
              low: prev.ETHUSDT.low === 0 ? ethRes.price : Math.min(ethRes.price, prev.ETHUSDT.low)
            }
          }));
          setConnected(true);
        }
      } catch (error) {
        console.error('Error fetching prices:', error);
        setConnected(false);
      }
    };

    updatePrices();
    const interval = setInterval(updatePrices, 2000); // Update every 2 seconds
    return () => clearInterval(interval);
  }, []);

  const PriceCard = ({ symbol, data, icon: Icon, color }) => (
    <div className={`bg-gradient-to-br ${color} rounded-xl p-4 border border-white/20`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <Icon className="w-5 h-5 text-white" />
          <span className="text-white font-semibold">{symbol}</span>
        </div>
        <div className="flex items-center space-x-1">
          <Activity className={`w-4 h-4 ${connected ? 'text-green-400 animate-pulse' : 'text-gray-400'}`} />
          <span className="text-xs text-white/70">{connected ? 'Live' : 'Offline'}</span>
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex items-baseline space-x-2">
          <span className="text-2xl font-bold text-white">
            ${data.price.toLocaleString()}
          </span>
          {data.change !== 0 && (
            <div className={`flex items-center space-x-1 ${data.change > 0 ? 'text-green-400' : 'text-red-400'}`}>
              {data.change > 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
              <span className="text-sm font-medium">{Math.abs(data.change).toFixed(2)}%</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="bg-white/10 rounded px-2 py-1">
            <span className="text-white/60">High:</span>
            <span className="ml-1 text-white font-medium">${data.high.toLocaleString()}</span>
          </div>
          <div className="bg-white/10 rounded px-2 py-1">
            <span className="text-white/60">Low:</span>
            <span className="ml-1 text-white font-medium">${data.low.toLocaleString()}</span>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <PriceCard
        symbol="BTC/USDT"
        data={prices.BTCUSDT}
        icon={TrendingUp}
        color="from-orange-500/20 to-orange-600/20"
      />
      <PriceCard
        symbol="ETH/USDT"
        data={prices.ETHUSDT}
        icon={TrendingUp}
        color="from-purple-500/20 to-purple-600/20"
      />
    </div>
  );
}
