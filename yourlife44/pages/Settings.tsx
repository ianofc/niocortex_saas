import React, { useState, useEffect } from "react";
import { base44 } from "@/api/base44Client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { 
  User, 
  MapPin, 
  Briefcase, 
  GraduationCap, 
  Heart,
  Link as LinkIcon,
  Calendar,
  Save,
  Loader2,
  ArrowLeft,
  Bell,
  Shield,
  Palette
} from "lucide-react";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";
import { motion } from "framer-motion";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function Settings() {
  const [user, setUser] = useState(null);
  const [formData, setFormData] = useState({});
  const [isSaving, setIsSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    const userData = await base44.auth.me();
    setUser(userData);
    setFormData({
      bio: userData?.bio || "",
      location: userData?.location || "",
      work: userData?.work || "",
      education: userData?.education || "",
      website: userData?.website || "",
      relationship_status: userData?.relationship_status || "",
      birth_date: userData?.birth_date || ""
    });
  };

  const handleSave = async () => {
    setIsSaving(true);
    await base44.auth.updateMe(formData);
    setIsSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  return (
    <div className="max-w-3xl mx-auto px-4 pb-24 md:pb-8">
      {/* Header */}
      <div className="flex items-center gap-4 py-6">
        <Link to={createPageUrl("Profile")}>
          <Button variant="ghost" size="icon" className="rounded-full">
            <ArrowLeft className="w-5 h-5" />
          </Button>
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Configurações</h1>
          <p className="text-slate-500">Gerencie seu perfil e preferências</p>
        </div>
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList className="bg-white rounded-full p-1 border border-slate-200 w-full grid grid-cols-3">
          <TabsTrigger value="profile" className="rounded-full gap-2">
            <User className="w-4 h-4" />
            <span className="hidden sm:inline">Perfil</span>
          </TabsTrigger>
          <TabsTrigger value="notifications" className="rounded-full gap-2">
            <Bell className="w-4 h-4" />
            <span className="hidden sm:inline">Notificações</span>
          </TabsTrigger>
          <TabsTrigger value="privacy" className="rounded-full gap-2">
            <Shield className="w-4 h-4" />
            <span className="hidden sm:inline">Privacidade</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="profile">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 space-y-6"
          >
            {/* Bio */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <User className="w-4 h-4 text-slate-400" />
                Sobre você
              </Label>
              <Textarea
                value={formData.bio}
                onChange={(e) => handleChange('bio', e.target.value)}
                placeholder="Conte um pouco sobre você..."
                className="min-h-[100px]"
              />
            </div>

            {/* Location */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-slate-400" />
                Localização
              </Label>
              <Input
                value={formData.location}
                onChange={(e) => handleChange('location', e.target.value)}
                placeholder="Ex: São Paulo, Brasil"
              />
            </div>

            {/* Work */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-slate-400" />
                Trabalho
              </Label>
              <Input
                value={formData.work}
                onChange={(e) => handleChange('work', e.target.value)}
                placeholder="Ex: Designer na Empresa XYZ"
              />
            </div>

            {/* Education */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <GraduationCap className="w-4 h-4 text-slate-400" />
                Educação
              </Label>
              <Input
                value={formData.education}
                onChange={(e) => handleChange('education', e.target.value)}
                placeholder="Ex: Universidade de São Paulo"
              />
            </div>

            {/* Website */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <LinkIcon className="w-4 h-4 text-slate-400" />
                Website
              </Label>
              <Input
                value={formData.website}
                onChange={(e) => handleChange('website', e.target.value)}
                placeholder="https://seusite.com"
              />
            </div>

            {/* Relationship Status */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <Heart className="w-4 h-4 text-slate-400" />
                Status de relacionamento
              </Label>
              <Select 
                value={formData.relationship_status} 
                onValueChange={(value) => handleChange('relationship_status', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione..." />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="single">Solteiro(a)</SelectItem>
                  <SelectItem value="in_relationship">Em um relacionamento</SelectItem>
                  <SelectItem value="married">Casado(a)</SelectItem>
                  <SelectItem value="complicated">É complicado</SelectItem>
                  <SelectItem value="prefer_not_say">Prefiro não dizer</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Birth Date */}
            <div className="space-y-2">
              <Label className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-slate-400" />
                Data de nascimento
              </Label>
              <Input
                type="date"
                value={formData.birth_date}
                onChange={(e) => handleChange('birth_date', e.target.value)}
              />
            </div>

            {/* Save Button */}
            <div className="pt-4 border-t border-slate-100">
              <Button
                onClick={handleSave}
                disabled={isSaving}
                className="w-full rounded-full bg-gradient-to-r from-violet-600 to-cyan-500 hover:opacity-90 gap-2"
              >
                {isSaving ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : saved ? (
                  <>
                    <Save className="w-4 h-4" />
                    Salvo!
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4" />
                    Salvar alterações
                  </>
                )}
              </Button>
            </div>
          </motion.div>
        </TabsContent>

        <TabsContent value="notifications">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6"
          >
            <h3 className="font-semibold text-slate-800 mb-4">Preferências de notificação</h3>
            
            <div className="space-y-4">
              {[
                { label: "Curtidas e comentários", description: "Receba notificações de interações em seus posts" },
                { label: "Solicitações de amizade", description: "Saiba quando alguém quer se conectar" },
                { label: "Novos eventos", description: "Eventos de grupos que você participa" },
                { label: "Mensagens", description: "Notificações de novas mensagens" },
              ].map((item, index) => (
                <div key={index} className="flex items-center justify-between py-3 border-b border-slate-100 last:border-0">
                  <div>
                    <p className="font-medium text-slate-800">{item.label}</p>
                    <p className="text-sm text-slate-500">{item.description}</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked className="sr-only peer" />
                    <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-violet-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-violet-600"></div>
                  </label>
                </div>
              ))}
            </div>
          </motion.div>
        </TabsContent>

        <TabsContent value="privacy">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6"
          >
            <h3 className="font-semibold text-slate-800 mb-4">Configurações de privacidade</h3>
            
            <div className="space-y-4">
              {[
                { label: "Perfil público", description: "Qualquer pessoa pode ver seu perfil" },
                { label: "Mostrar status online", description: "Seus amigos podem ver quando você está online" },
                { label: "Permitir marcações", description: "Amigos podem marcar você em posts e fotos" },
                { label: "Indexação em buscas", description: "Seu perfil aparece nas buscas do YourLife" },
              ].map((item, index) => (
                <div key={index} className="flex items-center justify-between py-3 border-b border-slate-100 last:border-0">
                  <div>
                    <p className="font-medium text-slate-800">{item.label}</p>
                    <p className="text-sm text-slate-500">{item.description}</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked className="sr-only peer" />
                    <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-violet-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-violet-600"></div>
                  </label>
                </div>
              ))}
            </div>
          </motion.div>
        </TabsContent>
      </Tabs>
    </div>
  );
}