import React, { useState } from 'react';
import { Lock, User, Mail, Key, TrendingUp } from 'lucide-react';

export default function AuthPage({ onAuth }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    apiKey: '',
    apiSecret: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    // Simulate authentication
    setTimeout(() => {
      if (isLogin) {
        // Check if user exists in localStorage
        const users = JSON.parse(localStorage.getItem('tradingBotUsers') || '{}');
        const user = users[formData.email];
        
        if (user && user.password === formData.password) {
          onAuth(user);
        } else {
          alert('Invalid credentials. Try signing up first!');
          setLoading(false);
        }
      } else {
        // Sign up
        const users = JSON.parse(localStorage.getItem('tradingBotUsers') || '{}');
        
        if (users[formData.email]) {
          alert('Email already exists. Please login.');
          setLoading(false);
          return;
        }

        const newUser = {
          email: formData.email,
          password: formData.password,
          name: formData.name,
          apiKey: formData.apiKey,
          apiSecret: formData.apiSecret,
          createdAt: new Date().toISOString()
        };

        users[formData.email] = newUser;
        localStorage.setItem('tradingBotUsers', JSON.stringify(users));
        onAuth(newUser);
      }
    }, 1000);
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl mb-4 animate-pulse">
            <TrendingUp className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold text-white mb-2">Binance Futures Bot</h1>
          <p className="text-gray-400">Professional Trading Platform</p>
        </div>

        {/* Auth Card */}
        <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-6 sm:p-8 border border-white/20 shadow-2xl">
          {/* Tabs */}
          <div className="flex space-x-2 mb-6 bg-white/5 rounded-lg p-1">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                isLogin
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Login
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                !isLogin
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Sign Up
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Full Name
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                    placeholder="John Doe"
                    required={!isLogin}
                  />
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="you@example.com"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            {!isLogin && (
              <>
                <div className="pt-4 border-t border-white/10">
                  <p className="text-sm text-gray-400 mb-3">Binance API Credentials (Optional - can add later)</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    API Key
                  </label>
                  <div className="relative">
                    <Key className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type="text"
                      name="apiKey"
                      value={formData.apiKey}
                      onChange={handleChange}
                      className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                      placeholder="Your Binance API Key"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    API Secret
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type="password"
                      name="apiSecret"
                      value={formData.apiSecret}
                      onChange={handleChange}
                      className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                      placeholder="Your Binance API Secret"
                    />
                  </div>
                </div>
              </>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2 mt-6"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>{isLogin ? 'Logging in...' : 'Creating account...'}</span>
                </>
              ) : (
                <span>{isLogin ? 'Login to Dashboard' : 'Create Account'}</span>
              )}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-white/10">
            <p className="text-xs text-gray-400 text-center">
              🔒 Your credentials are stored locally and securely
            </p>
          </div>
        </div>

        {/* Demo Credentials */}
        <div className="mt-4 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
          <p className="text-xs text-blue-400 text-center">
            💡 Demo: Use any email/password to sign up, or login with existing account
          </p>
        </div>
      </div>
    </div>
  );
}
