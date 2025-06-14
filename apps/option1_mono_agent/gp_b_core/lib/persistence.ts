import fs from 'fs'
import path from 'path'
import { SwarmState } from './types'

const PERSISTENCE_DIR = process.env.SWARM_STATE_DIR || path.join(process.cwd(), 'data')
const STATE_FILE = path.join(PERSISTENCE_DIR, 'swarm_state.json')

export function saveSwarmState(state: SwarmState): void {
  try {
    if (!fs.existsSync(PERSISTENCE_DIR)) {
      fs.mkdirSync(PERSISTENCE_DIR, { recursive: true })
    }
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2))
  } catch (error) {
    console.error('Failed to save swarm state:', error)
  }
}

export function loadSwarmState(): SwarmState | null {
  try {
    if (fs.existsSync(STATE_FILE)) {
      const data = fs.readFileSync(STATE_FILE, 'utf-8')
      return JSON.parse(data) as SwarmState
    }
  } catch (error) {
    console.error('Failed to load swarm state:', error)
  }
  return null
}
