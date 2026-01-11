import React, { useState, useEffect } from "react";
import { base44 } from "@/api/base44Client";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import PostCard from "@/components/feed/PostCard";
import CreatePost from "@/components/feed/CreatePost";
import StoriesBar from "@/components/shared/StoriesBar";
import FriendSuggestions from "@/components/shared/FriendSuggestions";
import TrendingTopics from "@/components/shared/TrendingTopics";
import { Skeleton } from "@/components/ui/skeleton";
import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

export default function Home() {
  const [user, setUser] = useState(null);
  const queryClient = useQueryClient();

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    const userData = await base44.auth.me();
    setUser(userData);
  };

  const { data: posts = [], isLoading } = useQuery({
    queryKey: ['posts'],
    queryFn: () => base44.entities.Post.list('-created_date', 50),
  });

  const handlePostCreated = () => {
    queryClient.invalidateQueries({ queryKey: ['posts'] });
  };

  const handlePostDelete = async (postId) => {
    await base44.entities.Post.delete(postId);
    queryClient.invalidateQueries({ queryKey: ['posts'] });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 pb-24 md:pb-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Sidebar - Hidden on mobile */}
        <aside className="hidden lg:block lg:col-span-3 space-y-4 sticky top-24 h-fit">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-4">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-600 to-cyan-500 flex items-center justify-center">
                <span className="text-xl font-bold text-white">Y</span>
              </div>
              <div>
                <h2 className="font-bold text-lg text-slate-800">YourLife</h2>
                <p className="text-sm text-slate-500">Conecte-se ao mundo</p>
              </div>
            </div>
            <p className="text-sm text-slate-600">
              Compartilhe momentos, conecte-se com amigos e descubra novas experiências.
            </p>
          </div>
          <TrendingTopics />
        </aside>

        {/* Main Feed */}
        <main className="lg:col-span-6 space-y-4">
          <StoriesBar user={user} />
          <CreatePost user={user} onPostCreated={handlePostCreated} />
          
          {isLoading ? (
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-2xl p-4 space-y-4">
                  <div className="flex items-center gap-3">
                    <Skeleton className="w-12 h-12 rounded-full" />
                    <div className="space-y-2">
                      <Skeleton className="w-32 h-4" />
                      <Skeleton className="w-24 h-3" />
                    </div>
                  </div>
                  <Skeleton className="w-full h-20" />
                  <Skeleton className="w-full h-48 rounded-xl" />
                </div>
              ))}
            </div>
          ) : (
            <motion.div 
              className="space-y-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {posts.map((post) => (
                <PostCard 
                  key={post.id} 
                  post={post} 
                  currentUser={user}
                  onUpdate={handlePostCreated}
                  onDelete={handlePostDelete}
                />
              ))}
              
              {posts.length === 0 && (
                <div className="bg-white rounded-2xl p-12 text-center">
                  <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-violet-100 to-cyan-100 flex items-center justify-center">
                    <span className="text-4xl">📝</span>
                  </div>
                  <h3 className="text-xl font-semibold text-slate-800 mb-2">
                    Nenhum post ainda
                  </h3>
                  <p className="text-slate-500">
                    Seja o primeiro a compartilhar algo!
                  </p>
                </div>
              )}
            </motion.div>
          )}
        </main>

        {/* Right Sidebar */}
        <aside className="hidden lg:block lg:col-span-3 space-y-4 sticky top-24 h-fit">
          <FriendSuggestions />
          
          <div className="bg-gradient-to-br from-violet-600 via-cyan-500 to-rose-500 rounded-2xl p-4 text-white relative overflow-hidden">
            <div className="absolute -top-10 -right-10 w-32 h-32 bg-white/10 rounded-full blur-2xl" />
            <div className="relative">
              <div className="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center mb-3">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold mb-2">🎉 Conheça Lumenios AVA!</h3>
              <p className="text-sm opacity-90 mb-3">
                Seu avatar virtual assistente alimentado por Conscios AI está pronto para te ajudar!
              </p>
              <button className="w-full py-2 bg-white/20 rounded-xl text-sm font-medium hover:bg-white/30 transition-colors backdrop-blur-sm">
                Conhecer Lumenios
              </button>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}