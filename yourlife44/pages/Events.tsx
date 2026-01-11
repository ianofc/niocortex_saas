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
  Calendar as CalendarIcon, 
  MapPin, 
  Users,
  Clock,
  Star,
  Check,
  Loader2,
  Video
} from "lucide-react";
import { motion } from "framer-motion";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

const mockEvents = [
  {
    id: "1",
    title: "Tech Conference 2024",
    description: "A maior conferência de tecnologia do ano",
    cover_image: "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=600",
    date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
    location: "Centro de Convenções SP",
    is_online: false,
    category: "conferencia",
    organizer_name: "TechHub Brasil",
    attendees: ["user1", "user2", "user3"],
    interested: ["user4", "user5"]
  },
  {
    id: "2",
    title: "Workshop de Design",
    description: "Aprenda UI/UX com profissionais",
    cover_image: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=600",
    date: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
    location: "Online",
    is_online: true,
    category: "workshop",
    organizer_name: "Design Academy",
    attendees: ["user1"],
    interested: ["user2", "user3", "user4"]
  },
  {
    id: "3",
    title: "Show Acústico",
    description: "Uma noite especial de música ao vivo",
    cover_image: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600",
    date: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(),
    location: "Espaço Cultural Downtown",
    is_online: false,
    category: "show",
    organizer_name: "Music Live",
    attendees: ["user1", "user2", "user3", "user4", "user5"],
    interested: ["user6", "user7"]
  },
];

