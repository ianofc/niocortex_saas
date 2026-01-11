import React, { useState, useEffect } from "react";
import { base44 } from "@/api/base44Client";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { 
  Plus, 
  Search, 
  Users, 
  Globe, 
  Lock, 
  TrendingUp,
  Loader2
} from "lucide-react";
import { motion } from "framer-motion";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const categoryImages = {
  tecnologia: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600",
  esportes: "https://images.unsplash.com/photo-1461896836934- voices-of-victory?w=600",
  musica: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600",
  arte: "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=600",
  games: "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600",
  educacao: "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=600",
  negocios: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600",
  outro: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600",
};

const mockGroups = [
  { 
    id: "1", 
    name: "Tech Enthusiasts", 
    description: "Discussões sobre tecnologia e inovação",
    cover_image: categoryImages.tecnologia,
    category: "tecnologia",
    privacy: "public",
    members_count: 12450,
    members: []
  },
  { 
    id: "2", 
    name: "Amantes da Música", 
    description: "Compartilhe suas descobertas musicais",
    cover_image: categoryImages.musica,
    category: "musica",
    privacy: "public",
    members_count: 8320,
    members: []
  },
  { 
    id: "3", 
    name: "Gamers BR", 
    description: "A comunidade gamer brasileira",
    cover_image: categoryImages.games,
    category: "games",
    privacy: "public",
    members_count: 25680,
    members: []
  },
];

