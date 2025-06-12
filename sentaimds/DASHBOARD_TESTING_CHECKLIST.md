### AgnoSwarm Dashboard - Functional Test Checklist

Here's a semantic checklist you can follow to test the current stage of the application:

**I. Initial Load & Basic UI:**
    *   [ ] **Dashboard Loads:** Navigate to the `/dashboard` page. Does it load without any immediate console errors or crashes?
    *   [ ] **Header Display:** Is the new header ("AgnoSwarm Mission Control" with Brain icon and Settings button) correctly displayed at the top?
    *   [ ] **Agent Roster:** Does the "Agent Roster" panel on the left populate with agents (assuming configuration provides them)?
    *   [ ] **Main Panels:** Are the "Swarm Activity Visualizer" and "Agent Consciousness Detail" (or similar main content areas) visible?

**II. Settings Panel Interaction:**
    *   [ ] **Open Settings:** Click the "Settings" icon button in the header. Does the Settings Panel slide out?
    *   [ ] **Close Settings:**
        *   [ ] Can you close the Settings Panel by clicking the "X" or an equivalent close button within the panel?
        *   [ ] Can you close the Settings Panel by clicking outside of it (if it's a modal/sheet behavior)?
    *   [ ] **Settings Content:** Does the Settings Panel display configuration options as expected (e.g., API key input, agent model selectors)? (Functionality of these settings is a deeper test, for now just visual confirmation).

**III. Simulation Controls & Feedback:**
    *   [ ] **Start Simulation:**
        *   [ ] Click the "Start Swarm" (or equivalent) button in the `InteractionControls`.
        *   [ ] Does the simulation appear to start (e.g., "Stop Swarm" button becomes active, agent activity might change)?
        *   [ ] Is a toast notification displayed indicating the simulation has started?
    *   [ ] **Stop Simulation:**
        *   [ ] While the simulation is running, click the "Stop Swarm" button.
        *   [ ] Does the simulation appear to stop (e.g., "Start Swarm" button becomes active again)?
        *   [ ] Is a toast notification displayed indicating the simulation has stopped?
    *   [ ] **Change Simulation Speed:**
        *   [ ] Interact with the simulation speed control (e.g., slider or input).
        *   [ ] If the simulation is running, does its update frequency visually change?
        *   [ ] Is a toast notification displayed confirming the speed change?

**IV. Agent & Swarm Activity:**
    *   [ ] **Agent Selection:** Click on different agents in the "Agent Roster". Does the "Agent Consciousness Detail" panel update to reflect the selected agent's information?
    *   [ ] **Agent `current_action` Display:** Do agents in the roster show their `current_action` and corresponding icon (e.g., "Observing" with Eye icon)? (This depends on `runSwarmTick` updating these fields).
    *   [ ] **Emergent Behavior Detection:**
        *   [ ] Let the simulation run for a while. Are any emergent behaviors detected and listed in the "Emergent Behaviors" panel?
        *   [ ] Is a toast notification displayed when a new emergent behavior is detected?
    *   [ ] **Manual Emergent Behavior Introduction:**
        *   [ ] If there's a UI option to manually introduce an emergent behavior (via `InteractionControls`), try it.
        *   [ ] Is the behavior added to the list?
        *   [ ] Is a toast notification displayed?

**V. General Stability & Console:**
    *   [ ] **No New Console Errors:** While interacting with the dashboard, keep an eye on the browser's developer console. Are there any new critical JavaScript errors appearing?
    *   [ ] **Responsiveness:** Does the UI remain responsive during interactions and while the simulation is running?
