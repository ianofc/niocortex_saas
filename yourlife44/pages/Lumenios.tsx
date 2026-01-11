import React, { useState, useRef, useEffect } from "react";
import { base44 } from "@/api/base44Client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { 
  Sparkles, 
  Send, 
  Loader2, 
  Lightbulb,
  Wand2,
  MessageSquare,
  Trash2,
  RefreshCcw
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const suggestions = [
  "Me conte uma história inspiradora",
  "Dê-me dicas de produtividade",
  "Qual é a tendência do momento?",
  "Me ajude a escrever um post",
  "Sugira atividades para o fim de semana",
  "Crie uma legenda criativa para foto"
];

export default function Lumenios() {
  const [user, setUser] = useState(null);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Olá! Sou Lumenios, seu avatar virtual assistente no YourLife. Sou alimentado pela IA Conscios e posso te ajudar com ideias, criatividade, dicas e muito mais. Como posso ajudar você hoje? ✨"
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadUser();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadUser = async () => {
    const userData = await base44.auth.me();
    setUser(userData);
  };

  const handleSend = async (text = input) => {
    if (!text.trim() || isLoading) return;

    const userMessage = { role: "user", content: text };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    const response = await base44.integrations.Core.InvokeLLM({
      prompt: `Você é Lumenios, um avatar virtual assistente (AVA) da rede social YourLife, alimentado pela IA Conscios. 
Você tem personalidade amigável, carismática e criativa. Use emojis moderadamente e responda de forma concisa e útil.
Você ajuda os usuários com dicas, ideias criativas, sugestões de conteúdo, e conversas interessantes.
O usuário se chama ${user?.full_name || 'amigo'}.

Mensagem do usuário: ${text}`,
    });

    setMessages(prev => [...prev, { role: "assistant", content: response }]);
    setIsLoading(false);
  };

  const handleSuggestionClick = (suggestion) => {
    handleSend(suggestion);
  };

  const clearChat = () => {
    setMessages([
      {
        role: "assistant",
        content: "Olá! Sou Lumenios, seu avatar virtual assistente no YourLife. Sou alimentado pela IA Conscios e posso te ajudar com ideias, criatividade, dicas e muito mais. Como posso ajudar você hoje? ✨"
      }
    ]);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 pb-24 md:pb-8 h-[calc(100vh-100px)] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between py-4">
        <div className="flex items-center gap-3">
          <div className="relative w-12 h-12">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-violet-600 via-cyan-500 to-rose-500 flex items-center justify-center shadow-lg shadow-violet-500/30 animate-pulse">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Lumenios AVA</h1>
            <p className="text-sm text-slate-500">Avatar Virtual Assistente • Powered by Conscios AI</p>
          </div>
        </div>
        
        <Button
          variant="outline"
          size="sm"
          onClick={clearChat}
          className="rounded-full gap-2"
        >
          <RefreshCcw className="w-4 h-4" />
          Nova conversa
        </Button>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto space-y-4 py-4">
        <AnimatePresence>
          {messages.map((message, index) => (
          <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
          {message.role === 'assistant' ? (
            <div className="relative w-10 h-10 flex-shrink-0">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 via-cyan-500 to-rose-500 flex items-center justify-center shadow-lg">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
            </div>
          ) : (
                <Avatar className="w-10 h-10 flex-shrink-0">
                  <AvatarImage src={user?.avatar} />
                  <AvatarFallback className="bg-gradient-to-br from-violet-500 to-cyan-500 text-white">
                    {user?.full_name?.charAt(0)}
                  </AvatarFallback>
                </Avatar>
              )}
              
              <div className={`max-w-[80%] ${message.role === 'user' ? 'text-right' : ''}`}>
                <div className={`inline-block p-4 rounded-2xl ${
                  message.role === 'user' 
                    ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white rounded-tr-none' 
                    : 'bg-white border border-slate-200 text-slate-700 rounded-tl-none shadow-sm'
                }`}>
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-3"
          >
            <div className="relative w-10 h-10">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 via-cyan-500 to-rose-500 flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white animate-pulse" />
              </div>
              <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white animate-pulse" />
            </div>
            <div className="bg-white border border-slate-200 p-4 rounded-2xl rounded-tl-none shadow-sm">
              <div className="flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-violet-600" />
                <span className="text-slate-500">Lumenios está processando com Conscios AI...</span>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions */}
      {messages.length <= 1 && (
        <div className="py-4">
          <p className="text-sm text-slate-500 mb-3 flex items-center gap-2">
            <Lightbulb className="w-4 h-4" />
            Sugestões
          </p>
          <div className="flex flex-wrap gap-2">
            {suggestions.map((suggestion, index) => (
              <motion.button
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                onClick={() => handleSuggestionClick(suggestion)}
                className="px-4 py-2 bg-white border border-slate-200 rounded-full text-sm text-slate-700 hover:bg-slate-50 hover:border-violet-300 transition-all"
              >
                {suggestion}
              </motion.button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="sticky bottom-0 bg-gradient-to-t from-slate-50 via-slate-50 to-transparent pt-4">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Digite sua mensagem..."
              className="w-full pr-12 py-6 rounded-full border-slate-200 focus:border-violet-400 focus:ring-violet-400"
              disabled={isLoading}
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
              <Button
                size="icon"
                className="rounded-full w-9 h-9 bg-gradient-to-r from-violet-600 to-cyan-500 hover:opacity-90"
                onClick={() => handleSend()}
                disabled={!input.trim() || isLoading}
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
        
        <p className="text-center text-xs text-slate-400 mt-2">
          Lumenios AVA é alimentado por Conscios AI. Pode cometer erros. Verifique informações importantes.
        </p>
      </div>
    </div>
  );
}