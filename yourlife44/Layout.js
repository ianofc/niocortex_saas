import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { createPageUrl } from "./utils";
import { base44 } from "@/api/base44Client";
import { 
  Home, 
  Film, 
  Users, 
  Calendar, 
  Sparkles, 
  Bell, 
  MessageCircle, 
  Search,
  Menu,
  X,
  LogOut,
  User,
  Settings
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { motion, AnimatePresence } from "framer-motion";

export default function Layout({ children, currentPageName }) {
  const [user, setUser] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    const userData = await base44.auth.me();
    setUser(userData);
  };

  const handleLogout = () => {
    base44.auth.logout();
  };

  const navItems = [
    { name: "Home", icon: Home, page: "Home" },
    { name: "Reels", icon: Film, page: "Reels" },
    { name: "Grupos", icon: Users, page: "Groups" },
    { name: "Eventos", icon: Calendar, page: "Events" },
    { name: "Lumenios AVA", icon: Sparkles, page: "Lumenios" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-violet-50">
      <style>{`
        :root {
          --primary: #7c3aed;
          --primary-light: #a78bfa;
          --secondary: #0ea5e9;
          --accent: #f43f5e;
          --dark: #1e1b4b;
        }
        .glass-nav {
          background: rgba(255, 255, 255, 0.7);
          backdrop-filter: blur(20px);
          -webkit-backdrop-filter: blur(20px);
          border-bottom: 1px solid rgba(255, 255, 255, 0.3);
        }
        .nav-item-active {
          background: linear-gradient(135deg, #7c3aed 0%, #0ea5e9 100%);
          color: white !important;
        }
        .yourlife-gradient {
          background: linear-gradient(135deg, #7c3aed 0%, #0ea5e9 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
      `}</style>

      {/* Top Navigation - Glassbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 px-4 py-2 glass-nav">
        <div className="flex items-center justify-between mx-auto max-w-7xl">
          {/* Logo */}
          <Link to={createPageUrl("Home")} className="flex items-center gap-2">
            <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-cyan-500">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="hidden text-2xl font-bold yourlife-gradient sm:block">
              YourLife
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="items-center hidden gap-1 md:flex">
            {navItems.map((item) => (
              <Link
                key={item.page}
                to={createPageUrl(item.page)}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-full transition-all duration-300 font-medium ${
                  currentPageName === item.page
                    ? "nav-item-active shadow-lg shadow-violet-500/30"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.name}</span>
              </Link>
            ))}
          </div>

          {/* Right Section */}
          <div className="flex items-center gap-3">
            {/* Search */}
            <button 
              onClick={() => setSearchOpen(!searchOpen)}
              className="p-2.5 rounded-full hover:bg-slate-100 transition-colors"
            >
              <Search className="w-5 h-5 text-slate-600" />
            </button>

            {/* Notifications */}
            <button className="p-2.5 rounded-full hover:bg-slate-100 transition-colors relative">
              <Bell className="w-5 h-5 text-slate-600" />
              <span className="absolute w-2 h-2 rounded-full top-1 right-1 bg-rose-500" />
            </button>

            {/* Messages */}
            <Link 
              to={createPageUrl("Messages")}
              className="p-2.5 rounded-full hover:bg-slate-100 transition-colors"
            >
              <MessageCircle className="w-5 h-5 text-slate-600" />
            </Link>

            {/* Profile Dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="flex items-center gap-2 p-1 pr-3 transition-colors rounded-full hover:bg-slate-100">
                  <Avatar className="border-2 w-9 h-9 border-violet-200">
                    <AvatarImage src={user?.avatar} />
                    <AvatarFallback className="text-sm text-white bg-gradient-to-br from-violet-500 to-cyan-500">
                      {user?.full_name?.charAt(0) || "U"}
                    </AvatarFallback>
                  </Avatar>
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56 mt-2">
                <DropdownMenuItem asChild>
                  <Link to={createPageUrl("Profile")} className="flex items-center gap-2 cursor-pointer">
                    <User className="w-4 h-4" />
                    Meu Perfil
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link to={createPageUrl("Settings")} className="flex items-center gap-2 cursor-pointer">
                    <Settings className="w-4 h-4" />
                    Configurações
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="cursor-pointer text-rose-600">
                  <LogOut className="w-4 h-4 mr-2" />
                  Sair
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Mobile Menu Button */}
            <button 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-full md:hidden hover:bg-slate-100"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Search Bar Expanded */}
        <AnimatePresence>
          {searchOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="overflow-hidden"
            >
              <div className="max-w-xl py-3 mx-auto">
                <div className="relative">
                  <Search className="absolute w-5 h-5 -translate-y-1/2 left-4 top-1/2 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Buscar no YourLife..."
                    className="w-full py-3 pl-12 pr-4 border rounded-full bg-white/80 border-slate-200 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
                    autoFocus
                  />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed left-0 right-0 z-40 top-16 glass-nav md:hidden"
          >
            <div className="p-4 space-y-2">
              {navItems.map((item) => (
                <Link
                  key={item.page}
                  to={createPageUrl(item.page)}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                    currentPageName === item.page
                      ? "nav-item-active"
                      : "text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <main className="min-h-screen pt-20">
        {children}
      </main>

      {/* Mobile Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 px-2 py-2 border-t md:hidden glass-nav border-slate-200/50">
        <div className="flex items-center justify-around">
          {navItems.map((item) => (
            <Link
              key={item.page}
              to={createPageUrl(item.page)}
              className={`flex flex-col items-center gap-1 px-3 py-2 rounded-xl transition-all ${
                currentPageName === item.page
                  ? "text-violet-600"
                  : "text-slate-500"
              }`}
            >
              <item.icon className={`w-6 h-6 ${currentPageName === item.page ? "scale-110" : ""}`} />
              <span className="text-xs font-medium">{item.name}</span>
            </Link>
          ))}
        </div>
      </nav>
    </div>
  );
}