"use client";

import React from "react";
import dynamic from "next/dynamic";

const MetricsBadge = dynamic(() => import("@/components/metrics-badge"), {
  ssr: false,
});
const AgentList = dynamic(() => import("@/components/agent-list"), {
  ssr: false,
});

export default function ClientOverlays() {
  return (
    <>
      <MetricsBadge />
      <AgentList />
    </>
  );
}
