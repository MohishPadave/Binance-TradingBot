import React, { useState } from 'react';
import axios from 'axios';
import { ShoppingCart, TrendingUp, Shield, Zap, Grid3x3, Clock } from 'lucide-react';

const tabs = [
  { id: 'market', name: 'Market', icon: ShoppingCart },
  { id: 'limit', name: 'Limit', icon: TrendingUp },
  { id: 'stop-limit', name: 'Stop-Limit', icon: Shield },
  { id: 'oco', name: 'OCO', icon: Zap },
  { id: 'twap', name: 'TWAP', icon: Clock },
  { id: 'grid', name: 'Grid', icon: Grid3x3 },
];

export default function OrderPanel() {
  const [activeTab, setActiveTab] = useState('market');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const showMessage = (text, type = 'success') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 5000);
  };

  const handleMarketOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    
    try {
      const response = await axios.post('/api/market_order', {
        symbol: formData.get('symbol'),
        side: formData.get('side'),
        quantity: formData.get('quantity')
      });
      
      if (response.data.success) {
        showMessage(`✓ Market order placed! Order ID: ${response.data.order_id}`, 'success');
        e.target.reset();
      } else {
        showMessage(response.data.message, 'error');
      }
    } catch (error) {
      showMessage(error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleLimitOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    
    try {
      const response = await axios.post('/api/limit_order', {
        symbol: formData.get('symbol'),
        side: formData.get('side'),
        quantity: formData.get('quantity'),
        price: formData.get('price')
      });
      
      if (response.data.success) {
        showMessage(`✓ Limit order placed! Order ID: ${response.data.order_id}`, 'success');
        e.target.reset();
      } else {
        showMessage(response.data.message, 'error');
      }
    } catch (error) {
      showMessage(error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleStopLimitOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    
    try {
      const response = await axios.post('/api/stop_limit_order', {
        symbol: formData.get('symbol'),
        side: formData.get('side'),
        quantity: formData.get('quantity'),
        stop_price: formData.get('stop_price'),
        limit_price: formData.get('limit_price')
      });
      
      if (response.data.success) {
        showMessage(`✓ Stop-Limit order placed! Order ID: ${response.data.order_id}`, 'success');
        e.target.reset();
      } else {
        showMessage(response.data.message, 'error');
      }
    } catch (error) {
      showMessage(error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleOCOOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    
    try {
      const response = await axios.post('/api/oco_order', {
        symbol: formData.get('symbol'),
        side: formData.get('side'),
        quantity: formData.get('quantity'),
        tp_price: formData.get('tp_price'),
        sl_price: formData.get('sl_price')
      });
      
      if (response.data.success) {
        showMessage(`✓ OCO orders placed! TP: ${response.data.tp_order_id}, SL: ${response.data.sl_order_id}`, 'success');
        e.target.reset();
      } else {
        showMessage(response.data.message, 'error');
      }
    } catch (error) {
      showMessage(error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleTWAPOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    
    showMessage('⏳ Executing TWAP... This will take some time.', 'info');
    
    try {
      const response = await axios.post('/api/twap_order', {
        symbol: formData.get('symbol'),
        side: formData.get('side'),
        quantity: formData.get('quantity'),
        num_orders: formData.get('num_orders'),
        interval: formData.get('interval')
      });
      
      if (response.data.success) {
        showMessage(`✓ ${response.data.message}`, 'success');
        e.target.reset();
      } else {
        showMessage(response.data.message, 'error');
      }
    } catch (error) {
      showMessage(error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleGridOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    
    try {
      const response = await axios.post('/api/grid_order', {
        symbol: formData.get('symbol'),
        lower_price: formData.get('lower_price'),
        upper_price: formData.get('upper_price'),
        num_grids: formData.get('num_grids'),
        quantity_per_grid: formData.get('quantity_per_grid')
      });
      
      if (response.data.success) {
        showMessage(`✓ ${response.data.message}`, 'success');
        e.target.reset();
      } else {
        showMessage(response.data.message, 'error');
      }
    } catch (error) {
      showMessage(error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 overflow-hidden">
      {/* Tabs */}
      <div className="flex overflow-x-auto border-b border-white/10 scrollbar-hide">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-4 sm:px-6 py-3 sm:py-4 font-medium transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-blue-500/20 text-blue-400 border-b-2 border-blue-500'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="text-sm sm:text-base">{tab.name}</span>
            </button>
          );
        })}
      </div>

      {/* Content */}
      <div className="p-4 sm:p-6">
        {message && (
          <div className={`mb-4 p-4 rounded-lg ${
            message.type === 'success' ? 'bg-green-500/20 text-green-400 border border-green-500/30' :
            message.type === 'error' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
            'bg-blue-500/20 text-blue-400 border border-blue-500/30'
          }`}>
            {message.text}
          </div>
        )}

        {activeTab === 'market' && (
          <form onSubmit={handleMarketOrder} className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">Market Order</h3>
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3 mb-4">
              <p className="text-xs text-yellow-400">
                💡 Tip: With $5,000 balance, use small quantities like 0.001 BTC (~$100)
              </p>
            </div>
            <InputField label="Symbol" name="symbol" defaultValue="BTCUSDT" />
            <SelectField label="Side" name="side" options={['BUY', 'SELL']} />
            <InputField label="Quantity (BTC)" name="quantity" type="number" step="0.001" defaultValue="0.001" placeholder="0.001" />
            <SubmitButton loading={loading}>Place Market Order</SubmitButton>
          </form>
        )}

        {activeTab === 'limit' && (
          <form onSubmit={handleLimitOrder} className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">Limit Order</h3>
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3 mb-4">
              <p className="text-xs text-blue-400">
                💡 Limit orders execute only at your specified price or better
              </p>
            </div>
            <InputField label="Symbol" name="symbol" defaultValue="BTCUSDT" />
            <SelectField label="Side" name="side" options={['BUY', 'SELL']} />
            <InputField label="Quantity (BTC)" name="quantity" type="number" step="0.001" defaultValue="0.001" placeholder="0.001" />
            <InputField label="Price (USDT)" name="price" type="number" step="0.01" defaultValue="100000" placeholder="100000" />
            <SubmitButton loading={loading}>Place Limit Order</SubmitButton>
          </form>
        )}

        {activeTab === 'stop-limit' && (
          <form onSubmit={handleStopLimitOrder} className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">Stop-Limit Order</h3>
            <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-3 mb-4">
              <p className="text-xs text-purple-400">
                💡 Triggers a limit order when stop price is reached
              </p>
            </div>
            <InputField label="Symbol" name="symbol" defaultValue="BTCUSDT" />
            <SelectField label="Side" name="side" options={['BUY', 'SELL']} />
            <InputField label="Quantity (BTC)" name="quantity" type="number" step="0.001" defaultValue="0.001" placeholder="0.001" />
            <InputField label="Stop Price (USDT)" name="stop_price" type="number" step="0.01" defaultValue="105000" placeholder="105000" />
            <InputField label="Limit Price (USDT)" name="limit_price" type="number" step="0.01" defaultValue="105100" placeholder="105100" />
            <SubmitButton loading={loading}>Place Stop-Limit Order</SubmitButton>
          </form>
        )}

        {activeTab === 'oco' && (
          <form onSubmit={handleOCOOrder} className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">OCO Order</h3>
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 mb-4">
              <p className="text-xs text-red-400">
                💡 Places take-profit and stop-loss together. One cancels the other.
              </p>
            </div>
            <InputField label="Symbol" name="symbol" defaultValue="BTCUSDT" />
            <SelectField label="Side" name="side" options={['SELL', 'BUY']} />
            <InputField label="Quantity (BTC)" name="quantity" type="number" step="0.001" defaultValue="0.001" placeholder="0.001" />
            <InputField label="Take Profit Price (USDT)" name="tp_price" type="number" step="0.01" defaultValue="110000" placeholder="110000" />
            <InputField label="Stop Loss Price (USDT)" name="sl_price" type="number" step="0.01" defaultValue="95000" placeholder="95000" />
            <SubmitButton loading={loading}>Place OCO Order</SubmitButton>
          </form>
        )}

        {activeTab === 'twap' && (
          <form onSubmit={handleTWAPOrder} className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">TWAP Order</h3>
            <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3 mb-4">
              <p className="text-xs text-green-400">
                💡 Splits large orders into smaller chunks over time
              </p>
            </div>
            <InputField label="Symbol" name="symbol" defaultValue="BTCUSDT" />
            <SelectField label="Side" name="side" options={['BUY', 'SELL']} />
            <InputField label="Total Quantity (BTC)" name="quantity" type="number" step="0.001" defaultValue="0.005" placeholder="0.005" />
            <InputField label="Number of Orders" name="num_orders" type="number" defaultValue="5" min="2" placeholder="5" />
            <InputField label="Interval (seconds)" name="interval" type="number" defaultValue="10" min="1" placeholder="10" />
            <SubmitButton loading={loading}>Execute TWAP</SubmitButton>
          </form>
        )}

        {activeTab === 'grid' && (
          <form onSubmit={handleGridOrder} className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">Grid Trading</h3>
            <div className="bg-orange-500/10 border border-orange-500/30 rounded-lg p-3 mb-4">
              <p className="text-xs text-orange-400">
                💡 Places multiple buy/sell orders in a price range
              </p>
            </div>
            <InputField label="Symbol" name="symbol" defaultValue="BTCUSDT" />
            <InputField label="Lower Price (USDT)" name="lower_price" type="number" step="0.01" defaultValue="95000" placeholder="95000" />
            <InputField label="Upper Price (USDT)" name="upper_price" type="number" step="0.01" defaultValue="105000" placeholder="105000" />
            <InputField label="Number of Grids" name="num_grids" type="number" defaultValue="5" min="2" placeholder="5" />
            <InputField label="Quantity per Grid (BTC)" name="quantity_per_grid" type="number" step="0.001" defaultValue="0.001" placeholder="0.001" />
            <SubmitButton loading={loading}>Setup Grid</SubmitButton>
          </form>
        )}
      </div>
    </div>
  );
}

function InputField({ label, name, type = 'text', ...props }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-300 mb-2">{label}</label>
      <input
        type={type}
        name={name}
        className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
        required
        {...props}
      />
    </div>
  );
}

function SelectField({ label, name, options }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(options[0]);

  return (
    <div>
      <label className="block text-sm font-medium text-gray-300 mb-2">{label}</label>
      <input type="hidden" name={name} value={selected} />
      <div className="relative">
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition flex items-center justify-between"
        >
          <span className={`font-medium ${selected === 'BUY' ? 'text-green-400' : 'text-red-400'}`}>
            {selected}
          </span>
          <svg className={`w-5 h-5 transition-transform ${isOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        
        {isOpen && (
          <div className="absolute z-10 w-full mt-2 bg-gray-900 border border-white/20 rounded-lg shadow-xl overflow-hidden">
            {options.map(opt => (
              <button
                key={opt}
                type="button"
                onClick={() => {
                  setSelected(opt);
                  setIsOpen(false);
                }}
                className={`w-full px-4 py-3 text-left transition-all ${
                  selected === opt
                    ? 'bg-blue-500/20 text-blue-400'
                    : 'text-white hover:bg-white/10'
                } ${opt === 'BUY' ? 'hover:text-green-400' : 'hover:text-red-400'}`}
              >
                <span className="font-medium">{opt}</span>
                {opt === 'BUY' && <span className="text-xs ml-2 text-gray-400">Long Position</span>}
                {opt === 'SELL' && <span className="text-xs ml-2 text-gray-400">Short Position</span>}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function SubmitButton({ loading, children }) {
  return (
    <button
      type="submit"
      disabled={loading}
      className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
    >
      {loading ? (
        <>
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
          <span>Processing...</span>
        </>
      ) : (
        <span>{children}</span>
      )}
    </button>
  );
}
