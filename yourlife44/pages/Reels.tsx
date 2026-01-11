import React, { useState, useEffect, useRef } from "react";
import { base44 } from "@/api/base44Client";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { 
  Heart, 
  MessageCircle, 
  Share2, 
  Music2, 
  Plus,
  Play,
  Pause,
  Volume2,
  VolumeX,
  ChevronUp,
  ChevronDown
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const mockReels = [
  {
    id: "1",
    video_url: "https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=800",
    thumbnail_url: "https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=800",
    caption: "Explorando novos horizontes 🌅 #viagem #natureza",
    author_name: "Ana Beatriz",
    author_avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
    likes: ["user1", "user2", "user3"],
    views_count: 15420,
    music: "Sunset Dreams - Chill Vibes"
  },
  {
    id: "2",
    video_url: "https://images.unsplash.com/photo-1682687221038-404670f09439?w=800",
    thumbnail_url: "https://images.unsplash.com/photo-1682687221038-404670f09439?w=800",
    caption: "Momentos que importam ✨ #lifestyle",
    author_name: "Carlos Eduardo",
    author_avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150",
    likes: ["user1", "user2"],
    views_count: 8930,
    music: "Good Times - Summer Mix"
  },
  {
    id: "3",
    video_url: "https://images.unsplash.com/photo-1682695796954-bad0d0f59ff1?w=800",
    thumbnail_url: "https://images.unsplash.com/photo-1682695796954-bad0d0f59ff1?w=800",
    caption: "Arte em movimento 🎨 #arte #criatividade",
    author_name: "Marina Costa",
 