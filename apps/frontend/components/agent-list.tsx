"use client";

import React, { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";

interface AgentSummary {
  agent_id: string;
  name: string;
  preset_name: string;
}

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function AgentList() {
  const [agents, setAgents] = useState<AgentSummary[]>([]);

  useEffect(() => {
    async function fetchAgents() {
      try {
        const res = await fetch(`${BACKEND_URL}/agents`);
        if (res.ok) {
          const data = (await res.json()) as AgentSummary[];
          setAgents(data);
        }
      } catch (e) {
        // ignore for now
      }
    }

    fetchAgents();
    const id = setInterval(fetchAgents, 10000);
    return () => clearInterval(id);
  }, []);

  if (agents.length === 0) return null;

  return (
    <div className="fixed left-2 top-14 z-40 bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg border border-slate-700 w-48 max-h-[70vh] overflow-y-auto shadow-lg">
      <h4 className="text-xs font-semibold text-slate-300 mb-2">Agents</h4>
      <ul className="space-y-1">
        {agents.map((a) => (
          <li key={a.agent_id} className="flex items-center justify-between text-xs text-white">
            <span>{a.name}</span>
            <Badge>{a.preset_name}</Badge>
          </li>
        ))}
      </ul>
    </div>
  );
}
