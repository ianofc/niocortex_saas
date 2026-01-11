import React, { useState, useEffect } from "react";
import { base44 } from "@/api/base44Client";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  Search, 
  Edit, 
  MoreHorizontal, 
  Send,
  Image,
  Smile,
  Phone,
  Video,
  Info,
  ArrowLeft
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const mockConversations = [
  {
    id: "1",
    user: {
      name: "Ana Beatriz",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
      online: true
    },
    lastMessage: "Oi! Tudo bem com você?",
    time: "Agora",
    unread: 2
  },
  {
    id: "2",
    user: {
      name: "Carlos Eduardo",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150",
      online: false
    },
    lastMessage: "Vamos marcar aquele café!",
    time: "15min",
    unread: 0
  },
  {
    id: "3",
    user: {
      name: "Marina Costa",
      avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150",
      online: true
    },
    lastMessage: "Adorei sua última foto 📸",
    time: "1h",
    unread: 0
  },
  {
    id: "4",
    user: {
      name: "Pedro Lima",
      avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150",
      online: false
    },
    lastMessage: "Enviou uma foto",
    time: "3h",
    unread: 1
  },
];

const mockMessages = [
  { id: 1, sender: "them", text: "Oi! Tudo bem com você?", time: "10:30" },
  { id: 2, sender: "me", text: "Oi Ana! Tudo ótimo, e você?", time: "10:31" },
  { id: 3, sender: "them", text: "Também! Vi que você postou uma foto incrível ontem", time: "10:32" },
  { id: 4, sender: "me", text: "Haha obrigado! Foi naquela viagem que te falei", time: "10:33" },
  { id: 5, sender: "them", text: "Que lugar lindo! Preciso ir lá também 🌴", time: "10:34" },
];

export default function Messages() {
  const [user, setUser] = useState(null);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState(mockMessages);
  const [showMobileChat, setShowMobileChat] = useState(false);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    const userData = await base44.auth.me();
    setUser(userData);
  };

  const handleSend = () => {
    if (!message.trim()) return;
    
    setMessages([
      ...messages,
      {
        id: messages.length + 1,
        sender: "me",
        text: message,
        time: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
      }
    ]);
    setMessage("");
  };

  const handleSelectConversation = (conv) => {
    setSelectedConversation(conv);
    setShowMobileChat(true);
  };

  return (
    <div className="max-w-6xl mx-auto h-[calc(100vh-100px)] md:h-[calc(100vh-100px)] flex">
      {/* Conversations List */}
      <div className={`${showMobileChat ? 'hidden md:flex' : 'flex'} w-full md:w-96 flex-col bg-white md:rounded-l-2xl md:border-r border-slate-200`}>
        {/* Header */}
        <div className="p-4 border-b border-slate-100">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-slate-800">Mensagens</h1>
            <Button variant="ghost" size="icon" className="rounded-full">
              <Edit className="w-5 h-5" />
            </Button>
          </div>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <Input
              placeholder="Buscar conversa..."
              className="pl-10 rounded-full border-slate-200"
            />
          </div>
        </div>

        {/* Conversations */}
        <div className="flex-1 overflow-y-auto">
          {mockConversations.map((conv, index) => (
            <motion.div
              key={conv.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => handleSelectConversation(conv)}
              className={`flex items-center gap-3 p-4 cursor-pointer transition-colors ${
                selectedConversation?.id === conv.id 
                  ? 'bg-violet-50' 
                  : 'hover:bg-slate-50'
              }`}
            >
              <div className="relative">
                <Avatar className="w-14 h-14">
                  <AvatarImage src={conv.user.avatar} />
                  <AvatarFallback>{conv.user.name.charAt(0)}</AvatarFallback>
                </Avatar>
                {conv.user.online && (
                  <div className="absolute bottom-0 right-0 w-4 h-4 bg-green-500 rounded-full border-2 border-white" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-slate-800 truncate">{conv.user.name}</h3>
                  <span className="text-xs text-slate-500">{conv.time}</span>
                </div>
                <p className={`text-sm truncate ${conv.unread ? 'text-slate-800 font-medium' : 'text-slate-500'}`}>
                  {conv.lastMessage}
                </p>
              </div>
              {conv.unread > 0 && (
                <div className="w-5 h-5 bg-violet-600 rounded-full flex items-center justify-center">
                  <span className="text-xs text-white font-medium">{conv.unread}</span>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className={`${!showMobileChat ? 'hidden md:flex' : 'flex'} flex-1 flex-col bg-white md:rounded-r-2xl`}>
        {selectedConversation ? (
          <>
            {/* Chat Header */}
            <div className="p-4 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="md:hidden rounded-full"
                  onClick={() => setShowMobileChat(false)}
                >
                  <ArrowLeft className="w-5 h-5" />
                </Button>
                <Avatar className="w-10 h-10">
                  <AvatarImage src={selectedConversation.user.avatar} />
                  <AvatarFallback>{selectedConversation.user.name.charAt(0)}</AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="font-semibold text-slate-800">{selectedConversation.user.name}</h3>
                  <p className="text-xs text-green-500">
                    {selectedConversation.user.online ? 'Online' : 'Offline'}
                  </p>
                </div>
              </div>
              <div className="flex gap-1">
                <Button variant="ghost" size="icon" className="rounded-full">
                  <Phone className="w-5 h-5 text-slate-600" />
                </Button>
                <Button variant="ghost" size="icon" className="rounded-full">
                  <Video className="w-5 h-5 text-slate-600" />
                </Button>
                <Button variant="ghost" size="icon" className="rounded-full">
                  <Info className="w-5 h-5 text-slate-600" />
                </Button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((msg, index) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className={`flex ${msg.sender === 'me' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[70%] px-4 py-2 rounded-2xl ${
                    msg.sender === 'me' 
                      ? 'bg-gradient-to-r from-violet-600 to-cyan-500 text-white rounded-br-none' 
                      : 'bg-slate-100 text-slate-800 rounded-bl-none'
                  }`}>
                    <p>{msg.text}</p>
                    <p className={`text-xs mt-1 ${msg.sender === 'me' ? 'text-white/70' : 'text-slate-500'}`}>
                      {msg.time}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Input */}
            <div className="p-4 border-t border-slate-100">
              <div className="flex items-center gap-2">
                <Button variant="ghost" size="icon" className="rounded-full flex-shrink-0">
                  <Image className="w-5 h-5 text-slate-600" />
                </Button>
                <Button variant="ghost" size="icon" className="rounded-full flex-shrink-0">
                  <Smile className="w-5 h-5 text-slate-600" />
                </Button>
                <Input
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Digite sua mensagem..."
                  className="flex-1 rounded-full border-slate-200"
                />
                <Button 
                  onClick={handleSend}
                  disabled={!message.trim()}
                  size="icon" 
                  className="rounded-full bg-gradient-to-r from-violet-600 to-cyan-500 hover:opacity-90 flex-shrink-0"
                >
                  <Send className="w-5 h-5" />
                </Button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-violet-100 flex items-center justify-center">
                <Send className="w-10 h-10 text-violet-500" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Suas mensagens</h3>
              <p className="text-slate-500">Selecione uma conversa para começar</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}