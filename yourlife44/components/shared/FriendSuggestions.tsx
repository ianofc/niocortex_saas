import React from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { UserPlus, X } from "lucide-react";
import { motion } from "framer-motion";

const mockSuggestions = [
  { 
    id: 1, 
    name: "Lucas Oliveira", 
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150",
    mutualFriends: 12
  },
  { 
    id: 2, 
    name: "Juliana Costa", 
    avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150",
    mutualFriends: 8
  },
  { 
    id: 3, 
    name: "Rafael Santos", 
    avatar: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150",
    mutualFriends: 5
  },
];

export default function FriendSuggestions() {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-slate-800">Sugestões de amizade</h3>
        <Button variant="link" className="text-violet-600 p-0 h-auto">
          Ver todas
        </Button>
      </div>

      <div className="space-y-3">
        {mockSuggestions.map((suggestion, index) => (
          <motion.div
            key={suggestion.id}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center gap-3"
          >
            <Avatar className="w-12 h-12">
              <AvatarImage src={suggestion.avatar} />
              <AvatarFallback>{suggestion.name.charAt(0)}</AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <h4 className="font-medium text-slate-800 truncate">{suggestion.name}</h4>
              <p className="text-xs text-slate-500">{suggestion.mutualFriends} amigos em comum</p>
            </div>
            <div className="flex gap-1">
              <Button size="sm" className="rounded-full bg-violet-600 hover:bg-violet-700">
                <UserPlus className="w-4 h-4" />
              </Button>
              <Button size="sm" variant="ghost" className="rounded-full">
                <X className="w-4 h-4" />
              </Button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}