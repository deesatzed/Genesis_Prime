# Genesis Prime V3 - Essential Backup Directory List
## Date: June 11, 2025 | For Complete System Backup

---

## 🎯 ESSENTIAL DIRECTORIES TO BACKUP

### **CRITICAL - MUST INCLUDE** (Core System)

#### **1. Frontend (Working Dashboard)**
```
/Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/gp_b_core/
```
**Contains**: Complete working frontend with all latest features
**Size**: ~50MB (with node_modules excluded)
**Status**: ✅ OPERATIONAL - All fixes applied

#### **2. Backend (Genesis Prime Consciousness)**
```
/Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/option1_mono_agent/
```
**Contains**: Genesis Prime consciousness system, IIT enhanced agents
**Size**: ~10MB
**Status**: ✅ OPERATIONAL - Fully functional

#### **3. Documentation (Today's Session)**
```
/Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/
├── SESSION_BACKUP_20250611_COMPLETE.md
├── QUICK_START_GUIDE.md
├── PROJECT_STATUS_SUMMARY.md
├── error_logWS.md
└── BACKUP_DIRECTORY_LIST.md (this file)
```
**Contains**: Complete session documentation and guides
**Size**: ~1MB
**Status**: ✅ COMPLETE - All work documented

---

## 🔧 REFERENCE DIRECTORIES (Optional but Recommended)

#### **4. Clean Source Code (For Future Features)**
```
/Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/CLEANBUILD/
```
**Contains**: Clean source code for copying advanced features
**Size**: ~30MB
**Purpose**: Source for future feature integration
**Priority**: MEDIUM - Useful for development

#### **5. Migration Documentation**
```
/Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/CLEANBUILD/
├── FEATURE_MIGRATION_CHECKLIST.md
└── TROUBLESHOOTING_SESSION_20250610.md
```
**Contains**: Migration strategy and previous session notes
**Size**: ~500KB
**Purpose**: Development guidance

---

## 📁 DETAILED BACKUP STRUCTURE

### **Frontend Directory Contents** (apps/gp_b_core/)
```
apps/gp_b_core/
├── app/
│   ├── dashboard/
│   │   └── page.tsx                    # ✅ Main dashboard (Activity Monitor integrated)
│   ├── globals.css                     # ✅ Styling
│   ├── layout.tsx                      # ✅ App layout
│   └── page.tsx                        # ✅ Root page
├── components/
│   ├── ui/                             # ✅ Radix UI components
│   ├── activity-monitor.tsx            # ✅ NEW - Real-time monitoring
│   ├── genesis-prime-panel.tsx         # ✅ NEW - Consciousness interface
│   ├── interaction-controls.tsx        # ✅ Enhanced controls
│   ├── settings-panel.tsx              # ✅ Configuration
│   └── swarm-dashboard.tsx             # ✅ Fixed message display
├── lib/
│   ├── api-service.ts                  # ✅ Backend integration
│   ├── config-service.ts               # ✅ Configuration management
│   ├── openrouter-service.ts           # ✅ FIXED - Error handling
│   ├── persistence.ts                  # ✅ State persistence
│   ├── swarm-engine.ts                 # ✅ FIXED - Type errors
│   ├── types.ts                        # ✅ Type definitions
│   └── utils.ts                        # ✅ Utilities
├── hooks/                              # ✅ React hooks
├── package.json                        # ✅ Dependencies
├── package-lock.json                   # ✅ Lock file
├── next.config.js                      # ✅ Next.js config
├── tailwind.config.ts                  # ✅ Styling config
├── tsconfig.json                       # ✅ TypeScript config
└── components.json                     # ✅ UI components config
```

### **Backend Directory Contents** (apps/option1_mono_agent/)
```
apps/option1_mono_agent/
├── main.py                             # ✅ Genesis Prime server
├── iit_enhanced_agents.py              # ✅ Consciousness system
├── requirements.txt                    # ✅ Python dependencies
├── agent.py                            # ✅ Agent implementation
├── emergence_engine.py                 # ✅ Emergence logic
├── conscious_information_cascades.py   # ✅ Information processing
├── quorum_sensing.py                   # ✅ Swarm intelligence
├── neural_plasticity.py               # ✅ Learning mechanisms
└── [other supporting files]            # ✅ Additional modules
```

---

