import React from "react";
import { TrendingUp, Hash } from "lucide-react";
import { motion } from "framer-motion";

const trends = [
  { tag: "tecnologia", posts: "12.5K" },
  { tag: "viagem", posts: "8.2K" },
  { tag: "fotografia", posts: "6.8K" },
  { tag: "música", posts: "5.4K" },
  { tag: "arte", posts: "4.1K" },
];

export default function TrendingTopics() {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-4">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp className="w-5 h-5 text-violet-600" />
        <h3 className="font-semibold text-slate-800">Em alta</h3>
      </div>

      <div className="space-y-3">
        {trends.map((trend, index) => (
          <motion.div
            key={trend.tag}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center justify-between cursor-pointer hover:bg-slate-50 -mx-2 px-2 py-2 rounded-xl transition-colors"
          >
            <div className="flex items-center gap-2">
              <Hash className="w-4 h-4 text-violet-500" />
              <span className="font-medium text-slate-700">{trend.tag}</span>
            </div>
            <span className="text-sm text-slate-500">{trend.posts} posts</span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}