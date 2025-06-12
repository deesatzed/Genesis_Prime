// /Users/o2satz/AMM/Genesis_Prime/GP_b/agno_swarm_demo/app/app/test/page.tsx
export default function TestPage() {
  return (
    <div className="flex h-screen flex-col items-center justify-center bg-gray-900 p-8">
      <h1 className="mb-4 text-3xl font-bold text-blue-400">Tailwind Test Page</h1>
      <p className="mb-8 text-lg text-gray-300">If you see this styled, Tailwind is working.</p>
      <div className="flex space-x-4">
        <div className="h-32 w-32 rounded-lg bg-sky-500 p-4 text-white shadow-lg">Box 1 (Sky)</div>
        <div className="h-32 w-32 rounded-lg bg-emerald-500 p-4 text-white shadow-lg">Box 2 (Emerald)</div>
        <div className="h-32 w-32 rounded-lg bg-rose-500 p-4 text-white shadow-lg">Box 3 (Rose)</div>
      </div>
    </div>
  );
}