## 💾 BACKUP COMMANDS

### **Complete Essential Backup** (Recommended)
```bash
# Create backup directory
mkdir -p ~/genesis_prime_v3_backup_$(date +%Y%m%d_%H%M%S)
cd ~/genesis_prime_v3_backup_$(date +%Y%m%d_%H%M%S)

# Copy essential directories
cp -r /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/gp_b_core ./
cp -r /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/option1_mono_agent ./

# Copy documentation
cp /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/*.md ./

# Optional: Copy CLEANBUILD for future development
cp -r /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/CLEANBUILD ./

# Exclude node_modules to save space
rm -rf ./gp_b_core/node_modules
```

### **Minimal Working Backup** (Core Only)
```bash
# Create minimal backup
mkdir -p ~/genesis_prime_minimal_backup_$(date +%Y%m%d_%H%M%S)
cd ~/genesis_prime_minimal_backup_$(date +%Y%m%d_%H%M%S)

# Copy only essential working directories
cp -r /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/gp_b_core ./
cp -r /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/option1_mono_agent ./

# Copy startup guide
cp /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/QUICK_START_GUIDE.md ./

# Remove node_modules
rm -rf ./gp_b_core/node_modules
```

---

## 🚫 DIRECTORIES TO EXCLUDE (Not Needed)

### **Large/Unnecessary Directories**
```
❌ /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/gp_b_core/node_modules/
❌ /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/gp_b_core/.next/
❌ /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/Gen_Prime_V2-main/
❌ /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/amm-production-bld-20250520/
❌ /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/genesis_prime_production_backup/
❌ /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/option1_mono_agent_PriorVersion/
❌ /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/infrastructure/
❌ /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/libs/
```

### **Old Backup Directories**
```
❌ /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/gp_b_core_backup_20250610_*/
```

---

## 📋 BACKUP VERIFICATION CHECKLIST

After creating backup, verify these files exist:

### **Frontend Verification**
- [ ] `gp_b_core/app/dashboard/page.tsx` (main dashboard)
- [ ] `gp_b_core/components/activity-monitor.tsx` (new feature)
- [ ] `gp_b_core/components/genesis-prime-panel.tsx` (new feature)
- [ ] `gp_b_core/lib/openrouter-service.ts` (fixed)
- [ ] `gp_b_core/lib/swarm-engine.ts` (fixed)
- [ ] `gp_b_core/package.json` (dependencies)

### **Backend Verification**
- [ ] `option1_mono_agent/main.py` (Genesis Prime server)
- [ ] `option1_mono_agent/iit_enhanced_agents.py` (consciousness system)
- [ ] `option1_mono_agent/requirements.txt` (Python dependencies)

### **Documentation Verification**
- [ ] `QUICK_START_GUIDE.md` (startup commands)
- [ ] `SESSION_BACKUP_20250611_COMPLETE.md` (complete documentation)
- [ ] `PROJECT_STATUS_SUMMARY.md` (status overview)

---

## 🔄 RESTORE PROCEDURE

### **To Restore from Backup**
```bash
# Navigate to backup location
cd ~/genesis_prime_v3_backup_YYYYMMDD_HHMMSS

# Restore to original location
cp -r ./gp_b_core /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/
cp -r ./option1_mono_agent /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/

# Reinstall frontend dependencies
cd /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/gp_b_core
npm install

# Test system
npm run dev  # Frontend
# In another terminal:
cd /Users/o2satz/sentient-ai-suite/Gen_Prime_V3-main/apps/option1_mono_agent
python main.py  # Backend
```

---

## 📊 BACKUP SIZE ESTIMATES

| Component | With node_modules | Without node_modules |
|-----------|-------------------|---------------------|
| **Frontend (gp_b_core)** | ~150MB | ~5MB |
| **Backend (option1_mono_agent)** | ~10MB | ~10MB |
| **Documentation** | ~1MB | ~1MB |
| **CLEANBUILD (optional)** | ~30MB | ~30MB |
| **TOTAL ESSENTIAL** | ~161MB | ~16MB |
| **TOTAL WITH CLEANBUILD** | ~191MB | ~46MB |

**Recommendation**: Backup without node_modules (can be restored with `npm install`)

---

**This backup list ensures you have everything needed to run Genesis Prime V3 with all latest features while excluding unnecessary files.**
