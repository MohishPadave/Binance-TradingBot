import React, { useState } from 'react';
import axios from 'axios';
import { Send, Settings, CheckCircle } from 'lucide-react';

export default function TelegramSettings() {
  const [botToken, setBotToken] = useState('');
  const [chatId, setChatId] = useState('');
  const [configured, setConfigured] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleConfigure = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/telegram/config', {
        bot_token: botToken,
        chat_id: chatId
      });
      
      if (response.data.success) {
        setConfigured(true);
        alert('✅ Telegram configured! You will receive alerts.');
      } else {
        alert('❌ Configuration failed: ' + response.data.message);
      }
    } catch (error) {
      alert('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTest = async () => {
    try {
      const response = await axios.post('/api/telegram/test');
      if (response.data.success) {
        alert('✅ Test message sent! Check your Telegram.');
      } else {
        alert('❌ Failed to send test message');
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 p-4 sm:p-6">
      <div className="flex items-center space-x-2 mb-4">
        <Send className="w-5 h-5 text-blue-400" />
        <h3 className="text-lg sm:text-xl font-bold text-white">Telegram Alerts</h3>
      </div>

      {configured ? (
        <div className="space-y-4">
          <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-4 flex items-center space-x-3">
            <CheckCircle className="w-6 h-6 text-green-400" />
            <div>
              <p className="text-green-400 font-medium">Alerts Configured</p>
              <p className="text-sm text-gray-400">You'll receive notifications for all trades</p>
            </div>
          </div>
          
          <button
            onClick={handleTest}
            className="w-full bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 text-blue-400 font-medium py-2 px-4 rounded-lg transition-all"
          >
            Send Test Message
          </button>
          
          <button
            onClick={() => setConfigured(false)}
            className="w-full text-gray-400 hover:text-white text-sm transition-colors"
          >
            Reconfigure
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3">
            <p className="text-xs text-blue-400 mb-2">📱 How to setup:</p>
            <ol className="text-xs text-gray-400 space-y-1 list-decimal list-inside">
              <li>Create bot with @BotFather on Telegram</li>
              <li>Get your bot token</li>
              <li>Start chat with your bot</li>
              <li>Get chat ID from @userinfobot</li>
            </ol>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Bot Token
            </label>
            <input
              type="text"
              value={botToken}
              onChange={(e) => setBotToken(e.target.value)}
              className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              placeholder="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Chat ID
            </label>
            <input
              type="text"
              value={chatId}
              onChange={(e) => setChatId(e.target.value)}
              className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              placeholder="123456789"
            />
          </div>

          <button
            onClick={handleConfigure}
            disabled={loading || !botToken || !chatId}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Configuring...</span>
              </>
            ) : (
              <>
                <Settings className="w-4 h-4" />
                <span>Configure Alerts</span>
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
}
