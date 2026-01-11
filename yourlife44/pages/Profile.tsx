import React, { useState, useEffect } from "react";
import { base44 } from "@/api/base44Client";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import PostCard from "@/components/feed/PostCard";
import { 
  Camera, 
  MapPin, 
  Briefcase, 
  GraduationCap, 
  Heart,
  Calendar,
  Link as LinkIcon,
  Settings,
  Grid3X3,
  Bookmark,
  Users,
  Film,
  Image as ImageIcon,
  MoreHorizontal,
  Loader2
} from "lucide-react";
import { motion } from "framer-motion";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

export default function Profile() {
  const [user, setUser] = useState(null);
  const [uploading, setUploading] = useState(false);
  const queryClient = useQueryClient();

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    const userData = await base44.auth.me();
    setUser(userData);
  };

  const { data: posts = [], isLoading: postsLoading } = useQuery({
    queryKey: ['user-posts', user?.email],
    queryFn: () => base44.entities.Post.filter({ author_email: user?.email }, '-created_date'),
    enabled: !!user?.email
  });

  const { data: photos = [] } = useQuery({
    queryKey: ['user-photos', user?.email],
    queryFn: () => base44.entities.Photo.filter({ owner_email: user?.email }, '-created_date'),
    enabled: !!user?.email
  });

  const { data: friendships = [] } = useQuery({
    queryKey: ['user-friends', user?.email],
    queryFn: () => base44.entities.Friendship.filter({ user_email: user?.email, status: 'accepted' }),
    enabled: !!user?.email
  });

  const handleCoverUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setUploading(true);
    const { file_url } = await base44.integrations.Core.UploadFile({ file });
    await base44.auth.updateMe({ cover_photo: file_url });
    setUser({ ...user, cover_photo: file_url });
    setUploading(false);
  };

  const handleAvatarUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setUploading(true);
    const { file_url } = await base44.integrations.Core.UploadFile({ file });
    await base44.auth.updateMe({ avatar: file_url });
    setUser({ ...user, avatar: file_url });
    setUploading(false);
  };

  const relationshipLabels = {
    single: "Solteiro(a)",
    in_relationship: "Em um relacionamento",
    married: "Casado(a)",
    complicated: "É complicado",
    prefer_not_say: "Prefiro não dizer"
  };

  return (
    <div className="max-w-5xl mx-auto pb-24 md:pb-8">
      {/* Cover Photo */}
      <div className="relative h-48 md:h-72 bg-gradient-to-r from-violet-600 via-cyan-500 to-rose-500 md:rounded-b-3xl overflow-hidden">
        {user?.cover_photo && (
          <img 
            src={user.cover_photo} 
            alt="Cover" 
            className="w-full h-full object-cover"
          />
        )}
        <div className="absolute inset-0 bg-black/20" />
        
        <label className="absolute bottom-4 right-4 p-2 bg-white/90 rounded-full cursor-pointer hover:bg-white transition-colors shadow-lg">
          <input 
            type="file" 
            accept="image/*" 
            className="hidden" 
            onChange={handleCoverUpload}
          />
          {uploading ? (
            <Loader2 className="w-5 h-5 animate-spin text-slate-600" />
          ) : (
            <Camera className="w-5 h-5 text-slate-600" />
          )}
        </label>
      </div>

      {/* Profile Info */}
      <div className="px-4 md:px-8 -mt-16 md:-mt-20 relative z-10">
        <div className="flex flex-col md:flex-row md:items-end gap-4">
          {/* Avatar */}
          <div className="relative">
            <Avatar className="w-32 h-32 md:w-40 md:h-40 border-4 border-white shadow-xl">
              <AvatarImage src={user?.avatar} />
              <AvatarFallback className="bg-gradient-to-br from-violet-500 to-cyan-500 text-white text-4xl">
                {user?.full_name?.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <label className="absolute bottom-2 right-2 p-2 bg-slate-100 rounded-full cursor-pointer hover:bg-slate-200 transition-colors shadow">
              <input 
                type="file" 
                accept="image/*" 
                className="hidden" 
                onChange={handleAvatarUpload}
              />
              <Camera className="w-4 h-4 text-slate-600" />
            </label>
          </div>

          {/* Name & Actions */}
          <div className="flex-1 md:pb-2">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h1 className="text-2xl md:text-3xl font-bold text-slate-800">
                  {user?.full_name}
                </h1>
                <p className="text-slate-500">
                  {friendships.length} amigos • {posts.length} publicações
                </p>
              </div>
              <div className="flex gap-2">
                <Link to={createPageUrl("Settings")}>
                  <Button variant="outline" className="rounded-full gap-2">
                    <Settings className="w-4 h-4" />
                    Editar perfil
                  </Button>
                </Link>
                <Button variant="ghost" size="icon" className="rounded-full">
                  <MoreHorizontal className="w-5 h-5" />
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Bio */}
        {user?.bio && (
          <p className="mt-4 text-slate-700 max-w-2xl">{user.bio}</p>
        )}

        {/* Info Cards */}
        <div className="flex flex-wrap gap-4 mt-4 text-sm text-slate-600">
          {user?.location && (
            <div className="flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-slate-400" />
              <span>{user.location}</span>
            </div>
          )}
          {user?.work && (
            <div className="flex items-center gap-1.5">
              <Briefcase className="w-4 h-4 text-slate-400" />
              <span>{user.work}</span>
            </div>
          )}
          {user?.education && (
            <div className="flex items-center gap-1.5">
              <GraduationCap className="w-4 h-4 text-slate-400" />
              <span>{user.education}</span>
            </div>
          )}
          {user?.relationship_status && (
            <div className="flex items-center gap-1.5">
              <Heart className="w-4 h-4 text-slate-400" />
              <span>{relationshipLabels[user.relationship_status]}</span>
            </div>
          )}
          {user?.website && (
            <div className="flex items-center gap-1.5">
              <LinkIcon className="w-4 h-4 text-slate-400" />
              <a href={user.website} target="_blank" rel="noopener noreferrer" className="text-violet-600 hover:underline">
                {user.website.replace(/^https?:\/\//, '')}
              </a>
            </div>
          )}
          <div className="flex items-center gap-1.5">
            <Calendar className="w-4 h-4 text-slate-400" />
            <span>Entrou em {user?.created_date ? format(new Date(user.created_date), "MMMM 'de' yyyy", { locale: ptBR }) : 'recentemente'}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="px-4 md:px-8 mt-6">
        <Tabs defaultValue="posts" className="space-y-6">
          <TabsList className="bg-white rounded-full p-1 border border-slate-200 w-full md:w-auto inline-flex">
            <TabsTrigger value="posts" className="rounded-full px-4 md:px-6 gap-2">
              <Grid3X3 className="w-4 h-4" />
              <span className="hidden md:inline">Publicações</span>
            </TabsTrigger>
            <TabsTrigger value="photos" className="rounded-full px-4 md:px-6 gap-2">
              <ImageIcon className="w-4 h-4" />
              <span className="hidden md:inline">Fotos</span>
            </TabsTrigger>
            <TabsTrigger value="reels" className="rounded-full px-4 md:px-6 gap-2">
              <Film className="w-4 h-4" />
              <span className="hidden md:inline">Reels</span>
            </TabsTrigger>
            <TabsTrigger value="friends" className="rounded-full px-4 md:px-6 gap-2">
              <Users className="w-4 h-4" />
              <span className="hidden md:inline">Amigos</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="posts" className="space-y-4">
            {posts.length > 0 ? (
              posts.map(post => (
                <PostCard 
                  key={post.id} 
                  post={post} 
                  currentUser={user}
                  onUpdate={() => queryClient.invalidateQueries({ queryKey: ['user-posts'] })}
                />
              ))
            ) : (
              <div className="text-center py-12 bg-white rounded-2xl">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
                  <Grid3X3 className="w-10 h-10 text-slate-400" />
                </div>
                <h3 className="text-lg font-semibold text-slate-800 mb-2">Nenhuma publicação</h3>
                <p className="text-slate-500">Suas publicações aparecerão aqui</p>
              </div>
            )}
          </TabsContent>

          <TabsContent value="photos">
            {photos.length > 0 ? (
              <div className="grid grid-cols-3 gap-1 md:gap-2">
                {photos.map((photo, index) => (
                  <motion.div
                    key={photo.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: index * 0.1 }}
                    className="aspect-square rounded-lg overflow-hidden cursor-pointer hover:opacity-90 transition-opacity"
                  >
                    <img 
                      src={photo.url} 
                      alt={photo.caption || 'Foto'}
                      className="w-full h-full object-cover"
                    />
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 bg-white rounded-2xl">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
                  <ImageIcon className="w-10 h-10 text-slate-400" />
                </div>
                <h3 className="text-lg font-semibold text-slate-800 mb-2">Nenhuma foto</h3>
                <p className="text-slate-500">Suas fotos aparecerão aqui</p>
              </div>
            )}
          </TabsContent>

          <TabsContent value="reels">
            <div className="text-center py-12 bg-white rounded-2xl">
              <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
                <Film className="w-10 h-10 text-slate-400" />
              </div>
              <h3 className="text-lg font-semibold text-slate-800 mb-2">Nenhum reel</h3>
              <p className="text-slate-500">Seus reels aparecerão aqui</p>
            </div>
          </TabsContent>

          <TabsContent value="friends">
            {friendships.length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {friendships.map((friendship) => (
                  <motion.div
                    key={friendship.id}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="bg-white rounded-2xl p-4 text-center shadow-sm border border-slate-100"
                  >
                    <Avatar className="w-20 h-20 mx-auto mb-3">
                      <AvatarImage src={friendship.friend_avatar} />
                      <AvatarFallback className="bg-gradient-to-br from-violet-500 to-cyan-500 text-white text-xl">
                        {friendship.friend_name?.charAt(0)}
                      </AvatarFallback>
                    </Avatar>
                    <h4 className="font-semibold text-slate-800">{friendship.friend_name}</h4>
                    <Button variant="outline" size="sm" className="mt-2 rounded-full w-full">
                      Ver perfil
                    </Button>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 bg-white rounded-2xl">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
                  <Users className="w-10 h-10 text-slate-400" />
                </div>
                <h3 className="text-lg font-semibold text-slate-800 mb-2">Nenhum amigo ainda</h3>
                <p className="text-slate-500 mb-4">Encontre amigos para se conectar!</p>
                <Link to={createPageUrl("Home")}>
                  <Button className="rounded-full bg-violet-600 hover:bg-violet-700">
                    Encontrar amigos
                  </Button>
                </Link>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}