import React from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Plus } from "lucide-react";
import { motion } from "framer-motion";

const mockStories = [
  { id: 1, name: "Ana Silva", avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150", hasStory: true },
  { id: 2, name: "João Costa", avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150", hasStory: true },
  { id: 3, name: "Maria Santos", avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150", hasStory: true },
  { id: 4, name: "Pedro Lima", avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150", hasStory: true },
  { id: 5, name: "Carla Mendes", avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150", hasStory: true },
];

export default function StoriesBar({ user }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-4">
      <div className="flex gap-4 overflow-x-auto pb-2 scrollbar-hide">
        {/* Create Story */}
        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="flex flex-col items-center gap-2 cursor-pointer flex-shrink-0"
        >
          <div className="relative">
            <Avatar className="w-16 h-16 border-2 border-slate-200">
              <AvatarImage src={user?.avatar} />
              <AvatarFallback className="bg-gradient-to-br from-violet-500 to-cyan-500 text-white text-xl">
                {user?.full_name?.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-violet-600 rounded-full flex items-center justify-center border-2 border-white">
              <Plus className="w-4 h-4 text-white" />
            </div>
          </div>
          <span className="text-xs font-medium text-slate-700">Criar story</span>
        </motion.div>

        {/* Stories */}
        {mockStories.map((story, index) => (
          <motion.div 
            key={story.id}
            whileHover={{ scale: 1.05 }}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex flex-col items-center gap-2 cursor-pointer flex-shrink-0"
          >
            <div className={`p-0.5 rounded-full ${story.hasStory ? "bg-gradient-to-tr from-violet-600 via-cyan-500 to-rose-500" : ""}`}>
              <Avatar className="w-16 h-16 border-2 border-white">
                <AvatarImage src={story.avatar} />
                <AvatarFallback>{story.name.charAt(0)}</AvatarFallback>
              </Avatar>
            </div>
            <span className="text-xs font-medium text-slate-700 truncate w-16 text-center">
              {story.name.split(' ')[0]}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}