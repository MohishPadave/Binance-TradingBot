import React from 'react';
import { BookOpen, TrendingUp, Shield, Zap, Clock, Grid3x3, Target } from 'lucide-react';

const blogPosts = [
  {
    id: 1,
    title: 'Market Orders',
    icon: TrendingUp,
    color: 'from-blue-500 to-cyan-500',
    content: 'A market order is an instruction to buy or sell immediately at the best available current price. It guarantees execution but not the execution price.',
    details: [
      'Executes immediately at current market price',
      'Best for: Quick entry/exit when speed matters',
      'Risk: Price slippage in volatile markets',
      'Example: Buy 0.001 BTC at whatever the current price is'
    ]
  },
  {
    id: 2,
    title: 'Limit Orders',
    icon: Target,
    color: 'from-purple-500 to-pink-500',
    content: 'A limit order sets the maximum or minimum price at which you are willing to buy or sell. It gives you price control but may not execute if the price doesn\'t reach your limit.',
    details: [
      'Executes only at your specified price or better',
      'Best for: Getting a specific price point',
      'Risk: May not execute if price doesn\'t reach limit',
      'Example: Buy BTC only if price drops to $40,000'
    ]
  },
  {
    id: 3,
    title: 'Stop-Limit Orders',
    icon: Shield,
    color: 'from-orange-500 to-red-500',
    content: 'A stop-limit order combines stop and limit orders. When the stop price is reached, it triggers a limit order. Used for breakout trading strategies.',
    details: [
      'Two prices: Stop price (trigger) and Limit price (execution)',
      'Best for: Breakout trading, limiting losses',
      'Risk: May not execute in fast-moving markets',
      'Example: If BTC hits $45k (stop), buy at $45.1k (limit)'
    ]
  },
  {
    id: 4,
    title: 'OCO Orders (One-Cancels-Other)',
    icon: Zap,
    color: 'from-green-500 to-emerald-500',
    content: 'OCO orders place two orders simultaneously: a take-profit and a stop-loss. When one executes, the other is automatically cancelled. Essential for risk management.',
    details: [
      'Places take-profit and stop-loss together',
      'Best for: Automated risk management',
      'Benefit: Set and forget - protects profits and limits losses',
      'Example: Sell at $50k (profit) OR $40k (loss protection)'
    ]
  },
  {
    id: 5,
    title: 'TWAP (Time-Weighted Average Price)',
    icon: Clock,
    color: 'from-indigo-500 to-purple-500',
    content: 'TWAP splits a large order into smaller chunks executed at regular intervals. This reduces market impact and achieves a better average price.',
    details: [
      'Splits large orders into smaller parts over time',
      'Best for: Large orders, reducing market impact',
      'Benefit: Better average price, less slippage',
      'Example: Buy 1 BTC split into 10 orders over 100 seconds'
    ]
  },
  {
    id: 6,
    title: 'Grid Trading',
    icon: Grid3x3,
    color: 'from-yellow-500 to-orange-500',
    content: 'Grid trading places multiple buy and sell orders at predetermined intervals within a price range. It profits from market volatility by buying low and selling high automatically.',
    details: [
      'Places multiple orders in a price range',
      'Best for: Ranging/sideways markets',
      'Benefit: Automated profit-taking from volatility',
      'Example: 10 orders between $40k-$50k, profit from oscillations'
    ]
  }
];

const glossary = [
  { term: 'Futures', definition: 'Contracts to buy/sell an asset at a predetermined price at a future date' },
  { term: 'USDT-M', definition: 'USDT-Margined futures - contracts settled in USDT stablecoin' },
  { term: 'Leverage', definition: 'Borrowing funds to increase position size (e.g., 10x leverage = 10x exposure)' },
  { term: 'Long Position', definition: 'Buying an asset expecting price to increase' },
  { term: 'Short Position', definition: 'Selling an asset expecting price to decrease' },
  { term: 'Slippage', definition: 'Difference between expected and actual execution price' },
  { term: 'Liquidity', definition: 'How easily an asset can be bought/sold without affecting price' },
  { term: 'Volatility', definition: 'Rate at which price increases or decreases' },
  { term: 'Testnet', definition: 'Simulated trading environment with fake money for testing' }
];

export default function BlogPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-6 sm:p-8 border border-white/20">
        <div className="flex items-center space-x-3 mb-4">
          <BookOpen className="w-8 h-8 text-blue-400" />
          <h1 className="text-2xl sm:text-3xl font-bold text-white">Trading Education</h1>
        </div>
        <p className="text-gray-300 text-sm sm:text-base">
          Learn about different order types and trading concepts used in this platform
        </p>
      </div>

      {/* Order Types */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
        {blogPosts.map((post) => {
          const Icon = post.icon;
          return (
            <div
              key={post.id}
              className="bg-white/10 backdrop-blur-xl rounded-2xl p-6 border border-white/20 hover:border-white/40 transition-all hover:transform hover:scale-105"
            >
              <div className="flex items-start space-x-4 mb-4">
                <div className={`bg-gradient-to-r ${post.color} p-3 rounded-xl`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-white mb-2">{post.title}</h3>
                  <p className="text-gray-300 text-sm">{post.content}</p>
                </div>
              </div>

              <div className="space-y-2 mt-4 pt-4 border-t border-white/10">
                {post.details.map((detail, idx) => (
                  <div key={idx} className="flex items-start space-x-2">
                    <span className="text-blue-400 mt-1">•</span>
                    <p className="text-gray-400 text-sm">{detail}</p>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Glossary */}
      <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-6 sm:p-8 border border-white/20">
        <h2 className="text-2xl font-bold text-white mb-6">Trading Glossary</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {glossary.map((item, idx) => (
            <div key={idx} className="bg-white/5 rounded-lg p-4 border border-white/10">
              <h4 className="font-semibold text-blue-400 mb-2">{item.term}</h4>
              <p className="text-gray-300 text-sm">{item.definition}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Warning */}
      <div className="bg-red-500/20 border border-red-500/30 rounded-2xl p-6">
        <h3 className="text-xl font-bold text-red-400 mb-3">⚠️ Risk Warning</h3>
        <p className="text-gray-300 text-sm">
          Trading futures involves substantial risk of loss. This platform uses Binance Testnet with simulated funds. 
          Never trade with money you cannot afford to lose. Always do your own research and consider seeking advice 
          from independent financial advisors.
        </p>
      </div>
    </div>
  );
}