function GroupCard({ group, onJoin }) {
  const [joined, setJoined] = useState(false);

  const handleJoin = () => {
    setJoined(!joined);
    onJoin?.(group);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden group cursor-pointer"
    >
      <div className="relative h-32 overflow-hidden">
        <img 
          src={group.cover_image || categoryImages[group.category] || categoryImages.outro}
          alt={group.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <div className="absolute bottom-3 left-3 right-3 flex items-end justify-between">
          <div>
            <h3 className="font-bold text-white text-lg">{group.name}</h3>
            <div className="flex items-center gap-2 text-white/80 text-sm">
              {group.privacy === "public" ? (
                <Globe className="w-3 h-3" />
              ) : (
                <Lock className="w-3 h-3" />
              )}
              <span>{group.privacy === "public" ? "Público" : "Privado"}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="p-4">
        <p className="text-slate-600 text-sm mb-3 line-clamp-2">{group.description}</p>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-slate-500 text-sm">
            <Users className="w-4 h-4" />
            <span>{(group.members_count || 0).toLocaleString()} membros</span>
          </div>
          
          <Button 
            size="sm"
            onClick={handleJoin}
            className={`rounded-full ${
              joined 
                ? "bg-slate-100 text-slate-700 hover:bg-slate-200" 
                : "bg-violet-600 hover:bg-violet-700"
            }`}
          >
            {joined ? "Participando" : "Participar"}
          </Button>
        </div>
      </div>
    </motion.div>
  );
}

export default function Groups() {
  const [user, setUser] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newGroup, setNewGroup] = useState({
    name: "",
    description: "",
    category: "outro",
    privacy: "public"
  });
  const [isCreating, setIsCreating] = useState(false);
  const queryClient = useQueryClient();

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    const userData = await base44.auth.me();
    setUser(userData);
  };

  const { data: groups = [], isLoading } = useQuery({
    queryKey: ['groups'],
    queryFn: () => base44.entities.Group.list('-created_date', 50),
  });

  const allGroups = [...mockGroups, ...groups];

  const filteredGroups = allGroups.filter(group =>
    group.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    group.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleCreateGroup = async () => {
    if (!newGroup.name.trim()) return;
    
    setIsCreating(true);
    await base44.entities.Group.create({
      ...newGroup,
      admin_email: user?.email,
      members: [user?.email],
      members_count: 1,
      cover_image: categoryImages[newGroup.category]
    });
    
    setNewGroup({ name: "", description: "", category: "outro", privacy: "public" });
    setCreateDialogOpen(false);
    setIsCreating(false);
    queryClient.invalidateQueries({ queryKey: ['groups'] });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 pb-24 md:pb-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Grupos</h1>
          <p className="text-slate-500">Encontre comunidades com seus interesses</p>
        </div>
        
        <div className="flex gap-3">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <Input
              placeholder="Buscar grupos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 rounded-full border-slate-200"
            />
          </div>
          
          <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button className="rounded-full bg-gradient-to-r from-violet-600 to-cyan-500 hover:opacity-90 gap-2">
                <Plus className="w-5 h-5" />
                <span className="hidden sm:inline">Criar grupo</span>
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <DialogHeader>
                <DialogTitle>Criar novo grupo</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 mt-4">
                <div>
                  <label className="text-sm font-medium text-slate-700">Nome do grupo</label>
                  <Input
                    placeholder="Ex: Amantes de Café"
                    value={newGroup.name}
                    onChange={(e) => setNewGroup({...newGroup, name: e.target.value})}
                    className="mt-1"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700">Descrição</label>
                  <Textarea
                    placeholder="Do que se trata o grupo?"
                    value={newGroup.description}
                    onChange={(e) => setNewGroup({...newGroup, description: e.target.value})}
                    className="mt-1"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-slate-700">Categoria</label>
                    <Select 
                      value={newGroup.category} 
                      onValueChange={(value) => setNewGroup({...newGroup, category: value})}
                    >
                      <SelectTrigger className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="tecnologia">Tecnologia</SelectItem>
                        <SelectItem value="esportes">Esportes</SelectItem>
                        <SelectItem value="musica">Música</SelectItem>
                        <SelectItem value="arte">Arte</SelectItem>
                        <SelectItem value="games">Games</SelectItem>
                        <SelectItem value="educacao">Educação</SelectItem>
                        <SelectItem value="negocios">Negócios</SelectItem>
                        <SelectItem value="outro">Outro</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-700">Privacidade</label>
                    <Select 
                      value={newGroup.privacy} 
                      onValueChange={(value) => setNewGroup({...newGroup, privacy: value})}
                    >
                      <SelectTrigger className="mt-1">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="public">Público</SelectItem>
                        <SelectItem value="private">Privado</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <Button 
                  onClick={handleCreateGroup}
                  disabled={!newGroup.name.trim() || isCreating}
                  className="w-full rounded-full bg-violet-600 hover:bg-violet-700"
                >
                  {isCreating ? <Loader2 className="w-4 h-4 animate-spin" /> : "Criar grupo"}
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="discover" className="space-y-6">
        <TabsList className="bg-white rounded-full p-1 border border-slate-200">
          <TabsTrigger value="discover" className="rounded-full px-6">Descobrir</TabsTrigger>
          <TabsTrigger value="my-groups" className="rounded-full px-6">Meus grupos</TabsTrigger>
        </TabsList>

        <TabsContent value="discover">
          {/* Trending */}
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-violet-600" />
              <h2 className="text-xl font-bold text-slate-800">Em alta</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredGroups.slice(0, 3).map((group, index) => (
                <GroupCard key={group.id} group={group} />
              ))}
            </div>
          </div>

          {/* All Groups */}
          <div>
            <h2 className="text-xl font-bold text-slate-800 mb-4">Todos os grupos</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredGroups.map((group, index) => (
                <GroupCard key={group.id} group={group} />
              ))}
            </div>
            
            {filteredGroups.length === 0 && (
              <div className="text-center py-12">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
                  <Users className="w-10 h-10 text-slate-400" />
                </div>
                <h3 className="text-lg font-semibold text-slate-800 mb-2">Nenhum grupo encontrado</h3>
                <p className="text-slate-500">Tente buscar por outro termo ou crie um novo grupo!</p>
              </div>
            )}
          </div>
        </TabsContent>

        <TabsContent value="my-groups">
          <div className="text-center py-12">
            <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-violet-100 flex items-center justify-center">
              <Users className="w-10 h-10 text-violet-500" />
            </div>
            <h3 className="text-lg font-semibold text-slate-800 mb-2">Você ainda não participa de grupos</h3>
            <p className="text-slate-500 mb-4">Encontre grupos interessantes e participe!</p>
            <Button className="rounded-full bg-violet-600 hover:bg-violet-700">
              Explorar grupos
            </Button>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}