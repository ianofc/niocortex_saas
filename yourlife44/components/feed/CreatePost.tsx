import React, { useState } from "react";
import { base44 } from "@/api/base44Client";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { 
  Image, 
  Video, 
  Smile, 
  MapPin, 
  X,
  Globe,
  Users,
  Lock,
  Loader2
} from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { motion, AnimatePresence } from "framer-motion";

export default function CreatePost({ user, onPostCreated }) {
  const [content, setContent] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [visibility, setVisibility] = useState("public");
  const [isExpanded, setIsExpanded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setUploading(true);
    const { file_url } = await base44.integrations.Core.UploadFile({ file });
    setImageUrl(file_url);
    setUploading(false);
  };

  const handleSubmit = async () => {
    if (!content.trim()) return;
    
    setIsLoading(true);
    await base44.entities.Post.create({
      content,
      image_url: imageUrl,
      author_name: user?.full_name,
      author_email: user?.email,
      author_avatar: user?.avatar,
      likes: [],
      visibility
    });
    
    setContent("");
    setImageUrl("");
    setIsExpanded(false);
    setIsLoading(false);
    onPostCreated?.();
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-4">
      <div className="flex gap-3">
        <Avatar className="w-12 h-12 border-2 border-violet-100">
          <AvatarImage src={user?.avatar} />
          <AvatarFallback className="bg-gradient-to-br from-violet-500 to-cyan-500 text-white">
            {user?.full_name?.charAt(0)}
          </AvatarFallback>
        </Avatar>
        
        <div className="flex-1">
          <div
            onClick={() => setIsExpanded(true)}
            className={`bg-slate-50 rounded-2xl transition-all ${isExpanded ? "p-0" : "px-4 py-3 cursor-pointer hover:bg-slate-100"}`}
          >
            {isExpanded ? (
              <Textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder={`No que você está pensando, ${user?.full_name?.split(' ')[0]}?`}
                className="min-h-[100px] border-0 bg-slate-50 focus-visible:ring-0 resize-none text-lg"
                autoFocus
              />
            ) : (
              <span className="text-slate-500">
                No que você está pensando, {user?.full_name?.split(' ')[0]}?
              </span>
            )}
          </div>

          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
              >
                {/* Image Preview */}
                {imageUrl && (
                  <div className="relative mt-3 rounded-xl overflow-hidden">
                    <img src={imageUrl} alt="Preview" className="w-full max-h-64 object-cover" />
                    <Button
                      variant="secondary"
                      size="icon"
                      className="absolute top-2 right-2 rounded-full"
                      onClick={() => setImageUrl("")}
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                )}

                {/* Actions Bar */}
                <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between">
                  <div className="flex items-center gap-1">
                    <label className="p-2 rounded-full hover:bg-slate-100 cursor-pointer transition-colors">
                      <input 
                        type="file" 
                        accept="image/*" 
                        className="hidden" 
                        onChange={handleImageUpload}
                      />
                      {uploading ? (
                        <Loader2 className="w-5 h-5 text-green-500 animate-spin" />
                      ) : (
                        <Image className="w-5 h-5 text-green-500" />
                      )}
                    </label>
                    <button className="p-2 rounded-full hover:bg-slate-100 transition-colors">
                      <Video className="w-5 h-5 text-rose-500" />
                    </button>
                    <button className="p-2 rounded-full hover:bg-slate-100 transition-colors">
                      <Smile className="w-5 h-5 text-amber-500" />
                    </button>
                    <button className="p-2 rounded-full hover:bg-slate-100 transition-colors">
                      <MapPin className="w-5 h-5 text-cyan-500" />
                    </button>
                  </div>

                  <div className="flex items-center gap-2">
                    <Select value={visibility} onValueChange={setVisibility}>
                      <SelectTrigger className="w-32 h-9 rounded-full">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="public">
                          <div className="flex items-center gap-2">
                            <Globe className="w-4 h-4" />
                            Público
                          </div>
                        </SelectItem>
                        <SelectItem value="friends">
                          <div className="flex items-center gap-2">
                            <Users className="w-4 h-4" />
                            Amigos
                          </div>
                        </SelectItem>
                        <SelectItem value="private">
                          <div className="flex items-center gap-2">
                            <Lock className="w-4 h-4" />
                            Só eu
                          </div>
                        </SelectItem>
                      </SelectContent>
                    </Select>

                    <Button
                      onClick={handleSubmit}
                      disabled={!content.trim() || isLoading}
                      className="rounded-full bg-gradient-to-r from-violet-600 to-cyan-500 hover:opacity-90"
                    >
                      {isLoading ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        "Publicar"
                      )}
                    </Button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}