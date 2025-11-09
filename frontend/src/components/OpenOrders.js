import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { RefreshCw, X } from 'lucide-react';

export default function OpenOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadOrders = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/open_orders');
      if (response.data.success) {
        setOrders(response.data.orders);
      }
    } catch (error) {
      console.error('Error loading orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const cancelOrder = async (symbol, orderId) => {
    if (!window.confirm('Cancel this order?')) return;
    
    try {
      const response = await axios.post('/api/cancel_order', {
        symbol,
        order_id: orderId
      });
      
      if (response.data.success) {
        loadOrders();
      }
    } catch (error) {
      console.error('Error cancelling order:', error);
    }
  };

  useEffect(() => {
    loadOrders();
    const interval = setInterval(loadOrders, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 p-4 sm:p-6">
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <h3 className="text-lg sm:text-xl font-bold text-white">Open Orders</h3>
        <button
          onClick={loadOrders}
          disabled={loading}
          className="p-2 hover:bg-white/10 rounded-lg transition-colors"
        >
          <RefreshCw className={`w-5 h-5 text-gray-400 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="space-y-3">
        {orders.length === 0 ? (
          <p className="text-center text-gray-400 py-8">No open orders</p>
        ) : (
          orders.map((order) => (
            <div
              key={order.orderId}
              className="bg-white/5 rounded-lg p-4 border border-white/10 hover:border-white/20 transition-all"
            >
              <div className="flex items-start justify-between mb-2">
                <div>
                  <p className="font-semibold text-white">{order.symbol}</p>
                  <p className="text-sm text-gray-400">
                    {order.type} {order.side}
                  </p>
                </div>
                <button
                  onClick={() => cancelOrder(order.symbol, order.orderId)}
                  className="p-1 hover:bg-red-500/20 rounded transition-colors"
                >
                  <X className="w-4 h-4 text-red-400" />
                </button>
              </div>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Quantity:</span>
                  <span className="text-white">{order.origQty}</span>
                </div>
                {order.price && (
                  <div className="flex justify-between">
                    <span className="text-gray-400">Price:</span>
                    <span className="text-white">${parseFloat(order.price).toLocaleString()}</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span className="text-gray-400">Status:</span>
                  <span className="text-blue-400">{order.status}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
