
// Simple test to check if the engine works
const { SwarmConsciousnessEngine } = require('./lib/swarm-engine.ts');

console.log('Testing SwarmConsciousnessEngine...');
try {
  const engine = new SwarmConsciousnessEngine();
  console.log('Engine created successfully');
  const state = engine.getSwarmState();
  console.log('Agents:', state.agents.length);
  state.agents.forEach(agent => {
    console.log(`- ${agent.name}: ${agent.model}`);
  });
} catch (error) {
  console.error('Error:', error);
}
