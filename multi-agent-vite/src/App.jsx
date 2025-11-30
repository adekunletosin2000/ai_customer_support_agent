import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Zap, MessageSquare, Brain, Search, AlertCircle, TrendingUp, UserCheck, FileText, CheckCircle, Clock, Activity, Sparkles } from 'lucide-react';

const MultiAgentSupportUI = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! How can I help you today? I have 7 AI agents ready to assist you.', timestamp: new Date() }
  ]);
  const [input, setInput] = useState('');
  const [activeAgents, setActiveAgents] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [userId, setUserId] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('connecting');
  const messagesEndRef = useRef(null);
  const initializingRef = useRef(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isProcessing]);

  useEffect(() => {
    if (!sessionId && !initializingRef.current) {
      initializeSession();
    }
  }, []);

  const allAgents = [
    { id: 'intent', name: 'Intent Detection', icon: Brain, color: 'bg-purple-500', description: 'Understands what customer wants' },
    { id: 'classifier', name: 'Issue Classifier', icon: FileText, color: 'bg-blue-500', description: 'Categorizes the request' },
    { id: 'sentiment', name: 'Sentiment Analysis', icon: TrendingUp, color: 'bg-pink-500', description: 'Detects customer emotion' },
    { id: 'knowledge', name: 'Knowledge Search', icon: Search, color: 'bg-green-500', description: 'Finds relevant information' },
    { id: 'troubleshooting', name: 'Troubleshooting', icon: Zap, color: 'bg-yellow-500', description: 'Solves technical issues' },
    { id: 'escalation_check', name: 'Escalation Checker', icon: AlertCircle, color: 'bg-red-500', description: 'Flags urgent issues' },
    { id: 'escalate_human', name: 'Human Escalation', icon: UserCheck, color: 'bg-orange-500', description: 'Transfers to human agent' }
  ];

  const initializeSession = async () => {
    if (initializingRef.current) {
      console.log('Already initializing session, skipping...');
      return false;
    }

    initializingRef.current = true;

    try {
      setConnectionStatus('connecting');
      console.log('🔄 Initializing session...');
      
      const response = await fetch('http://localhost:5000/api/chat/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      });

      if (!response.ok) {
        throw new Error(`Failed to start session: ${response.status}`);
      }

      const data = await response.json();
      setSessionId(data.session_id);
      setUserId(data.user_id);
      setConnectionStatus('connected');
      setError(null);
      
      console.log('✅ Session initialized:', data.session_id);
      console.log('✅ User ID:', data.user_id);
      return true;
    } catch (err) {
      console.error('❌ Session initialization failed:', err);
      setConnectionStatus('disconnected');
      setError(err.message);
      return false;
    } finally {
      initializingRef.current = false;
    }
  };

  const callBackendAPI = async (userMessage) => {
    if (!sessionId || !userId) {
      console.error('❌ No session available');
      setError('No active session. Reinitializing...');
      const success = await initializeSession();
      if (!success) return;
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    setIsProcessing(true);
    setActiveAgents([]);
    setError(null);

    console.log('📤 Sending message with:', { sessionId, userId, message: userMessage });

    const agentSequence = ['intent', 'classifier', 'sentiment', 'knowledge', 'troubleshooting', 'escalation_check'];
    
    for (let i = 0; i < agentSequence.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 300));
      setActiveAgents(prev => [...prev, agentSequence[i]]);
    }

    try {
      const response = await fetch('http://localhost:5000/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          user_id: userId,
          message: userMessage
        })
      });

      console.log('📥 Response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json();
        console.error('❌ Error response:', errorData);
        throw new Error(errorData.error || `Server error: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Response data:', data);
      
      if (data.metadata?.escalation_status === 'pending') {
        setActiveAgents(prev => [...prev, 'escalate_human']);
      }
      
      let responseContent = data.agent_response;
      if (typeof responseContent === 'object' && responseContent !== null) {
        responseContent = responseContent.content || 
                         responseContent.text || 
                         JSON.stringify(responseContent, null, 2);
      }
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: responseContent,
        timestamp: new Date(),
        metadata: data.metadata,
        messageCount: data.message_count
      }]);

      setConnectionStatus('connected');

    } catch (err) {
      console.error('❌ API Error:', err);
      
      const isSessionError = err.message.includes('Invalid session_id') || 
                             err.message.includes('Session not found');
      
      if (isSessionError && !sessionId) {
        setError('Session expired. Attempting to reconnect...');
        const recovered = await initializeSession();
        if (recovered) {
          setTimeout(() => callBackendAPI(userMessage), 500);
          return;
        }
      }
      
      setError(err.message);
      setConnectionStatus('error');
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `❌ Error: ${err.message}\n\n${isSessionError ? '🔄 Attempting to reconnect...' : 'Please check:\n1. Flask server is running on http://localhost:5000\n2. Try refreshing the page'}`,
        timestamp: new Date(),
        isError: true
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSend = () => {
    if (!input.trim() || isProcessing) return;

    const userMessage = input.trim();
    setInput('');

    setMessages(prev => [...prev, {
      role: 'user',
      content: userMessage,
      timestamp: new Date()
    }]);

    callBackendAPI(userMessage);
  };

  const handleQuickAction = (action) => {
    if (isProcessing || !sessionId) return;

    setMessages(prev => [...prev, {
      role: 'user',
      content: action,
      timestamp: new Date()
    }]);
    
    callBackendAPI(action);
  };

  const quickActions = [
    "My internet is not working at all!",
    "I was charged twice on my bill",
    "How do I reset my password?"
  ];

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'bg-green-500';
      case 'connecting': return 'bg-yellow-500';
      case 'disconnected':
      case 'error': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getConnectionStatusText = () => {
    switch (connectionStatus) {
      case 'connected': return 'Connected';
      case 'connecting': return 'Connecting...';
      case 'disconnected': return 'Disconnected';
      case 'error': return 'Error';
      default: return 'Unknown';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 p-4 md:p-6">
      <div className="max-w-7xl mx-auto h-screen flex flex-col">
        
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
                7 AI agents • Powered by Google Gemini • Real-time orchestration
              </p>
            </div>
          </div>
          
          {(error || connectionStatus !== 'connected') && (
            <div className={`mt-3 ${connectionStatus === 'connected' ? 'bg-green-500/20 border-green-400' : 'bg-red-500/20 border-red-400'} border rounded-lg p-3 ${connectionStatus === 'connected' ? 'text-green-200' : 'text-red-200'} text-sm`}>
              <div className="flex items-center gap-2">
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                <div className="flex-1">
                  <div className="font-semibold">
                    {connectionStatus === 'connected' ? 'Connection Restored' : 'Backend Connection Issue'}
                  </div>
                  {connectionStatus !== 'connected' && (
                    <div className="text-xs mt-1">
                      Make sure Flask server is running: <code className="bg-black/30 px-2 py-1 rounded ml-1">python app.py</code>
                    </div>
                  )}
                </div>
                <button 
                  onClick={() => {
                    initializingRef.current = false;
                    initializeSession();
                  }}
                  className={`${connectionStatus === 'connected' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'} px-3 py-1 rounded text-xs font-semibold whitespace-nowrap`}
                >
                  {connectionStatus === 'connecting' ? 'Connecting...' : connectionStatus === 'connected' ? 'Reconnect' : 'Retry Connection'}
                </button>
              </div>
            </div>
          )}
          
          <div className="grid grid-cols-4 gap-3 mt-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
              <div className="text-2xl font-bold text-white">{messages.length - 1}</div>
              <div className="text-xs text-purple-200">Messages</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
              <div className="text-2xl font-bold text-white">{activeAgents.length}</div>
              <div className="text-xs text-purple-200">Active Agents</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full ${getConnectionStatusColor()} ${connectionStatus === 'connecting' ? 'animate-pulse' : ''}`}></div>
                <div className="text-xs text-purple-200">{getConnectionStatusText()}</div>
              </div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
              <div className="text-xs text-purple-200 truncate" title={sessionId}>
                Session: {sessionId ? sessionId.slice(0, 8) + '...' : 'N/A'}
              </div>
            </div>
          </div>
        </div>

        <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-4 min-h-0">
          
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
                    {msg.metadata && (
                      <div className="mt-3 pt-3 border-t border-gray-300">
                        <p className="text-xs text-gray-500 font-medium flex items-center gap-1">
                          <Zap className="w-3 h-3" />
                          {activeAgents.length} agents used
                        </p>
                        {msg.metadata.escalation_status && (
                          <p className="text-xs text-gray-600 mt-1">
                            Status: {msg.metadata.escalation_status}
                            {msg.metadata.escalation_status === 'pending' && ' 🔄'}
                            {msg.metadata.escalation_status === 'escalated' && ' ⚠️'}
                          </p>
                        )}
                        {msg.messageCount && (
                          <p className="text-xs text-gray-400 mt-1">
                            Message #{msg.messageCount}
                          </p>
                        )}
                      </div>
                    )}
                    <div className="mt-2 text-xs text-gray-400">
                      {msg.timestamp.toLocaleTimeString()}
                    </div>
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

            {messages.length <= 1 && !isProcessing && (
              <div className="px-4 pb-2">
                <div className="text-xs text-gray-500 mb-2 font-semibold">Quick actions:</div>
                <div className="flex flex-wrap gap-2">
                  {quickActions.map((action, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleQuickAction(action)}
                      className="text-xs bg-purple-100 hover:bg-purple-200 text-purple-700 px-3 py-2 rounded-lg transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                      disabled={isProcessing || !sessionId}
                    >
                      {action}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="p-4 bg-white border-t-2 border-gray-200">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder={sessionId ? "Type your message..." : "Connecting to server..."}
                  className="flex-1 bg-gray-100 border-2 border-gray-300 text-gray-900 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition-all disabled:opacity-50"
                  disabled={isProcessing || !sessionId}
                />
                <button
                  onClick={handleSend}
                  disabled={isProcessing || !input.trim() || !sessionId}
                  className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 disabled:from-gray-400 disabled:to-gray-500 text-white rounded-xl px-6 py-3 font-semibold transition-all shadow-lg hover:shadow-xl transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

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
                      <div className={`w-11 h-11 ${agent.color} rounded-xl flex items-center justify-center ${isActive && !isCompleted ? 'animate-pulse' : ''} shadow-md`}>
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

            <div className="p-4 bg-gray-50 border-t-2 border-gray-200">
              <div className="text-xs text-gray-600">
                <div className="flex justify-between mb-1">
                  <span>Total Agents:</span>
                  <span className="font-bold">{allAgents.length}</span>
                </div>
                <div className="flex justify-between">
                  <span>Currently Active:</span>
                  <span className="font-bold text-purple-600">{activeAgents.length}</span>
                </div>
              </div>
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