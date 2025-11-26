import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Zap, MessageSquare, Brain, Search, AlertCircle, TrendingUp, UserCheck, FileText, CheckCircle, Clock, Activity, Sparkles } from 'lucide-react';

const MultiAgentSupportUI = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! How can I help you today? I have 11 AI agents ready to assist you.', timestamp: new Date() }
  ]);
  const [input, setInput] = useState('');
  const [activeAgents, setActiveAgents] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isProcessing]);

  const allAgents = [
    { id: 'orchestrator', name: 'Orchestrator', icon: Bot, color: 'bg-gray-700', description: 'Coordinates all agents' },
    { id: 'intent', name: 'Intent Detection', icon: Brain, color: 'bg-purple-500', description: 'Understands what customer wants' },
    { id: 'classifier', name: 'Classifier', icon: FileText, color: 'bg-blue-500', description: 'Categorizes the request' },
    { id: 'sentiment', name: 'Sentiment Analysis', icon: TrendingUp, color: 'bg-pink-500', description: 'Detects customer emotion' },
    { id: 'knowledge', name: 'Knowledge Search', icon: Search, color: 'bg-green-500', description: 'Finds relevant information' },
    { id: 'troubleshooting', name: 'Troubleshooting', icon: Zap, color: 'bg-yellow-500', description: 'Solves technical issues' },
    { id: 'response', name: 'Response Generator', icon: MessageSquare, color: 'bg-indigo-500', description: 'Creates the answer' },
    { id: 'escalation', name: 'Escalation', icon: AlertCircle, color: 'bg-red-500', description: 'Flags urgent issues' },
    { id: 'summarization', name: 'Summarization', icon: FileText, color: 'bg-cyan-500', description: 'Summarizes conversation' },
    { id: 'analytics', name: 'Analytics', icon: Activity, color: 'bg-orange-500', description: 'Tracks patterns' },
    { id: 'user_profile', name: 'User Profiling', icon: UserCheck, color: 'bg-teal-500', description: 'Understands customer history' }
  ];

  const callBackendAPI = async (userMessage) => {
    setIsProcessing(true);
    setActiveAgents([]);
    setError(null);

    // Animate agent activation
    const agentSequence = ['orchestrator', 'intent', 'classifier', 'sentiment', 'knowledge', 'troubleshooting', 'response', 'analytics', 'user_profile'];
    
    for (let i = 0; i < agentSequence.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 400));
      setActiveAgents(prev => [...prev, agentSequence[i]]);
    }

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        agentsUsed: data.agents_used,
        metadata: data.metadata
      }]);

    } catch (err) {
      console.error('API Error:', err);
      setError(err.message);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `❌ Error: Could not connect to backend server. Make sure Flask is running on http://localhost:5000\n\nError details: ${err.message}`,
        timestamp: new Date(),
        isError: true
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSend = () => {
    if (!input.trim() || isProcessing) return;

    setMessages(prev => [...prev, {
      role: 'user',
      content: input,
      timestamp: new Date()
    }]);

    callBackendAPI(input);
    setInput('');
  };

  const quickActions = [
    "My internet is not working",
    "I was charged twice on my bill",
    "How do I reset my password?"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 p-4 md:p-6">
      <div className="max-w-7xl mx-auto h-screen flex flex-col">
        
        {/* Enhanced Header */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="relative">
              <Bot className="w-12 h-12 text-purple-300" />
              <Sparkles className="w-5 h-5 text-yellow-300 absolute -top-1 -right-1 animate-pulse" />
            </div>
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-white">
                Multi-Agent AI Support
              </h1>
              <p className="text-purple-200 text-sm md:text-base">
                11 AI agents • Powered by Google Gemini • Real-time orchestration
              </p>
            </div>
          </div>
          
          {/* Connection Status */}
          {error && (
            <div className="mt-3 bg-red-500/20 border border-red-400 rounded-lg p-3 text-red-200 text-sm">
              ⚠️ Backend connection issue. Make sure Flask server is running: <code className="bg-black/30 px-2 py-1 rounded">python app.py</code>
            </div>
          )}
          
          {/* Stats Bar */}
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
              <div className="text-2xl font-bold text-white">{messages.length}</div>
              <div className="text-xs text-purple-200">Messages</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
              <div className="text-2xl font-bold text-white">{activeAgents.length}</div>
              <div className="text-xs text-purple-200">Active Agents</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full ${error ? 'bg-red-500' : 'bg-green-500'} animate-pulse`}></div>
                <div className="text-xs text-purple-200">{error ? 'Disconnected' : 'Connected'}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-4 min-h-0">
          
          {/* Chat Interface */}
          <div className="lg:col-span-2 bg-white/95 backdrop-blur-xl rounded-3xl border border-white/40 shadow-2xl flex flex-col overflow-hidden">
            <div className="p-4 bg-gradient-to-r from-purple-600 to-indigo-600">
              <h2 className="text-xl font-bold flex items-center gap-2 text-white">
                <MessageSquare className="w-5 h-5" />
                Customer Chat
                {isProcessing && (
                  <span className="ml-auto flex items-center gap-2 text-sm">
                    <Clock className="w-4 h-4 animate-spin" />
                    Processing...
                  </span>
                )}
              </h2>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-white">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
                  {msg.role === 'assistant' && (
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center flex-shrink-0 shadow-lg">
                      <Bot className="w-6 h-6 text-white" />
                    </div>
                  )}
                  
                  <div className={`max-w-lg ${
                    msg.role === 'user' 
                      ? 'bg-gradient-to-br from-blue-600 to-blue-700 text-white' 
                      : msg.isError
                      ? 'bg-red-50 text-red-900 border-2 border-red-300'
                      : 'bg-white text-gray-900 border-2 border-gray-200'
                  } rounded-2xl p-4 shadow-lg`}>
                    <p className="text-sm leading-relaxed whitespace-pre-line">{msg.content}</p>
                    {msg.agentsUsed && (
                      <div className="mt-3 pt-3 border-t border-gray-300">
                        <p className="text-xs text-gray-500 font-medium flex items-center gap-1">
                          <Zap className="w-3 h-3" />
                          Agents used: {msg.agentsUsed.slice(0, 5).join(', ')}
                          {msg.agentsUsed.length > 5 && ` +${msg.agentsUsed.length - 5} more`}
                        </p>
                        {msg.metadata && (
                          <p className="text-xs text-gray-400 mt-1">
                            Priority: {msg.metadata.priority} | Category: {msg.metadata.category}
                            {msg.metadata.escalated && ' | ⚠️ Escalated'}
                          </p>
                        )}
                      </div>
                    )}
                  </div>

                  {msg.role === 'user' && (
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-600 to-blue-700 flex items-center justify-center flex-shrink-0 shadow-lg">
                      <User className="w-6 h-6 text-white" />
                    </div>
                  )}
                </div>
              ))}

              {isProcessing && (
                <div className="flex gap-3 justify-start animate-fade-in">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center animate-pulse shadow-lg">
                    <Bot className="w-6 h-6 text-white" />
                  </div>
                  <div className="bg-white border-2 border-gray-200 rounded-2xl p-4 shadow-lg">
                    <div className="flex gap-2">
                      <div className="w-3 h-3 bg-purple-600 rounded-full animate-bounce"></div>
                      <div className="w-3 h-3 bg-indigo-600 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      <div className="w-3 h-3 bg-purple-600 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Quick Actions */}
            {messages.length <= 1 && (
              <div className="px-4 pb-2">
                <div className="text-xs text-gray-500 mb-2">Quick actions:</div>
                <div className="flex flex-wrap gap-2">
                  {quickActions.map((action, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        setInput(action);
                        setTimeout(() => {
                          setMessages(prev => [...prev, {
                            role: 'user',
                            content: action,
                            timestamp: new Date()
                          }]);
                          callBackendAPI(action);
                        }, 100);
                      }}
                      className="text-xs bg-purple-100 hover:bg-purple-200 text-purple-700 px-3 py-2 rounded-lg transition-colors"
                      disabled={isProcessing}
                    >
                      {action}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input */}
            <div className="p-4 bg-white border-t-2 border-gray-200">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Type your message..."
                  className="flex-1 bg-gray-100 border-2 border-gray-300 text-gray-900 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition-all"
                  disabled={isProcessing}
                />
                <button
                  onClick={handleSend}
                  disabled={isProcessing || !input.trim()}
                  className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 disabled:from-gray-400 disabled:to-gray-500 text-white rounded-xl px-6 py-3 font-semibold transition-all shadow-lg hover:shadow-xl transform hover:scale-105 disabled:scale-100"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Agent Activity Panel */}
          <div className="bg-white/95 backdrop-blur-xl rounded-3xl border border-white/40 shadow-2xl flex flex-col overflow-hidden">
            <div className="p-4 bg-gradient-to-r from-indigo-600 to-purple-600">
              <h2 className="text-xl font-bold flex items-center gap-2 text-white">
                <Activity className="w-5 h-5" />
                Live Agent Activity
              </h2>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-gradient-to-b from-gray-50 to-white">
              {allAgents.map((agent) => {
                const isActive = activeAgents.includes(agent.id);
                const isCompleted = isActive && !isProcessing;
                const Icon = agent.icon;

                return (
                  <div
                    key={agent.id}
                    className={`p-3 rounded-xl border-2 transition-all duration-300 ${
                      isActive 
                        ? 'bg-gradient-to-r from-white to-purple-50 border-purple-400 shadow-lg scale-102' 
                        : 'bg-white border-gray-200 shadow hover:shadow-md'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-11 h-11 ${agent.color} rounded-xl flex items-center justify-center ${isActive ? 'animate-pulse' : ''} shadow-md`}>
                        <Icon className="w-6 h-6 text-white" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-bold text-sm text-gray-900 truncate">{agent.name}</h3>
                        <p className="text-xs text-gray-600 truncate">{agent.description}</p>
                      </div>
                      {isActive && (
                        <div className="flex-shrink-0">
                          {isCompleted ? (
                            <CheckCircle className="w-5 h-5 text-green-500" />
                          ) : (
                            <Clock className="w-5 h-5 text-purple-600 animate-spin" />
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-out;
        }
        .scale-102 {
          transform: scale(1.02);
        }
      `}</style>
    </div>
  );
};

export default MultiAgentSupportUI;