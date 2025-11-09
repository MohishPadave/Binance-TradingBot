import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, Wallet, BookOpen, LogOut, History, Bell } from 'lucide-react';
import AuthPage from './components/AuthPage';
import Dashboard from './components/Dashboard';
import OrderPanel from './components/OrderPanel';
import OpenOrders from './components/OpenOrders';
import BlogPage from './components/BlogPage';
import OrderHistory from './components/OrderHistory';
import TelegramSettings from './components/TelegramSettings';
import LivePrices from './components/LivePrices';
import { API_URL } from './config';

function App() {
  const [user, setUser] = useState(null);
  const [connected, setConnected] = useState(false);
  const [balance, setBalance] = useState('0.00');
  const [prices, setPrices] = useState({ btc: 0, eth: 0 });
  const [currentPage, setCurrentPage] = useState('dashboard');

  const handleConnect = async (apiKey, apiSecret) => {
    try {
      const response = await axios.post(`${API_URL}/api/connect`, {
        api_key: apiKey,
        api_secret: apiSecret
      });
      
      if (response.data.success) {
        setConnected(true);
        setBalance(response.data.balance);
        updatePrices();
      } else {
        alert('Connection failed: ' + response.data.message);
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  useEffect(() => {
    // Check if user is logged in
    const savedUser = localStorage.getItem('tradingBotUser');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setUser(userData);
      // Auto-connect if credentials exist
      if (userData.apiKey && userData.apiSecret) {
        handleConnect(userData.apiKey, userData.apiSecret);
      }
    }
    // eslint-disable-next-line
  }, []);

  const handleAuth = (userData) => {
    setUser(userData);
    localStorage.setItem('tradingBotUser', JSON.stringify(userData));
    if (userData.apiKey && userData.apiSecret) {
      handleConnect(userData.apiKey, userData.apiSecret);
    }
  };

  const handleLogout = () => {
    setUser(null);
    setConnected(false);
    localStorage.removeItem('tradingBotUser');
    setCurrentPage('dashboard');
  };

  const updatePrices = async () => {
    try {
      const [btcRes, ethRes] = await Promise.all([
        axios.get(`${API_URL}/api/price/BTCUSDT`),
        axios.get(`${API_URL}/api/price/ETHUSDT`)
      ]);
      
      if (btcRes.data.success && ethRes.data.success) {
        setPrices({
          btc: btcRes.data.price,
          eth: ethRes.data.price
        });
      }
    } catch (error) {
      console.error('Error updating prices:', error);
    }
  };

  useEffect(() => {
    if (connected) {
      const interval = setInterval(updatePrices, 10000);
      return () => clearInterval(interval);
    }
  }, [connected]);

  if (!user) {
    return <AuthPage onAuth={handleAuth} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-lg border-b border-white/10 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-2 rounded-lg">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div className="hidden sm:block">
                <h1 className="text-xl sm:text-2xl font-bold text-white">Binance Futures Bot</h1>
                <p className="text-xs sm:text-sm text-gray-400">USDT-M Testnet</p>
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex items-center space-x-2 sm:space-x-3">
              <button
                onClick={() => setCurrentPage('dashboard')}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all ${
                  currentPage === 'dashboard'
                    ? 'bg-blue-500/20 text-blue-400'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <TrendingUp className="w-4 h-4" />
                <span className="hidden sm:inline text-sm">Dashboard</span>
              </button>
              <button
                onClick={() => setCurrentPage('history')}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all ${
                  currentPage === 'history'
                    ? 'bg-blue-500/20 text-blue-400'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <History className="w-4 h-4" />
                <span className="hidden sm:inline text-sm">History</span>
              </button>
              <button
                onClick={() => setCurrentPage('alerts')}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all ${
                  currentPage === 'alerts'
                    ? 'bg-blue-500/20 text-blue-400'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Bell className="w-4 h-4" />
                <span className="hidden sm:inline text-sm">Alerts</span>
              </button>
              <button
                onClick={() => setCurrentPage('blog')}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all ${
                  currentPage === 'blog'
                    ? 'bg-blue-500/20 text-blue-400'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <BookOpen className="w-4 h-4" />
                <span className="hidden sm:inline text-sm">Blog</span>
              </button>
              
              {connected && (
                <div className="hidden lg:flex bg-green-500/20 border border-green-500/30 rounded-lg px-3 py-2">
                  <div className="flex items-center space-x-2">
                    <Wallet className="w-4 h-4 text-green-400" />
                    <div>
                      <p className="text-xs text-gray-400">Balance</p>
                      <p className="text-sm font-bold text-white">${parseFloat(balance).toLocaleString()}</p>
                    </div>
                  </div>
                </div>
              )}

              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-3 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-all"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden sm:inline text-sm">Logout</span>
              </button>
            </nav>
          </div>

          {/* Mobile Balance */}
          {connected && (
            <div className="md:hidden mt-3 bg-green-500/20 border border-green-500/30 rounded-lg px-4 py-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Balance:</span>
                <span className="text-lg font-bold text-white">${parseFloat(balance).toLocaleString()}</span>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        {currentPage === 'blog' ? (
          <BlogPage />
        ) : currentPage === 'history' ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
            <OrderHistory />
            <TelegramSettings />
          </div>
        ) : currentPage === 'alerts' ? (
          <div className="space-y-6">
            <LivePrices />
            <TelegramSettings />
          </div>
        ) : (
          <>
            {!connected && (
              <div className="mb-6 bg-yellow-500/20 border border-yellow-500/30 rounded-lg p-4">
                <p className="text-yellow-400 text-center">
                  ⚠️ Not connected to Binance. {user.apiKey ? 'Connecting...' : 'Please add API credentials in your profile.'}
                </p>
              </div>
            )}
            
            <LivePrices />
            
            <div className="mt-6">
              <Dashboard prices={prices} onRefresh={updatePrices} />
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 mt-4 sm:mt-6">
              <div className="lg:col-span-2">
                <OrderPanel />
              </div>
              <div>
                <OpenOrders />
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