function EventCard({ event }) {
  const [status, setStatus] = useState(null); // null, 'going', 'interested'

  const eventDate = new Date(event.date);
  const isPast = eventDate < new Date();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden"
    >
      <div className="relative h-40 overflow-hidden">
        <img 
          src={event.cover_image}
          alt={event.title}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        
        {/* Date Badge */}
        <div className="absolute top-3 left-3 bg-white rounded-xl p-2 text-center min-w-[50px] shadow-lg">
          <span className="block text-xs font-medium text-violet-600 uppercase">
            {format(eventDate, 'MMM', { locale: ptBR })}
          </span>
          <span className="block text-xl font-bold text-slate-800">
            {format(eventDate, 'd')}
          </span>
        </div>

        {event.is_online && (
          <div className="absolute top-3 right-3 bg-cyan-500 text-white rounded-full px-3 py-1 text-xs font-medium flex items-center gap-1">
            <Video className="w-3 h-3" />
            Online
          </div>
        )}
      </div>

      <div className="p-4">
        <h3 className="font-bold text-lg text-slate-800 mb-1">{event.title}</h3>
        
        <div className="flex items-center gap-1.5 text-slate-500 text-sm mb-2">
          <Clock className="w-4 h-4" />
          <span>{format(eventDate, "EEEE, d 'de' MMMM 'às' HH:mm", { locale: ptBR })}</span>
        </div>

        <div className="flex items-center gap-1.5 text-slate-500 text-sm mb-3">
          <MapPin className="w-4 h-4" />
          <span>{event.location}</span>
        </div>

        <p className="text-slate-600 text-sm mb-4 line-clamp-2">{event.description}</p>

        <div className="flex items-center justify-between pt-3 border-t border-slate-100">
          <div className="flex items-center gap-1.5 text-slate-500 text-sm">
            <Users className="w-4 h-4" />
            <span>{(event.attendees?.length || 0)} confirmados</span>
          </div>

          {!isPast && (
            <div className="flex gap-2">
              <Button
                size="sm"
                variant={status === 'interested' ? "secondary" : "outline"}
                onClick={() => setStatus(status === 'interested' ? null : 'interested')}
                className="rounded-full"
              >
                <Star className={`w-4 h-4 mr-1 ${status === 'interested' ? 'fill-current' : ''}`} />
                Interesse
              </Button>
              <Button
                size="sm"
                onClick={() => setStatus(status === 'going' ? null : 'going')}
                className={`rounded-full ${
                  status === 'going' 
                    ? 'bg-green-500 hover:bg-green-600' 
                    : 'bg-violet-600 hover:bg-violet-700'
                }`}
              >
                {status === 'going' ? (
                  <>
                    <Check className="w-4 h-4 mr-1" />
                    Vou
                  </>
                ) : (
                  "Participar"
                )}
              </Button>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}

export default function Events() {
  const [user, setUser] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newEvent, setNewEvent] = useState({
    title: "",
    description: "",
    date: "",
    location: "",
    is_online: false,
    category: "outro"
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

  const { data: events = [], isLoading } = useQuery({
    queryKey: ['events'],
    queryFn: () => base44.entities.Event.list('-date', 50),
  });

  const allEvents = [...mockEvents, ...events];

  const filteredEvents = allEvents.filter(event =>
    event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    event.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const upcomingEvents = filteredEvents.filter(e => new Date(e.date) > new Date());
  
  const handleCreateEvent = async () => {
    if (!newEvent.title.trim() || !newEvent.date) return;
    
    setIsCreating(true);
    await base44.entities.Event.create({
      ...newEvent,
      organizer_email: user?.email,
      organizer_name: user?.full_name,
      attendees: [user?.email],
      interested: [],
      cover_image: "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=600"
    });
    
    setNewEvent({ title: "", description: "", date: "", location: "", is_online: false, category: "outro" });
    setCreateDialogOpen(false);
    setIsCreating(false);
    queryClient.invalidateQueries({ queryKey: ['events'] });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 pb-24 md:pb-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Eventos</h1>
          <p className="text-slate-500">Descubra o que está acontecendo</p>
        </div>
        
        <div className="flex gap-3">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <Input
              placeholder="Buscar eventos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 rounded-full border-slate-200"
            />
          </div>
          
          <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button className="rounded-full bg-gradient-to-r from-violet-600 to-cyan-500 hover:opacity-90 gap-2">
                <Plus className="w-5 h-5" />
                <span className="hidden sm:inline">Criar evento</span>
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <DialogHeader>
                <DialogTitle>Criar novo evento</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 mt-4">
                <div>
                  <label className="text-sm font-medium text-slate-700">Título</label>
                  <Input
                    placeholder="Ex: Workshop de Marketing"
                    value={newEvent.title}
                    onChange={(e) => setNewEvent({...newEvent, title: e.target.value})}
                    className="mt-1"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700">Descrição</label>
                  <Textarea
                    placeholder="Sobre o que é o evento?"
                    value={newEvent.description}
                    onChange={(e) => setNewEvent({...newEvent, description: e.target.value})}
                    className="mt-1"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700">Data e hora</label>
                  <Input
                    type="datetime-local"
                    value={newEvent.date}
                    onChange={(e) => setNewEvent({...newEvent, date: e.target.value})}
                    className="mt-1"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700">Local</label>
                  <Input
                    placeholder="Endereço ou link"
                    value={newEvent.location}
                    onChange={(e) => setNewEvent({...newEvent, location: e.target.value})}
                    className="mt-1"
                  />
                </div>
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="is_online"
                    checked={newEvent.is_online}
                    onChange={(e) => setNewEvent({...newEvent, is_online: e.target.checked})}
                    className="rounded border-slate-300"
                  />
                  <label htmlFor="is_online" className="text-sm text-slate-700">Evento online</label>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700">Categoria</label>
                  <Select 
                    value={newEvent.category} 
                    onValueChange={(value) => setNewEvent({...newEvent, category: value})}
                  >
                    <SelectTrigger className="mt-1">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="festa">Festa</SelectItem>
                      <SelectItem value="conferencia">Conferência</SelectItem>
                      <SelectItem value="workshop">Workshop</SelectItem>
                      <SelectItem value="meetup">Meetup</SelectItem>
                      <SelectItem value="show">Show</SelectItem>
                      <SelectItem value="esporte">Esporte</SelectItem>
                      <SelectItem value="outro">Outro</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button 
                  onClick={handleCreateEvent}
                  disabled={!newEvent.title.trim() || !newEvent.date || isCreating}
                  className="w-full rounded-full bg-violet-600 hover:bg-violet-700"
                >
                  {isCreating ? <Loader2 className="w-4 h-4 animate-spin" /> : "Criar evento"}
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="upcoming" className="space-y-6">
        <TabsList className="bg-white rounded-full p-1 border border-slate-200">
          <TabsTrigger value="upcoming" className="rounded-full px-6">Próximos</TabsTrigger>
          <TabsTrigger value="my-events" className="rounded-full px-6">Meus eventos</TabsTrigger>
          <TabsTrigger value="past" className="rounded-full px-6">Passados</TabsTrigger>
        </TabsList>

        <TabsContent value="upcoming">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {upcomingEvents.map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
          
          {upcomingEvents.length === 0 && (
            <div className="text-center py-12">
              <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
                <CalendarIcon className="w-10 h-10 text-slate-400" />
              </div>
              <h3 className="text-lg font-semibold text-slate-800 mb-2">Nenhum evento encontrado</h3>
              <p className="text-slate-500">Crie um evento ou aguarde novos eventos!</p>
            </div>
          )}
        </TabsContent>

        <TabsContent value="my-events">
          <div className="text-center py-12">
            <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-violet-100 flex items-center justify-center">
              <CalendarIcon className="w-10 h-10 text-violet-500" />
            </div>
            <h3 className="text-lg font-semibold text-slate-800 mb-2">Você não confirmou presença em eventos</h3>
            <p className="text-slate-500 mb-4">Explore os eventos e participe!</p>
            <Button className="rounded-full bg-violet-600 hover:bg-violet-700">
              Explorar eventos
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="past">
          <div className="text-center py-12">
            <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
              <CalendarIcon className="w-10 h-10 text-slate-400" />
            </div>
            <h3 className="text-lg font-semibold text-slate-800 mb-2">Nenhum evento passado</h3>
            <p className="text-slate-500">Os eventos que você participou aparecerão aqui</p>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}