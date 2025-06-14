"use client";

import React, { useEffect, useState } from "react";

interface Metrics {
  session_id: string;
  created_at: string;
  prompt_tokens: number;
  completion_tokens: number;
  cost_usd: number;
}

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function MetricsBadge() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  useEffect(() => {
    async function fetchMetrics() {
      try {
        const res = await fetch(`${BACKEND_URL}/metrics`);
        if (res.ok) {
          const data = (await res.json()) as Metrics;
          setMetrics(data);
        }
      } catch (err) {
        // eslint-disable-next-line no-console
        console.error("Failed to fetch metrics", err);
      }
    }

    fetchMetrics();
    const id = setInterval(fetchMetrics, 5000);
    return () => clearInterval(id);
  }, []);

  if (!metrics) return null;

  const totalTokens = metrics.prompt_tokens + metrics.completion_tokens;

  return (
    <div className="fixed top-2 right-2 z-50 bg-slate-800/70 backdrop-blur-sm border border-slate-700 text-xs text-white px-3 py-1 rounded-lg shadow-lg flex items-center gap-2">
      <span className="text-cyan-400">{metrics.session_id.slice(0, 8)}</span>
      <span>T: {totalTokens}</span>
      <span>${metrics.cost_usd.toFixed(4)}</span>
    </div>
  );
}
