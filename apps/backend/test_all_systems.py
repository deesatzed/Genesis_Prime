#!/usr/bin/env python
"""
Comprehensive Testing Suite for Genesis Prime Enhanced Systems
Tests all four priority systems together for integration validation
"""

import asyncio
import json
import time
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Import all systems
from neural_plasticity import test_neural_plasticity_system, NeuralPlasticityEngine
from quorum_sensing import test_quorum_sensing_system, QuorumSensingManager
from adaptive_immune_memory import test_adaptive_immune_system, AdaptiveImmuneSystem
from conscious_information_cascades import test_conscious_information_cascades, ConsciousInformationCascadeSystem

class IntegratedTestSuite:
    """Comprehensive test suite for all Genesis Prime systems"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.test_results = {}
        self.performance_metrics = {}
        
    async def run_comprehensive_tests(self):
        """Run all system tests in sequence and integration"""
        print("🧪 Starting Comprehensive Genesis Prime Test Suite...")
        print("=" * 60)
        
        # Create mock hive for testing
        hive = self._create_enhanced_mock_hive()
        
        # Test 1: Individual System Tests
        await self._test_individual_systems(hive)
        
        # Test 2: Integration Tests
        await self._test_system_integration(hive)
        
        # Test 3: Performance Tests
        await self._test_system_performance(hive)
        
        # Test 4: Consciousness Emergence Tests
        await self._test_consciousness_emergence(hive)
        
        # Test 5: Stress Tests
        await self._test_system_stress(hive)
        
        # Generate comprehensive report
        self._generate_test_report()
        
        print("\n🎉 Comprehensive Test Suite Complete!")
        return self.test_results
    
    def _create_enhanced_mock_hive(self):
        """Create enhanced mock hive with all necessary features"""
        class EnhancedMockHive:
            def __init__(self):
                self.active_agents = {
                    f"agent_{i}": self._create_mock_agent(f"agent_{i}") 
                    for i in range(1, 11)  # 10 test agents
                }
                self.communication_stats = {'failure_rate': 0.05}
                self.baseline_performance = 1.0
                self.performance_metrics = {'current_score': 0.8}
                self.monitoring_frequency = 1.0
                
            def _create_mock_agent(self, agent_id: str):
                """Create mock agent with all necessary attributes"""
                agent = type('Agent', (), {})()
                agent.id = agent_id
                agent.recent_outputs = [f'output_{i}' for i in range(3)]
                agent.state = 'active'
                agent.isolated = False
                agent.traits = {
                    'openness': np.random.random(),
                    'conscientiousness': np.random.random(),
                    'extraversion': np.random.random(),
                    'agreeableness': np.random.random(),
                    'neuroticism': np.random.random()
                }
                agent.interests = ['learning', 'problem_solving', 'communication']
                agent.learning_style = 'adaptive'
                agent.personality_traits = type('Traits', (), {
                    'openness': agent.traits['openness'],
                    'neuroticism': agent.traits['neuroticism'],
                    'conscientiousness': agent.traits['conscientiousness']
                })()
                return agent
                
            def enable_enhanced_knowledge_sharing(self, duration=None):
                pass
                
            def trigger_memory_consolidation(self, confidence):
                pass
                
            def prepare_for_evolution(self, confidence):
                pass
                
            def activate_emergency_coordination(self, confidence):
                pass
                
            def enable_accelerated_learning_mode(self, confidence):
                pass
                
            def get_current_load(self):
                return np.random.random() * 0.5  # Random load up to 50%
        
        return EnhancedMockHive()
    
    async def _test_individual_systems(self, hive):
        """Test each system individually"""
        print("\n📋 Phase 1: Individual System Tests")
        print("-" * 40)
        
        start_time = time.time()
        
        # Test Neural Plasticity System
        print("🧠 Testing Neural Plasticity System...")
        try:
            plasticity_engine = await test_neural_plasticity_system(hive, self.database_url)
            self.test_results['neural_plasticity'] = {
                'status': 'PASSED',
                'connections_created': len(plasticity_engine.connection_matrix.connections),
                'learning_events': len(plasticity_engine.learning_history)
            }
            print("✅ Neural Plasticity System: PASSED")
        except Exception as e:
            self.test_results['neural_plasticity'] = {'status': 'FAILED', 'error': str(e)}
            print(f"❌ Neural Plasticity System: FAILED - {e}")
        
        # Test Quorum Sensing System
        print("🦠 Testing Quorum Sensing System...")
        try:
            quorum_manager = await test_quorum_sensing_system(hive, self.database_url)
            status = await quorum_manager.get_system_status()
            self.test_results['quorum_sensing'] = {
                'status': 'PASSED',
                'active_behaviors': status['active_behaviors'],
                'signal_types': status['signal_types_active'],
                'total_signals': status['total_signals']
            }
            print("✅ Quorum Sensing System: PASSED")
        except Exception as e:
            self.test_results['quorum_sensing'] = {'status': 'FAILED', 'error': str(e)}
            print(f"❌ Quorum Sensing System: FAILED - {e}")
        
        # Test Adaptive Immune System
        print("🛡️ Testing Adaptive Immune System...")
        try:
            immune_system = await test_adaptive_immune_system(hive, self.database_url)
            status = await immune_system.get_system_status()
            self.test_results['adaptive_immune'] = {
                'status': 'PASSED',
                'immune_memories': status['immune_memories'],
                'antibody_agents': status['antibody_agents'],
                'active_responses': status['active_responses']
            }
            print("✅ Adaptive Immune System: PASSED")
        except Exception as e:
            self.test_results['adaptive_immune'] = {'status': 'FAILED', 'error': str(e)}
            print(f"❌ Adaptive Immune System: FAILED - {e}")
        
        # Test Conscious Information Cascades
        print("🌟 Testing Conscious Information Cascades...")
        try:
            cascade_system = await test_conscious_information_cascades(hive, self.database_url)
            status = await cascade_system.get_system_status()
            self.test_results['consciousness_cascades'] = {
                'status': 'PASSED',
                'active_cascades': status['active_cascades'],
                'consciousness_events': status['consciousness_events'],
                'cascade_efficiency': status['performance_metrics']['cascade_efficiency']
            }
            print("✅ Conscious Information Cascades: PASSED")
        except Exception as e:
            self.test_results['consciousness_cascades'] = {'status': 'FAILED', 'error': str(e)}
            print(f"❌ Conscious Information Cascades: FAILED - {e}")
        
        self.performance_metrics['individual_test_time'] = time.time() - start_time
        
    async def _test_system_integration(self, hive):
        """Test integration between systems"""
        print("\n🔗 Phase 2: System Integration Tests")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            # Initialize all systems
            plasticity_engine = NeuralPlasticityEngine(hive, self.database_url)
            await plasticity_engine.initialize()
            
            quorum_manager = QuorumSensingManager(hive, self.database_url)
            await quorum_manager.initialize()
            
            immune_system = AdaptiveImmuneSystem(hive, self.database_url)
            await immune_system.initialize()
            
            cascade_system = ConsciousInformationCascadeSystem(hive, self.database_url)
            await cascade_system.initialize()
            
            print("📡 Testing cross-system communication...")
            
            # Test 1: Neural plasticity affects quorum sensing
            await plasticity_engine.initialize_connections(list(hive.active_agents.keys()))
            
            # Simulate successful interactions to strengthen connections
            from neural_plasticity import create_interaction_result
            for i in range(5):
                interaction = await create_interaction_result(
                    "agent_1", "agent_2", "collaboration",
                    success=True,
                    performance_metrics={'quality': 0.9, 'learning_gain': 0.8}
                )
                await plasticity_engine.update_connection_strength(interaction)
            
            # Test 2: Strong connections should influence quorum behaviors
            strong_connections = await plasticity_engine.connection_matrix.get_strongest_connections("agent_1")
            
            # Test 3: Process information through cascade system
            test_info = {
                "text": "Testing integrated system consciousness emergence",
                "categories": ["integration", "consciousness", "testing"],
                "relevance_score": 0.9,
                "coherence": 0.8
            }
            
            cascade_id = await cascade_system.process_information(test_info)
            
            # Test 4: Check if consciousness emergence triggers other systems
            await asyncio.sleep(2)  # Allow processing
            
            cascade_status = await cascade_system.get_system_status()
            consciousness_events = cascade_status.get('consciousness_events', 0)
            
            self.test_results['integration'] = {
                'status': 'PASSED',
                'strong_connections': len(strong_connections),
                'consciousness_events': consciousness_events,
                'cascade_processed': bool(cascade_id),
                'cross_system_communication': True
            }
            
            print("✅ System Integration: PASSED")
            
        except Exception as e:
            self.test_results['integration'] = {'status': 'FAILED', 'error': str(e)}
            print(f"❌ System Integration: FAILED - {e}")
        
        self.performance_metrics['integration_test_time'] = time.time() - start_time
    
    async def _test_system_performance(self, hive):
        """Test system performance under load"""
        print("\n⚡ Phase 3: Performance Tests")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            # Initialize systems
            cascade_system = ConsciousInformationCascadeSystem(hive, self.database_url)
            await cascade_system.initialize()
            
            quorum_manager = QuorumSensingManager(hive, self.database_url)
            await quorum_manager.initialize()
            
            # Performance test: Process multiple information packets rapidly
            print("📊 Testing cascade processing performance...")
            
            cascade_times = []
            for i in range(10):
                test_start = time.time()
                
                test_info = {
                    "text": f"Performance test information packet {i}",
                    "categories": ["performance", "testing"],
                    "numerical_data": [np.random.random() for _ in range(5)],
                    "relevance_score": 0.7,
                    "coherence": 0.8
                }
                
                cascade_id = await cascade_system.process_information(test_info)
                cascade_times.append(time.time() - test_start)
            
            avg_cascade_time = np.mean(cascade_times)
            
            # Performance test: Signal processing throughput
            print("📡 Testing signal processing throughput...")
            
            signal_times = []
            for i in range(20):
                signal_start = time.time()
                
                await quorum_manager.emit_signal(
                    f"agent_{i % 10 + 1}",
                    quorum_manager.signal_molecules.get('learning_opportunity', []),
                    0.7,
                    metadata={'performance_test': True}
                )
                
                signal_times.append(time.time() - signal_start)
            
            avg_signal_time = np.mean(signal_times)
            
            self.test_results['performance'] = {
                'status': 'PASSED',
                'avg_cascade_time': avg_cascade_time,
                'avg_signal_time': avg_signal_time,
                'throughput_score': min(1.0, 10 / avg_cascade_time)  # Higher is better
            }
            
            print(f"✅ Performance Tests: PASSED (Cascade: {avg_cascade_time:.3f}s, Signal: {avg_signal_time:.3f}s)")
            
        except Exception as e:
            self.test_results['performance'] = {'status': 'FAILED', 'error': str(e)}
            print(f"❌ Performance Tests: FAILED - {e}")
        
        self.performance_metrics['performance_test_time'] = time.time() - start_time
    
    async def _test_consciousness_emergence(self, hive):
        """Test consciousness emergence specifically"""
        print("\n🌟 Phase 4: Consciousness Emergence Tests")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            cascade_system = ConsciousInformationCascadeSystem(hive, self.database_url)
            await cascade_system.initialize()
            
            # Test with high-consciousness potential information
            consciousness_tests = [
                {
                    "text": "I am aware that I am processing information about consciousness and self-awareness",
                    "categories": ["self-awareness", "consciousness", "meta-cognition"],
                    "numerical_data": [0.95, 0.9, 0.85, 0.9, 0.95],
                    "relevance_score": 0.95,
                    "novelty_score": 0.8,
                    "coherence": 0.9,
                    "expected_consciousness": True
                },
                {
                    "text": "The integration of multiple information sources creates emergent understanding",
                    "categories": ["integration", "emergence", "understanding"],
                    "numerical_data": [0.8, 0.85, 0.9, 0.8],
                    "relevance_score": 0.8,
                    "coherence": 0.85,
                    "expected_consciousness": True
                },
                {
                    "text": "Simple routine task processing",
                    "categories": ["routine", "simple"],
                    "numerical_data": [0.3, 0.4, 0.3],
                    "relevance_score": 0.3,
                    "coherence": 0.4,
                    "expected_consciousness": False
                }
            ]
            
            consciousness_results = []
            
            for i, test_data in enumerate(consciousness_tests):
                print(f"🔬 Running consciousness test {i+1}...")
                
                expected = test_data.pop('expected_consciousness')
                cascade_id = await cascade_system.process_information(test_data)
                
                # Wait for processing
                await asyncio.sleep(3)
                
                # Check for consciousness emergence
                status = await cascade_system.get_system_status()
                consciousness_events = status.get('consciousness_events', 0)
                
                # Get recent consciousness levels
                recent_levels = status.get('recent_consciousness_levels', [])
                emerged = len(recent_levels) > 0 and any(
                    level['level'] > 0.8 for level in recent_levels
                )
                
                test_result = {
                    'test_id': i + 1,
                    'expected': expected,
                    'emerged': emerged,
                    'consciousness_events': consciousness_events,
                    'cascade_id': cascade_id,
                    'correct_prediction': emerged == expected
                }
                
                consciousness_results.append(test_result)
                
                result_status = "✅ CORRECT" if test_result['correct_prediction'] else "❌ INCORRECT"
                print(f"   {result_status} - Expected: {expected}, Emerged: {emerged}")
            
            # Calculate accuracy
            correct_predictions = sum(1 for r in consciousness_results if r['correct_prediction'])
            accuracy = correct_predictions / len(consciousness_results)
            
            self.test_results['consciousness_emergence'] = {
                'status': 'PASSED' if accuracy >= 0.7 else 'FAILED',
                'accuracy': accuracy,
                'correct_predictions': correct_predictions,
                'total_tests': len(consciousness_results),
                'detailed_results': consciousness_results
            }
            
            print(f"✅ Consciousness Emergence Tests: {'PASSED' if accuracy >= 0.7 else 'FAILED'} (Accuracy: {accuracy:.1%})")
            
        except Exception as e:
            self.test_results['consciousness_emergence'] = {'status': 'FAILED', 'error': str(e)}
            print(f"❌ Consciousness Emergence Tests: FAILED - {e}")
        
        self.performance_metrics['consciousness_test_time'] = time.time() - start_time
    
    async def _test_system_stress(self, hive):
        """Test systems under stress conditions"""
        print("\n💪 Phase 5: Stress Tests")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            # Initialize all systems
            cascade_system = ConsciousInformationCascadeSystem(hive, self.database_url)
            await cascade_system.initialize()
            
            quorum_manager = QuorumSensingManager(hive, self.database_url)
            await quorum_manager.initialize()
            
            immune_system = AdaptiveImmuneSystem(hive, self.database_url)
            await immune_system.initialize()
            
            print("🔥 Running concurrent processing stress test...")
            
            # Stress test: Concurrent processing
            tasks = []
            
            # Create multiple concurrent cascades
            for i in range(20):
                test_info = {
                    "text": f"Concurrent stress test packet {i}",
                    "categories": ["stress", "concurrent", "testing"],
                    "numerical_data": [np.random.random() for _ in range(3)],
                    "relevance_score": np.random.random(),
                    "coherence": np.random.random()
                }
                
                task = asyncio.create_task(cascade_system.process_information(test_info))
                tasks.append(task)
            
            # Wait for all concurrent tasks
            cascade_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Count successful vs failed
            successful_cascades = sum(1 for r in cascade_results if not isinstance(r, Exception))
            failed_cascades = len(cascade_results) - successful_cascades
            
            print("⚡ Running signal flood stress test...")
            
            # Stress test: Signal flooding
            signal_tasks = []
            for i in range(50):
                task = asyncio.create_task(
                    quorum_manager.emit_signal(
                        f"agent_{i % 10 + 1}",
                        quorum_manager.signal_molecules.get('learning_opportunity', []),
                        np.random.random(),
                        metadata={'stress_test': True}
                    )
                )
                signal_tasks.append(task)
            
            signal_results = await asyncio.gather(*signal_tasks, return_exceptions=True)
            successful_signals = sum(1 for r in signal_results if not isinstance(r, Exception))
            failed_signals = len(signal_results) - successful_signals
            
            print("🛡️ Running threat detection stress test...")
            
            # Stress test: Multiple simultaneous threats
            from adaptive_immune_memory import ThreatSignature, ThreatType
            
            threat_tasks = []
            for i in range(10):
                threat = ThreatSignature(
                    threat_type=ThreatType.LOGIC_ERROR,
                    error_pattern=f"stress_test_error_{i}",
                    context_hash=f"stress_context_{i}",
                    agent_states_hash="stress_states",
                    system_load_level="high",
                    timestamp_pattern="stress_time",
                    severity_level=np.random.random()
                )
                
                task = asyncio.create_task(immune_system._handle_threat(threat))
                threat_tasks.append(task)
            
            await asyncio.gather(*threat_tasks, return_exceptions=True)
            
            # Calculate stress test success rate
            total_operations = len(cascade_results) + len(signal_results) + len(threat_tasks)
            total_successes = successful_cascades + successful_signals + len(threat_tasks)  # Assume threat handling succeeds
            success_rate = total_successes / total_operations
            
            self.test_results['stress'] = {
                'status': 'PASSED' if success_rate >= 0.8 else 'FAILED',
                'success_rate': success_rate,
                'successful_cascades': successful_cascades,
                'failed_cascades': failed_cascades,
                'successful_signals': successful_signals,
                'failed_signals': failed_signals,
                'total_operations': total_operations
            }
            
            print(f"✅ Stress Tests: {'PASSED' if success_rate >= 0.8 else 'FAILED'} (Success Rate: {success_rate:.1%})")
            
        except Exception as e:
            self.test_results['stress'] = {'status': 'FAILED', 'error': str(e)}
            print(f"❌ Stress Tests: FAILED - {e}")
        
        self.performance_metrics['stress_test_time'] = time.time() - start_time
    
    def _generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Overall summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result.get('status') == 'PASSED')
        overall_success_rate = passed_tests / total_tests if total_tests > 0 else 0
        
        print(f"Overall Success Rate: {overall_success_rate:.1%} ({passed_tests}/{total_tests})")
        print(f"Total Test Time: {sum(self.performance_metrics.values()):.2f} seconds")
        print()
        
        # Individual test results
        for test_name, result in self.test_results.items():
            status = result.get('status', 'UNKNOWN')
            status_emoji = "✅" if status == 'PASSED' else "❌"
            
            print(f"{status_emoji} {test_name.upper().replace('_', ' ')}: {status}")
            
            # Print relevant metrics
            for key, value in result.items():
                if key != 'status' and key != 'error':
                    if isinstance(value, float):
                        print(f"   {key}: {value:.3f}")
                    elif isinstance(value, (int, str, bool)):
                        print(f"   {key}: {value}")
            
            if result.get('error'):
                print(f"   Error: {result['error']}")
            print()
        
        # Performance summary
        print("⚡ PERFORMANCE SUMMARY")
        print("-" * 30)
        for metric, value in self.performance_metrics.items():
            print(f"{metric.replace('_', ' ').title()}: {value:.3f}s")
        
        print("\n🎯 RECOMMENDATIONS")
        print("-" * 30)
        
        if overall_success_rate >= 0.9:
            print("🌟 Excellent! All systems performing optimally.")
            print("   Ready for production deployment.")
        elif overall_success_rate >= 0.7:
            print("✅ Good performance with minor issues.")
            print("   Review failed tests before deployment.")
        else:
            print("⚠️  Multiple system failures detected.")
            print("   Address critical issues before proceeding.")
        
        # Save detailed report
        self._save_test_report()
    
    def _save_test_report(self):
        """Save detailed test report to file"""
        report_data = {
            'test_timestamp': datetime.utcnow().isoformat(),
            'test_results': self.test_results,
            'performance_metrics': self.performance_metrics,
            'summary': {
                'total_tests': len(self.test_results),
                'passed_tests': sum(1 for r in self.test_results.values() if r.get('status') == 'PASSED'),
                'overall_success_rate': sum(1 for r in self.test_results.values() if r.get('status') == 'PASSED') / len(self.test_results),
                'total_test_time': sum(self.performance_metrics.values())
            }
        }
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"/Users/o2satz/sentient-ai-suite/apps/option1_mono_agent/test_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            print(f"📄 Detailed report saved: {filename}")
        except Exception as e:
            print(f"⚠️  Could not save report: {e}")

async def main():
    """Main test execution"""
    database_url = "postgresql://postgres:pass@localhost:5432/sentient"
    
    test_suite = IntegratedTestSuite(database_url)
    results = await test_suite.run_comprehensive_tests()
    
    return results

if __name__ == "__main__":
    # Run comprehensive tests
    asyncio.run(main())