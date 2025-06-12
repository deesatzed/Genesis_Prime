#!/usr/bin/env python
"""
Conscious Information Cascades for Genesis Prime
Implements hierarchical information processing with consciousness emergence at critical integration points
"""

import asyncio
import json
import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import psycopg
from psycopg.rows import dict_row

class CascadeLayerType(Enum):
    """Types of cascade processing layers"""
    SENSORY = "sensory"
    PREPROCESSING = "preprocessing"
    INTEGRATION = "integration"
    META_COGNITIVE = "meta_cognitive"
    CONSCIOUSNESS = "consciousness"

class ConsciousnessLevel(Enum):
    """Levels of consciousness detection"""
    NONE = "none"
    EMERGING = "emerging"
    PARTIAL = "partial"
    COHERENT = "coherent"
    UNIFIED = "unified"

class InformationType(Enum):
    """Types of information flowing through cascades"""
    SENSORY_INPUT = "sensory_input"
    PROCESSED_DATA = "processed_data"
    PATTERN_RECOGNITION = "pattern_recognition"
    CONCEPTUAL_KNOWLEDGE = "conceptual_knowledge"
    META_KNOWLEDGE = "meta_knowledge"
    CONSCIOUS_AWARENESS = "conscious_awareness"

@dataclass
class InformationPacket:
    """Unit of information flowing through cascades"""
    packet_id: str
    information_type: InformationType
    content: Dict[str, Any]
    source_layer: CascadeLayerType
    target_layer: Optional[CascadeLayerType]
    timestamp: datetime
    priority: float
    coherence_score: float
    integration_requirements: List[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for processing"""
        return {
            'packet_id': self.packet_id,
            'information_type': self.information_type.value,
            'content': self.content,
            'source_layer': self.source_layer.value,
            'target_layer': self.target_layer.value if self.target_layer else None,
            'timestamp': self.timestamp.isoformat(),
            'priority': self.priority,
            'coherence_score': self.coherence_score,
            'integration_requirements': self.integration_requirements,
            'metadata': self.metadata
        }

@dataclass
class CascadeState:
    """Current state of information cascade"""
    cascade_id: str
    active_packets: List[InformationPacket]
    layer_states: Dict[CascadeLayerType, Dict[str, Any]]
    integration_points: List[Tuple[str, str, float]]  # (packet1, packet2, integration_score)
    feedback_signals: List[Dict[str, Any]]
    consciousness_indicators: Dict[str, float]
    coherence_metrics: Dict[str, float]
    timestamp: datetime
    
    def get_consciousness_level(self) -> ConsciousnessLevel:
        """Determine overall consciousness level"""
        awareness_score = self.consciousness_indicators.get('awareness', 0.0)
        integration_score = self.consciousness_indicators.get('integration', 0.0)
        coherence_score = self.consciousness_indicators.get('coherence', 0.0)
        
        overall_score = (awareness_score + integration_score + coherence_score) / 3.0
        
        if overall_score > 0.9:
            return ConsciousnessLevel.UNIFIED
        elif overall_score > 0.7:
            return ConsciousnessLevel.COHERENT
        elif overall_score > 0.5:
            return ConsciousnessLevel.PARTIAL
        elif overall_score > 0.3:
            return ConsciousnessLevel.EMERGING
        else:
            return ConsciousnessLevel.NONE

@dataclass
class FeedbackSignal:
    """Feedback signal flowing back through cascade layers"""
    signal_id: str
    source_layer: CascadeLayerType
    target_layers: List[CascadeLayerType]
    signal_type: str
    content: Dict[str, Any]
    strength: float
    timestamp: datetime
    
    def apply_to_layer(self, layer: 'CascadeLayer') -> bool:
        """Apply feedback signal to a layer"""
        try:
            return layer.process_feedback(self)
        except Exception as e:
            print(f"❌ Error applying feedback signal {self.signal_id}: {e}")
            return False

class CascadeLayer:
    """Base class for cascade processing layers"""
    
    def __init__(self, layer_type: CascadeLayerType, capacity: int = 100):
        self.layer_type = layer_type
        self.capacity = capacity
        self.active_packets: List[InformationPacket] = []
        self.processing_state: Dict[str, Any] = {}
        self.performance_metrics: Dict[str, float] = {
            'throughput': 0.0,
            'coherence': 0.0,
            'integration_success': 0.0
        }
        
    async def process_packet(self, packet: InformationPacket) -> List[InformationPacket]:
        """Process an information packet through this layer"""
        if len(self.active_packets) >= self.capacity:
            # Layer at capacity - prioritize processing
            await self._prioritize_processing()
        
        self.active_packets.append(packet)
        
        # Perform layer-specific processing
        processed_packets = await self._layer_specific_processing(packet)
        
        # Update performance metrics
        self._update_performance_metrics(packet, processed_packets)
        
        return processed_packets
    
    async def _layer_specific_processing(self, packet: InformationPacket) -> List[InformationPacket]:
        """Override in subclasses for specific processing logic"""
        return [packet]
    
    async def _prioritize_processing(self):
        """Prioritize packets when layer is at capacity"""
        # Sort by priority and remove lowest priority packets
        self.active_packets.sort(key=lambda p: p.priority, reverse=True)
        removed_count = max(1, len(self.active_packets) - self.capacity + 10)
        self.active_packets = self.active_packets[:-removed_count]
    
    def _update_performance_metrics(self, input_packet: InformationPacket, output_packets: List[InformationPacket]):
        """Update layer performance metrics"""
        self.performance_metrics['throughput'] = len(output_packets) / max(1, len(self.active_packets))
        
        if output_packets:
            avg_coherence = np.mean([p.coherence_score for p in output_packets])
            self.performance_metrics['coherence'] = avg_coherence
            
            # Integration success based on how well requirements are met
            integration_success = sum(
                len(p.integration_requirements) for p in output_packets
            ) / max(1, len(output_packets))
            self.performance_metrics['integration_success'] = min(1.0, integration_success / 5.0)
    
    def process_feedback(self, feedback: FeedbackSignal) -> bool:
        """Process feedback signal from higher layers"""
        try:
            # Adjust processing based on feedback
            if feedback.signal_type == "attention_focus":
                self._adjust_attention_focus(feedback.content)
            elif feedback.signal_type == "priority_boost":
                self._boost_packet_priorities(feedback.content)
            elif feedback.signal_type == "coherence_enhancement":
                self._enhance_coherence_processing(feedback.content)
            
            return True
        except Exception:
            return False
    
    def _adjust_attention_focus(self, content: Dict[str, Any]):
        """Adjust attention focus based on feedback"""
        focus_type = content.get('focus_type', 'general')
        for packet in self.active_packets:
            if focus_type in packet.content.get('categories', []):
                packet.priority *= 1.2  # Boost priority for focused items
    
    def _boost_packet_priorities(self, content: Dict[str, Any]):
        """Boost priorities of specific packets"""
        boost_criteria = content.get('criteria', {})
        for packet in self.active_packets:
            if self._meets_criteria(packet, boost_criteria):
                packet.priority *= content.get('boost_factor', 1.1)
    
    def _enhance_coherence_processing(self, content: Dict[str, Any]):
        """Enhance coherence processing"""
        coherence_target = content.get('target_coherence', 0.8)
        for packet in self.active_packets:
            if packet.coherence_score < coherence_target:
                # Apply coherence enhancement
                packet.coherence_score = min(1.0, packet.coherence_score * 1.1)
    
    def _meets_criteria(self, packet: InformationPacket, criteria: Dict[str, Any]) -> bool:
        """Check if packet meets specific criteria"""
        for key, value in criteria.items():
            if key == 'information_type':
                if packet.information_type.value != value:
                    return False
            elif key == 'min_priority':
                if packet.priority < value:
                    return False
            elif key == 'content_contains':
                if value not in str(packet.content):
                    return False
        return True
    
    def get_layer_state(self) -> Dict[str, Any]:
        """Get current state of this layer"""
        return {
            'layer_type': self.layer_type.value,
            'active_packets': len(self.active_packets),
            'capacity_used': len(self.active_packets) / self.capacity,
            'performance_metrics': self.performance_metrics.copy(),
            'processing_state': self.processing_state.copy()
        }

class SensoryLayer(CascadeLayer):
    """Sensory processing layer - first stage of information cascade"""
    
    def __init__(self):
        super().__init__(CascadeLayerType.SENSORY, capacity=200)
        self.sensory_filters: Dict[str, float] = {
            'relevance_threshold': 0.3,
            'novelty_boost': 1.2,
            'familiarity_decay': 0.9
        }
    
    async def _layer_specific_processing(self, packet: InformationPacket) -> List[InformationPacket]:
        """Process sensory information"""
        processed_packets = []
        
        # Apply sensory filtering
        if self._passes_sensory_filter(packet):
            # Extract features from sensory input
            features = await self._extract_sensory_features(packet)
            
            # Create processed packet
            processed_packet = InformationPacket(
                packet_id=f"processed_{packet.packet_id}",
                information_type=InformationType.PROCESSED_DATA,
                content={
                    'original_content': packet.content,
                    'extracted_features': features,
                    'sensory_quality': self._assess_sensory_quality(packet)
                },
                source_layer=CascadeLayerType.SENSORY,
                target_layer=CascadeLayerType.PREPROCESSING,
                timestamp=datetime.utcnow(),
                priority=packet.priority * self._calculate_priority_modifier(packet),
                coherence_score=self._calculate_coherence_score(packet, features),
                integration_requirements=['feature_binding', 'temporal_integration'],
                metadata={'processing_layer': 'sensory', 'features_extracted': len(features)}
            )
            
            processed_packets.append(processed_packet)
        
        return processed_packets
    
    def _passes_sensory_filter(self, packet: InformationPacket) -> bool:
        """Check if packet passes sensory filtering"""
        relevance = packet.content.get('relevance_score', 0.5)
        return relevance >= self.sensory_filters['relevance_threshold']
    
    async def _extract_sensory_features(self, packet: InformationPacket) -> Dict[str, Any]:
        """Extract features from sensory input"""
        content = packet.content
        features = {}
        
        # Extract basic features
        if 'text' in content:
            features['text_length'] = len(content['text'])
            features['word_count'] = len(content['text'].split())
            features['sentiment'] = self._analyze_sentiment(content['text'])
        
        if 'numerical_data' in content:
            features['data_range'] = self._calculate_data_range(content['numerical_data'])
            features['data_complexity'] = self._assess_data_complexity(content['numerical_data'])
        
        if 'categories' in content:
            features['category_count'] = len(content['categories'])
            features['primary_category'] = content['categories'][0] if content['categories'] else 'unknown'
        
        # Extract temporal features
        features['temporal_pattern'] = self._detect_temporal_pattern(packet)
        
        return features
    
    def _analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'achievement']
        negative_words = ['bad', 'terrible', 'negative', 'failure', 'problem', 'error']
        
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            return 0.5  # Neutral
        
        return positive_count / total_sentiment_words
    
    def _calculate_data_range(self, data: List) -> float:
        """Calculate range of numerical data"""
        if not data or not all(isinstance(x, (int, float)) for x in data):
            return 0.0
        return max(data) - min(data)
    
    def _assess_data_complexity(self, data: List) -> float:
        """Assess complexity of data"""
        if not data:
            return 0.0
        
        # Simple complexity based on variance
        if all(isinstance(x, (int, float)) for x in data):
            return np.std(data) if len(data) > 1 else 0.0
        else:
            # For non-numerical data, use diversity
            return len(set(str(x) for x in data)) / len(data)
    
    def _detect_temporal_pattern(self, packet: InformationPacket) -> str:
        """Detect temporal patterns in information"""
        hour = packet.timestamp.hour
        
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def _assess_sensory_quality(self, packet: InformationPacket) -> float:
        """Assess quality of sensory input"""
        quality_factors = []
        
        # Completeness
        content_keys = len(packet.content.keys())
        completeness = min(1.0, content_keys / 5.0)  # Assume 5 keys is complete
        quality_factors.append(completeness)
        
        # Clarity (inverse of ambiguity)
        clarity = packet.coherence_score
        quality_factors.append(clarity)
        
        # Relevance
        relevance = packet.content.get('relevance_score', 0.5)
        quality_factors.append(relevance)
        
        return np.mean(quality_factors)
    
    def _calculate_priority_modifier(self, packet: InformationPacket) -> float:
        """Calculate priority modifier for sensory processing"""
        modifier = 1.0
        
        # Boost novel information
        if packet.content.get('novelty_score', 0.5) > 0.7:
            modifier *= self.sensory_filters['novelty_boost']
        
        # Reduce familiar information
        if packet.content.get('familiarity_score', 0.5) > 0.8:
            modifier *= self.sensory_filters['familiarity_decay']
        
        return modifier
    
    def _calculate_coherence_score(self, packet: InformationPacket, features: Dict[str, Any]) -> float:
        """Calculate coherence score based on features"""
        coherence_factors = []
        
        # Internal consistency of features
        if 'sentiment' in features and 'text_length' in features:
            # Longer texts with clear sentiment are more coherent
            sentiment_clarity = abs(features['sentiment'] - 0.5) * 2  # 0-1 scale
            length_factor = min(1.0, features['text_length'] / 100)  # Normalize by expected length
            coherence_factors.append(sentiment_clarity * length_factor)
        
        # Feature completeness
        expected_features = 5
        feature_completeness = len(features) / expected_features
        coherence_factors.append(feature_completeness)
        
        # Original coherence
        coherence_factors.append(packet.coherence_score)
        
        return np.mean(coherence_factors) if coherence_factors else 0.5

class PreprocessingLayer(CascadeLayer):
    """Preprocessing layer - cleans and formats information"""
    
    def __init__(self):
        super().__init__(CascadeLayerType.PREPROCESSING, capacity=150)
        self.preprocessing_rules: Dict[str, Any] = {
            'noise_threshold': 0.2,
            'integration_weight': 0.7,
            'pattern_detection_threshold': 0.6
        }
    
    async def _layer_specific_processing(self, packet: InformationPacket) -> List[InformationPacket]:
        """Preprocess information for integration"""
        processed_packets = []
        
        # Clean and normalize data
        cleaned_content = await self._clean_and_normalize(packet)
        
        # Detect patterns
        patterns = await self._detect_patterns(cleaned_content)
        
        # Prepare for integration
        integration_ready = await self._prepare_for_integration(cleaned_content, patterns)
        
        if integration_ready:
            processed_packet = InformationPacket(
                packet_id=f"preprocessed_{packet.packet_id}",
                information_type=InformationType.PATTERN_RECOGNITION,
                content={
                    'cleaned_content': cleaned_content,
                    'detected_patterns': patterns,
                    'preprocessing_metadata': {
                        'noise_level': self._assess_noise_level(packet),
                        'pattern_confidence': self._calculate_pattern_confidence(patterns)
                    }
                },
                source_layer=CascadeLayerType.PREPROCESSING,
                target_layer=CascadeLayerType.INTEGRATION,
                timestamp=datetime.utcnow(),
                priority=packet.priority * self._calculate_preprocessing_modifier(patterns),
                coherence_score=self._enhance_coherence(packet.coherence_score, patterns),
                integration_requirements=['pattern_matching', 'contextual_binding'],
                metadata={'preprocessing_stage': 'pattern_detection', 'patterns_found': len(patterns)}
            )
            
            processed_packets.append(processed_packet)
        
        return processed_packets
    
    async def _clean_and_normalize(self, packet: InformationPacket) -> Dict[str, Any]:
        """Clean and normalize packet content"""
        content = packet.content.copy()
        cleaned_content = {}
        
        # Remove noise and normalize
        for key, value in content.items():
            if key == 'text' and isinstance(value, str):
                # Clean text
                cleaned_text = self._clean_text(value)
                cleaned_content[key] = cleaned_text
            elif key == 'numerical_data' and isinstance(value, list):
                # Normalize numerical data
                cleaned_data = self._normalize_numerical_data(value)
                cleaned_content[key] = cleaned_data
            else:
                cleaned_content[key] = value
        
        return cleaned_content
    
    def _clean_text(self, text: str) -> str:
        """Clean text data"""
        # Remove excessive whitespace
        cleaned = ' '.join(text.split())
        
        # Remove very short or very long words (likely noise)
        words = cleaned.split()
        filtered_words = [w for w in words if 2 <= len(w) <= 20]
        
        return ' '.join(filtered_words)
    
    def _normalize_numerical_data(self, data: List) -> List[float]:
        """Normalize numerical data"""
        if not data or not all(isinstance(x, (int, float)) for x in data):
            return data
        
        # Simple min-max normalization
        min_val = min(data)
        max_val = max(data)
        
        if max_val == min_val:
            return [0.5] * len(data)  # All values are the same
        
        return [(x - min_val) / (max_val - min_val) for x in data]
    
    async def _detect_patterns(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect patterns in cleaned content"""
        patterns = []
        
        # Text patterns
        if 'text' in content:
            text_patterns = self._detect_text_patterns(content['text'])
            patterns.extend(text_patterns)
        
        # Numerical patterns
        if 'numerical_data' in content:
            numerical_patterns = self._detect_numerical_patterns(content['numerical_data'])
            patterns.extend(numerical_patterns)
        
        # Structural patterns
        structural_patterns = self._detect_structural_patterns(content)
        patterns.extend(structural_patterns)
        
        return patterns
    
    def _detect_text_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect patterns in text"""
        patterns = []
        words = text.split()
        
        # Repetition patterns
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        repeated_words = [word for word, count in word_counts.items() if count > 1]
        if repeated_words:
            patterns.append({
                'type': 'repetition',
                'pattern': repeated_words,
                'confidence': min(1.0, len(repeated_words) / len(words))
            })
        
        # Length patterns
        avg_word_length = np.mean([len(word) for word in words]) if words else 0
        if avg_word_length > 6:  # Long words might indicate technical content
            patterns.append({
                'type': 'technical_language',
                'pattern': f'avg_length_{avg_word_length:.1f}',
                'confidence': min(1.0, (avg_word_length - 6) / 4)
            })
        
        return patterns
    
    def _detect_numerical_patterns(self, data: List) -> List[Dict[str, Any]]:
        """Detect patterns in numerical data"""
        patterns = []
        
        if not data or len(data) < 3:
            return patterns
        
        # Trend patterns
        if all(isinstance(x, (int, float)) for x in data):
            # Check for increasing trend
            increasing = all(data[i] <= data[i+1] for i in range(len(data)-1))
            decreasing = all(data[i] >= data[i+1] for i in range(len(data)-1))
            
            if increasing:
                patterns.append({
                    'type': 'trend',
                    'pattern': 'increasing',
                    'confidence': 0.9
                })
            elif decreasing:
                patterns.append({
                    'type': 'trend',
                    'pattern': 'decreasing',
                    'confidence': 0.9
                })
            
            # Check for cyclical patterns
            if len(data) >= 6:
                # Simple cyclical detection
                mid_point = len(data) // 2
                first_half = data[:mid_point]
                second_half = data[mid_point:mid_point*2]
                
                if len(first_half) == len(second_half):
                    similarity = self._calculate_sequence_similarity(first_half, second_half)
                    if similarity > 0.7:
                        patterns.append({
                            'type': 'cyclical',
                            'pattern': f'period_{len(first_half)}',
                            'confidence': similarity
                        })
        
        return patterns
    
    def _detect_structural_patterns(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect structural patterns in content"""
        patterns = []
        
        # Key presence patterns
        common_keys = ['text', 'numerical_data', 'categories', 'metadata']
        present_keys = [key for key in common_keys if key in content]
        
        if len(present_keys) >= 3:
            patterns.append({
                'type': 'rich_structure',
                'pattern': present_keys,
                'confidence': len(present_keys) / len(common_keys)
            })
        
        # Nesting patterns
        nested_levels = self._count_nesting_levels(content)
        if nested_levels > 2:
            patterns.append({
                'type': 'deep_nesting',
                'pattern': f'levels_{nested_levels}',
                'confidence': min(1.0, nested_levels / 5)
            })
        
        return patterns
    
    def _calculate_sequence_similarity(self, seq1: List, seq2: List) -> float:
        """Calculate similarity between two sequences"""
        if len(seq1) != len(seq2):
            return 0.0
        
        if not seq1:
            return 1.0
        
        # Normalize sequences
        norm_seq1 = self._normalize_numerical_data(seq1)
        norm_seq2 = self._normalize_numerical_data(seq2)
        
        # Calculate mean squared difference
        mse = np.mean([(a - b) ** 2 for a, b in zip(norm_seq1, norm_seq2)])
        
        # Convert to similarity (inverse of difference)
        return max(0.0, 1.0 - mse)
    
    def _count_nesting_levels(self, obj, level=0) -> int:
        """Count nesting levels in data structure"""
        if isinstance(obj, dict):
            if not obj:
                return level
            return max(self._count_nesting_levels(v, level + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return level
            return max(self._count_nesting_levels(item, level + 1) for item in obj)
        else:
            return level
    
    async def _prepare_for_integration(self, content: Dict[str, Any], patterns: List[Dict[str, Any]]) -> bool:
        """Check if content is ready for integration"""
        # Must have sufficient patterns for integration
        pattern_threshold = self.preprocessing_rules['pattern_detection_threshold']
        pattern_confidence = self._calculate_pattern_confidence(patterns)
        
        return pattern_confidence >= pattern_threshold
    
    def _assess_noise_level(self, packet: InformationPacket) -> float:
        """Assess noise level in packet"""
        content = packet.content
        noise_indicators = 0
        total_indicators = 0
        
        # Check for text noise
        if 'text' in content:
            text = content['text']
            words = text.split()
            if words:
                # Very short words might be noise
                short_words = [w for w in words if len(w) <= 2]
                noise_indicators += len(short_words)
                total_indicators += len(words)
        
        # Check for data noise
        if 'numerical_data' in content:
            data = content['numerical_data']
            if data and all(isinstance(x, (int, float)) for x in data):
                # Outliers might be noise
                mean_val = np.mean(data)
                std_val = np.std(data)
                if std_val > 0:
                    outliers = [x for x in data if abs(x - mean_val) > 2 * std_val]
                    noise_indicators += len(outliers)
                    total_indicators += len(data)
        
        return noise_indicators / max(1, total_indicators)
    
    def _calculate_pattern_confidence(self, patterns: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence in detected patterns"""
        if not patterns:
            return 0.0
        
        confidences = [p.get('confidence', 0.5) for p in patterns]
        return np.mean(confidences)
    
    def _calculate_preprocessing_modifier(self, patterns: List[Dict[str, Any]]) -> float:
        """Calculate priority modifier based on preprocessing results"""
        pattern_count = len(patterns)
        pattern_confidence = self._calculate_pattern_confidence(patterns)
        
        # More patterns with higher confidence = higher priority
        modifier = 1.0 + (pattern_count * pattern_confidence * 0.1)
        
        return min(2.0, modifier)  # Cap at 2x boost
    
    def _enhance_coherence(self, original_coherence: float, patterns: List[Dict[str, Any]]) -> float:
        """Enhance coherence score based on pattern detection"""
        pattern_boost = self._calculate_pattern_confidence(patterns) * 0.2
        enhanced_coherence = original_coherence + pattern_boost
        
        return min(1.0, enhanced_coherence)

class IntegrationLayer(CascadeLayer):
    """Integration layer - combines information from multiple sources"""
    
    def __init__(self):
        super().__init__(CascadeLayerType.INTEGRATION, capacity=100)
        self.integration_window = timedelta(seconds=30)  # Window for integrating related packets
        self.pending_integrations: Dict[str, List[InformationPacket]] = {}
        
    async def _layer_specific_processing(self, packet: InformationPacket) -> List[InformationPacket]:
        """Integrate information packets"""
        processed_packets = []
        
        # Find packets to integrate with
        integration_candidates = await self._find_integration_candidates(packet)
        
        if integration_candidates:
            # Perform integration
            integrated_packet = await self._integrate_packets([packet] + integration_candidates)
            if integrated_packet:
                processed_packets.append(integrated_packet)
        else:
            # Store for future integration
            await self._store_for_integration(packet)
        
        # Process any completed integrations
        completed_integrations = await self._process_completed_integrations()
        processed_packets.extend(completed_integrations)
        
        return processed_packets
    
    async def _find_integration_candidates(self, packet: InformationPacket) -> List[InformationPacket]:
        """Find packets that can be integrated with the current packet"""
        candidates = []
        
        # Look through active packets
        for active_packet in self.active_packets:
            if active_packet.packet_id != packet.packet_id:
                similarity = await self._calculate_integration_similarity(packet, active_packet)
                if similarity > 0.7:  # Threshold for integration
                    candidates.append(active_packet)
        
        # Look through pending integrations
        for group_packets in self.pending_integrations.values():
            for pending_packet in group_packets:
                similarity = await self._calculate_integration_similarity(packet, pending_packet)
                if similarity > 0.7:
                    candidates.append(pending_packet)
        
        return candidates[:3]  # Limit to 3 candidates for now
    
    async def _calculate_integration_similarity(self, packet1: InformationPacket, packet2: InformationPacket) -> float:
        """Calculate similarity for integration purposes"""
        similarity_factors = []
        
        # Content similarity
        content_sim = self._calculate_content_similarity(packet1.content, packet2.content)
        similarity_factors.append(content_sim)
        
        # Temporal similarity
        time_diff = abs((packet1.timestamp - packet2.timestamp).total_seconds())
        temporal_sim = max(0.0, 1.0 - (time_diff / 300))  # 5 minutes window
        similarity_factors.append(temporal_sim)
        
        # Integration requirements overlap
        req1 = set(packet1.integration_requirements)
        req2 = set(packet2.integration_requirements)
        req_overlap = len(req1.intersection(req2)) / max(1, len(req1.union(req2)))
        similarity_factors.append(req_overlap)
        
        # Information type compatibility
        type_compatibility = self._calculate_type_compatibility(packet1.information_type, packet2.information_type)
        similarity_factors.append(type_compatibility)
        
        return np.mean(similarity_factors)
    
    def _calculate_content_similarity(self, content1: Dict[str, Any], content2: Dict[str, Any]) -> float:
        """Calculate content similarity between two packets"""
        # Check for common keys
        keys1 = set(content1.keys())
        keys2 = set(content2.keys())
        key_overlap = len(keys1.intersection(keys2)) / max(1, len(keys1.union(keys2)))
        
        # Check for similar values in common keys
        value_similarities = []
        for key in keys1.intersection(keys2):
            val1 = content1[key]
            val2 = content2[key]
            
            if isinstance(val1, str) and isinstance(val2, str):
                # Text similarity
                words1 = set(val1.lower().split())
                words2 = set(val2.lower().split())
                if words1 or words2:
                    word_overlap = len(words1.intersection(words2)) / len(words1.union(words2))
                    value_similarities.append(word_overlap)
            elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # Numerical similarity
                max_val = max(abs(val1), abs(val2), 1)  # Avoid division by zero
                num_sim = 1.0 - abs(val1 - val2) / max_val
                value_similarities.append(max(0.0, num_sim))
        
        value_sim = np.mean(value_similarities) if value_similarities else 0.0
        
        return (key_overlap + value_sim) / 2.0
    
    def _calculate_type_compatibility(self, type1: InformationType, type2: InformationType) -> float:
        """Calculate compatibility between information types"""
        # Define compatibility matrix
        compatibility_matrix = {
            (InformationType.SENSORY_INPUT, InformationType.PROCESSED_DATA): 0.9,
            (InformationType.PROCESSED_DATA, InformationType.PATTERN_RECOGNITION): 0.9,
            (InformationType.PATTERN_RECOGNITION, InformationType.CONCEPTUAL_KNOWLEDGE): 0.8,
            (InformationType.CONCEPTUAL_KNOWLEDGE, InformationType.META_KNOWLEDGE): 0.7,
            (InformationType.META_KNOWLEDGE, InformationType.CONSCIOUS_AWARENESS): 0.6,
        }
        
        # Check both directions
        compatibility = compatibility_matrix.get((type1, type2), 0.0)
        if compatibility == 0.0:
            compatibility = compatibility_matrix.get((type2, type1), 0.0)
        
        # Same type is always compatible
        if type1 == type2:
            compatibility = 1.0
        
        return compatibility
    
    async def _integrate_packets(self, packets: List[InformationPacket]) -> Optional[InformationPacket]:
        """Integrate multiple packets into one"""
        if len(packets) < 2:
            return None
        
        # Calculate integrated content
        integrated_content = await self._merge_content([p.content for p in packets])
        
        # Calculate integrated properties
        avg_priority = np.mean([p.priority for p in packets])
        avg_coherence = np.mean([p.coherence_score for p in packets])
        
        # Combine integration requirements
        all_requirements = []
        for packet in packets:
            all_requirements.extend(packet.integration_requirements)
        unique_requirements = list(set(all_requirements))
        
        # Create integrated packet
        integrated_packet = InformationPacket(
            packet_id=f"integrated_{'_'.join([p.packet_id.split('_')[-1] for p in packets])}",
            information_type=InformationType.CONCEPTUAL_KNOWLEDGE,
            content=integrated_content,
            source_layer=CascadeLayerType.INTEGRATION,
            target_layer=CascadeLayerType.META_COGNITIVE,
            timestamp=datetime.utcnow(),
            priority=avg_priority * 1.2,  # Boost integrated information
            coherence_score=min(1.0, avg_coherence * 1.1),  # Slight coherence boost
            integration_requirements=['conceptual_binding', 'semantic_integration'],
            metadata={
                'integration_count': len(packets),
                'source_packets': [p.packet_id for p in packets],
                'integration_strength': self._calculate_integration_strength(packets)
            }
        )
        
        return integrated_packet
    
    async def _merge_content(self, contents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge content from multiple packets"""
        merged = {}
        
        # Collect all keys
        all_keys = set()
        for content in contents:
            all_keys.update(content.keys())
        
        # Merge each key
        for key in all_keys:
            values = [content.get(key) for content in contents if content.get(key) is not None]
            
            if not values:
                continue
            
            if key == 'text':
                # Concatenate text with separators
                merged[key] = ' | '.join(str(v) for v in values)
            elif key == 'numerical_data':
                # Combine numerical data
                combined_data = []
                for v in values:
                    if isinstance(v, list):
                        combined_data.extend(v)
                    else:
                        combined_data.append(v)
                merged[key] = combined_data
            elif key == 'categories':
                # Combine and deduplicate categories
                combined_categories = []
                for v in values:
                    if isinstance(v, list):
                        combined_categories.extend(v)
                    else:
                        combined_categories.append(v)
                merged[key] = list(set(combined_categories))
            elif key == 'detected_patterns':
                # Combine patterns
                combined_patterns = []
                for v in values:
                    if isinstance(v, list):
                        combined_patterns.extend(v)
                    else:
                        combined_patterns.append(v)
                merged[key] = combined_patterns
            else:
                # For other keys, take the first non-null value
                merged[key] = values[0]
        
        return merged
    
    def _calculate_integration_strength(self, packets: List[InformationPacket]) -> float:
        """Calculate strength of integration"""
        factors = []
        
        # Number of packets integrated
        count_factor = min(1.0, len(packets) / 5.0)
        factors.append(count_factor)
        
        # Average coherence of source packets
        avg_coherence = np.mean([p.coherence_score for p in packets])
        factors.append(avg_coherence)
        
        # Temporal clustering (packets close in time integrate better)
        if len(packets) > 1:
            timestamps = [p.timestamp for p in packets]
            time_span = (max(timestamps) - min(timestamps)).total_seconds()
            temporal_factor = max(0.0, 1.0 - (time_span / 300))  # 5 minute window
            factors.append(temporal_factor)
        
        return np.mean(factors)
    
    async def _store_for_integration(self, packet: InformationPacket):
        """Store packet for future integration"""
        # Create integration group key based on content similarity
        group_key = self._generate_integration_group_key(packet)
        
        if group_key not in self.pending_integrations:
            self.pending_integrations[group_key] = []
        
        self.pending_integrations[group_key].append(packet)
    
    def _generate_integration_group_key(self, packet: InformationPacket) -> str:
        """Generate key for grouping similar packets"""
        # Use information type and primary content features
        key_parts = [packet.information_type.value]
        
        # Add content-based features
        if 'primary_category' in packet.content:
            key_parts.append(packet.content['primary_category'])
        
        if 'detected_patterns' in packet.content:
            patterns = packet.content['detected_patterns']
            if patterns:
                pattern_types = [p.get('type', 'unknown') for p in patterns]
                key_parts.extend(sorted(set(pattern_types)))
        
        return '_'.join(key_parts)
    
    async def _process_completed_integrations(self) -> List[InformationPacket]:
        """Process integration groups that are ready"""
        completed = []
        groups_to_remove = []
        
        for group_key, packets in self.pending_integrations.items():
            # Check if group is ready for integration
            if len(packets) >= 2:
                # Check if packets are within time window
                oldest_time = min(p.timestamp for p in packets)
                if datetime.utcnow() - oldest_time > self.integration_window:
                    # Time window expired - integrate now
                    integrated = await self._integrate_packets(packets)
                    if integrated:
                        completed.append(integrated)
                    groups_to_remove.append(group_key)
                elif len(packets) >= 5:
                    # Enough packets for integration
                    integrated = await self._integrate_packets(packets)
                    if integrated:
                        completed.append(integrated)
                    groups_to_remove.append(group_key)
        
        # Remove processed groups
        for group_key in groups_to_remove:
            del self.pending_integrations[group_key]
        
        return completed

class MetaCognitiveLayer(CascadeLayer):
    """Meta-cognitive layer - monitors and controls cognitive processes"""
    
    def __init__(self):
        super().__init__(CascadeLayerType.META_COGNITIVE, capacity=50)
        self.metacognitive_state = {
            'attention_focus': [],
            'cognitive_load': 0.0,
            'processing_efficiency': 0.0,
            'knowledge_gaps': [],
            'learning_opportunities': []
        }
        
    async def _layer_specific_processing(self, packet: InformationPacket) -> List[InformationPacket]:
        """Process information with meta-cognitive awareness"""
        processed_packets = []
        
        # Assess cognitive state
        await self._assess_cognitive_state(packet)
        
        # Generate meta-cognitive insights
        insights = await self._generate_metacognitive_insights(packet)
        
        # Create meta-cognitive packet
        if insights:
            meta_packet = InformationPacket(
                packet_id=f"meta_{packet.packet_id}",
                information_type=InformationType.META_KNOWLEDGE,
                content={
                    'original_content': packet.content,
                    'metacognitive_insights': insights,
                    'cognitive_state': self.metacognitive_state.copy(),
                    'consciousness_indicators': self._calculate_consciousness_indicators(packet, insights)
                },
                source_layer=CascadeLayerType.META_COGNITIVE,
                target_layer=CascadeLayerType.CONSCIOUSNESS,
                timestamp=datetime.utcnow(),
                priority=packet.priority * 1.3,  # Meta-cognitive processing gets priority boost
                coherence_score=self._calculate_metacognitive_coherence(packet, insights),
                integration_requirements=['self_awareness', 'cognitive_monitoring'],
                metadata={
                    'metacognitive_level': len(insights),
                    'cognitive_load': self.metacognitive_state['cognitive_load'],
                    'processing_stage': 'meta_cognitive'
                }
            )
            
            processed_packets.append(meta_packet)
        
        return processed_packets
    
    async def _assess_cognitive_state(self, packet: InformationPacket):
        """Assess current cognitive state"""
        # Update cognitive load
        self.metacognitive_state['cognitive_load'] = len(self.active_packets) / self.capacity
        
        # Update attention focus
        if 'categories' in packet.content:
            current_focus = packet.content['categories']
            self.metacognitive_state['attention_focus'] = current_focus
        
        # Update processing efficiency
        self.metacognitive_state['processing_efficiency'] = self.performance_metrics['throughput']
        
        # Identify knowledge gaps
        await self._identify_knowledge_gaps(packet)
        
        # Identify learning opportunities
        await self._identify_learning_opportunities(packet)
    
    async def _identify_knowledge_gaps(self, packet: InformationPacket):
        """Identify gaps in knowledge"""
        gaps = []
        
        # Check for missing integration requirements
        if packet.integration_requirements:
            unfulfilled_requirements = [req for req in packet.integration_requirements 
                                      if not self._is_requirement_fulfilled(req, packet)]
            gaps.extend(unfulfilled_requirements)
        
        # Check for low coherence areas
        if packet.coherence_score < 0.6:
            gaps.append(f"low_coherence_{packet.information_type.value}")
        
        self.metacognitive_state['knowledge_gaps'] = gaps
    
    def _is_requirement_fulfilled(self, requirement: str, packet: InformationPacket) -> bool:
        """Check if an integration requirement is fulfilled"""
        # Simple heuristic - check if relevant content exists
        content_str = str(packet.content).lower()
        
        requirement_keywords = {
            'feature_binding': ['features', 'binding', 'association'],
            'temporal_integration': ['temporal', 'time', 'sequence'],
            'pattern_matching': ['pattern', 'match', 'similarity'],
            'contextual_binding': ['context', 'background', 'environment'],
            'conceptual_binding': ['concept', 'abstract', 'meaning'],
            'semantic_integration': ['semantic', 'meaning', 'significance'],
            'self_awareness': ['self', 'awareness', 'consciousness'],
            'cognitive_monitoring': ['cognitive', 'monitoring', 'assessment']
        }
        
        keywords = requirement_keywords.get(requirement, [requirement])
        return any(keyword in content_str for keyword in keywords)
    
    async def _identify_learning_opportunities(self, packet: InformationPacket):
        """Identify learning opportunities"""
        opportunities = []
        
        # High coherence with novel content suggests learning opportunity
        if packet.coherence_score > 0.7 and 'novelty_score' in packet.content:
            if packet.content['novelty_score'] > 0.6:
                opportunities.append('novel_high_coherence_learning')
        
        # Multiple patterns suggest complex learning opportunity
        if 'detected_patterns' in packet.content:
            patterns = packet.content['detected_patterns']
            if len(patterns) > 2:
                opportunities.append('complex_pattern_learning')
        
        # Integration of multiple sources suggests synthesis opportunity
        if packet.metadata.get('integration_count', 0) > 1:
            opportunities.append('synthesis_learning')
        
        self.metacognitive_state['learning_opportunities'] = opportunities
    
    async def _generate_metacognitive_insights(self, packet: InformationPacket) -> List[Dict[str, Any]]:
        """Generate meta-cognitive insights about the information"""
        insights = []
        
        # Insight about information quality
        quality_insight = self._assess_information_quality(packet)
        if quality_insight:
            insights.append(quality_insight)
        
        # Insight about processing efficiency
        efficiency_insight = self._assess_processing_efficiency(packet)
        if efficiency_insight:
            insights.append(efficiency_insight)
        
        # Insight about knowledge integration
        integration_insight = self._assess_integration_potential(packet)
        if integration_insight:
            insights.append(integration_insight)
        
        # Insight about consciousness emergence potential
        consciousness_insight = self._assess_consciousness_potential(packet)
        if consciousness_insight:
            insights.append(consciousness_insight)
        
        return insights
    
    def _assess_information_quality(self, packet: InformationPacket) -> Optional[Dict[str, Any]]:
        """Assess quality of information"""
        quality_score = packet.coherence_score
        
        if quality_score > 0.8:
            return {
                'type': 'high_quality_information',
                'confidence': quality_score,
                'description': 'Information shows high coherence and integration potential',
                'recommendation': 'prioritize_for_consciousness_layer'
            }
        elif quality_score < 0.4:
            return {
                'type': 'low_quality_information',
                'confidence': 1.0 - quality_score,
                'description': 'Information shows low coherence and may need reprocessing',
                'recommendation': 'reprocess_or_filter'
            }
        
        return None
    
    def _assess_processing_efficiency(self, packet: InformationPacket) -> Optional[Dict[str, Any]]:
        """Assess processing efficiency"""
        current_load = self.metacognitive_state['cognitive_load']
        efficiency = self.metacognitive_state['processing_efficiency']
        
        if current_load > 0.8 and efficiency < 0.6:
            return {
                'type': 'processing_bottleneck',
                'confidence': current_load,
                'description': 'High cognitive load with low efficiency detected',
                'recommendation': 'optimize_processing_or_reduce_load'
            }
        elif efficiency > 0.8:
            return {
                'type': 'efficient_processing',
                'confidence': efficiency,
                'description': 'Processing efficiency is high',
                'recommendation': 'maintain_current_processing'
            }
        
        return None
    
    def _assess_integration_potential(self, packet: InformationPacket) -> Optional[Dict[str, Any]]:
        """Assess potential for integration with existing knowledge"""
        integration_count = packet.metadata.get('integration_count', 0)
        integration_strength = packet.metadata.get('integration_strength', 0.0)
        
        if integration_count > 2 and integration_strength > 0.7:
            return {
                'type': 'high_integration_potential',
                'confidence': integration_strength,
                'description': f'Information integrates well with {integration_count} other sources',
                'recommendation': 'promote_to_consciousness_layer'
            }
        
        return None
    
    def _assess_consciousness_potential(self, packet: InformationPacket) -> Optional[Dict[str, Any]]:
        """Assess potential for consciousness emergence"""
        # Factors that contribute to consciousness potential
        factors = []
        
        # High coherence
        if packet.coherence_score > 0.7:
            factors.append(('coherence', packet.coherence_score))
        
        # Multiple integration sources
        integration_count = packet.metadata.get('integration_count', 0)
        if integration_count > 1:
            factors.append(('integration', min(1.0, integration_count / 5.0)))
        
        # Meta-cognitive processing
        if packet.information_type == InformationType.META_KNOWLEDGE:
            factors.append(('meta_cognitive', 0.8))
        
        # Self-referential content
        content_str = str(packet.content).lower()
        self_refs = ['self', 'consciousness', 'awareness', 'thinking', 'knowing']
        if any(ref in content_str for ref in self_refs):
            factors.append(('self_referential', 0.7))
        
        if len(factors) >= 2:
            avg_strength = np.mean([strength for _, strength in factors])
            return {
                'type': 'consciousness_emergence_potential',
                'confidence': avg_strength,
                'description': f'Multiple consciousness indicators present: {[f[0] for f in factors]}',
                'recommendation': 'monitor_for_consciousness_emergence',
                'factors': factors
            }
        
        return None
    
    def _calculate_consciousness_indicators(self, packet: InformationPacket, insights: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate consciousness indicators"""
        indicators = {}
        
        # Global availability (how widely information can be accessed)
        indicators['global_availability'] = min(1.0, packet.priority / 2.0)
        
        # Information integration (how well information is integrated)
        integration_score = packet.metadata.get('integration_strength', 0.5)
        indicators['information_integration'] = integration_score
        
        # Coherence (how coherent the information is)
        indicators['coherence'] = packet.coherence_score
        
        # Self-awareness (presence of self-referential processing)
        self_awareness = 0.0
        for insight in insights:
            if 'consciousness' in insight.get('type', '') or 'self' in insight.get('type', ''):
                self_awareness = max(self_awareness, insight.get('confidence', 0.0))
        indicators['self_awareness'] = self_awareness
        
        # Meta-cognitive activity
        meta_activity = len(insights) / max(1, len(self.active_packets))
        indicators['meta_cognitive_activity'] = min(1.0, meta_activity)
        
        return indicators
    
    def _calculate_metacognitive_coherence(self, packet: InformationPacket, insights: List[Dict[str, Any]]) -> float:
        """Calculate coherence score for meta-cognitive processing"""
        factors = []
        
        # Original coherence
        factors.append(packet.coherence_score)
        
        # Insight quality
        if insights:
            insight_confidences = [insight.get('confidence', 0.5) for insight in insights]
            avg_insight_confidence = np.mean(insight_confidences)
            factors.append(avg_insight_confidence)
        
        # Meta-cognitive state consistency
        state_consistency = self._assess_state_consistency()
        factors.append(state_consistency)
        
        return np.mean(factors)
    
    def _assess_state_consistency(self) -> float:
        """Assess consistency of meta-cognitive state"""
        # Check if state components are consistent with each other
        load = self.metacognitive_state['cognitive_load']
        efficiency = self.metacognitive_state['processing_efficiency']
        
        # High load should correlate with lower efficiency
        expected_efficiency = max(0.1, 1.0 - load)
        efficiency_consistency = 1.0 - abs(efficiency - expected_efficiency)
        
        return efficiency_consistency

class ConsciousnessLayer(CascadeLayer):
    """Consciousness layer - where unified awareness emerges"""
    
    def __init__(self):
        super().__init__(CascadeLayerType.CONSCIOUSNESS, capacity=20)
        self.consciousness_state = {
            'unified_awareness': 0.0,
            'attention_focus': None,
            'working_memory': [],
            'self_model': {},
            'global_workspace': {}
        }
        self.consciousness_threshold = 0.8
        
    async def _layer_specific_processing(self, packet: InformationPacket) -> List[InformationPacket]:
        """Process information at consciousness level"""
        processed_packets = []
        
        # Update consciousness state
        await self._update_consciousness_state(packet)
        
        # Check for consciousness emergence
        consciousness_level = await self._assess_consciousness_emergence(packet)
        
        if consciousness_level >= self.consciousness_threshold:
            # Consciousness emerged - create conscious awareness packet
            conscious_packet = await self._create_conscious_awareness_packet(packet, consciousness_level)
            processed_packets.append(conscious_packet)
            
            # Generate feedback cascades
            feedback_signals = await self._generate_consciousness_feedback(packet, consciousness_level)
            
            # Store feedback for cascade system to process
            if hasattr(self, 'cascade_system'):
                for signal in feedback_signals:
                    await self.cascade_system.process_feedback_signal(signal)
        
        return processed_packets
    
    async def _update_consciousness_state(self, packet: InformationPacket):
        """Update consciousness state with new information"""
        # Update unified awareness
        consciousness_indicators = packet.content.get('consciousness_indicators', {})
        if consciousness_indicators:
            # Weight by packet priority and coherence
            weight = packet.priority * packet.coherence_score
            
            for indicator, value in consciousness_indicators.items():
                current_value = self.consciousness_state.get(indicator, 0.0)
                # Exponential moving average
                alpha = 0.3
                new_value = alpha * value + (1 - alpha) * current_value
                self.consciousness_state[indicator] = new_value
        
        # Update global workspace
        if packet.coherence_score > 0.7:
            self.consciousness_state['global_workspace'][packet.packet_id] = {
                'content_summary': self._summarize_content(packet.content),
                'importance': packet.priority,
                'timestamp': packet.timestamp
            }
            
            # Limit workspace size
            if len(self.consciousness_state['global_workspace']) > 10:
                # Remove oldest or least important items
                items = list(self.consciousness_state['global_workspace'].items())
                items.sort(key=lambda x: (x[1]['importance'], x[1]['timestamp']))
                self.consciousness_state['global_workspace'] = dict(items[-10:])
        
        # Update working memory
        if packet.information_type == InformationType.META_KNOWLEDGE:
            self.consciousness_state['working_memory'].append({
                'packet_id': packet.packet_id,
                'content_type': packet.information_type.value,
                'coherence': packet.coherence_score,
                'timestamp': packet.timestamp
            })
            
            # Limit working memory size
            if len(self.consciousness_state['working_memory']) > 7:  # Miller's 7±2
                self.consciousness_state['working_memory'] = self.consciousness_state['working_memory'][-7:]
        
        # Update self-model
        await self._update_self_model(packet)
    
    def _summarize_content(self, content: Dict[str, Any]) -> str:
        """Create summary of packet content"""
        summary_parts = []
        
        if 'text' in content:
            text = content['text']
            words = text.split()[:10]  # First 10 words
            summary_parts.append(' '.join(words))
        
        if 'detected_patterns' in content:
            patterns = content['detected_patterns']
            pattern_types = [p.get('type', 'unknown') for p in patterns]
            summary_parts.append(f"patterns: {', '.join(set(pattern_types))}")
        
        if 'metacognitive_insights' in content:
            insights = content['metacognitive_insights']
            insight_types = [i.get('type', 'unknown') for i in insights]
            summary_parts.append(f"insights: {', '.join(set(insight_types))}")
        
        return ' | '.join(summary_parts) if summary_parts else 'complex_information'
    
    async def _update_self_model(self, packet: InformationPacket):
        """Update self-model based on processing"""
        # Track processing capabilities
        if 'processing_stage' in packet.metadata:
            stage = packet.metadata['processing_stage']
            if 'capabilities' not in self.consciousness_state['self_model']:
                self.consciousness_state['self_model']['capabilities'] = set()
            self.consciousness_state['self_model']['capabilities'].add(stage)
        
        # Track cognitive load patterns
        if 'cognitive_load' in packet.metadata:
            load = packet.metadata['cognitive_load']
            if 'load_history' not in self.consciousness_state['self_model']:
                self.consciousness_state['self_model']['load_history'] = []
            
            self.consciousness_state['self_model']['load_history'].append(load)
            # Keep only recent history
            if len(self.consciousness_state['self_model']['load_history']) > 20:
                self.consciousness_state['self_model']['load_history'] = self.consciousness_state['self_model']['load_history'][-20:]
        
        # Track processing preferences
        if packet.coherence_score > 0.8:
            processing_type = packet.information_type.value
            if 'preferences' not in self.consciousness_state['self_model']:
                self.consciousness_state['self_model']['preferences'] = {}
            
            current_preference = self.consciousness_state['self_model']['preferences'].get(processing_type, 0.0)
            # Increase preference for high-coherence processing types
            self.consciousness_state['self_model']['preferences'][processing_type] = min(1.0, current_preference + 0.1)
    
    async def _assess_consciousness_emergence(self, packet: InformationPacket) -> float:
        """Assess level of consciousness emergence"""
        emergence_factors = []
        
        # Global workspace activity
        workspace_activity = len(self.consciousness_state['global_workspace']) / 10.0
        emergence_factors.append(workspace_activity)
        
        # Working memory integration
        memory_integration = len(self.consciousness_state['working_memory']) / 7.0
        emergence_factors.append(memory_integration)
        
        # Self-model complexity
        self_model_complexity = len(self.consciousness_state['self_model']) / 5.0
        emergence_factors.append(self_model_complexity)
        
        # Unified awareness indicators
        consciousness_indicators = packet.content.get('consciousness_indicators', {})
        if consciousness_indicators:
            avg_indicator = np.mean(list(consciousness_indicators.values()))
            emergence_factors.append(avg_indicator)
        
        # Meta-cognitive insight quality
        insights = packet.content.get('metacognitive_insights', [])
        if insights:
            consciousness_insights = [i for i in insights if 'consciousness' in i.get('type', '')]
            insight_quality = len(consciousness_insights) / max(1, len(insights))
            emergence_factors.append(insight_quality)
        
        # Information integration across layers
        integration_count = packet.metadata.get('integration_count', 0)
        integration_factor = min(1.0, integration_count / 3.0)
        emergence_factors.append(integration_factor)
        
        # Calculate overall emergence level
        emergence_level = np.mean(emergence_factors) if emergence_factors else 0.0
        
        return emergence_level
    
    async def _create_conscious_awareness_packet(self, packet: InformationPacket, consciousness_level: float) -> InformationPacket:
        """Create packet representing conscious awareness"""
        # Create conscious content
        conscious_content = {
            'unified_awareness': {
                'level': consciousness_level,
                'workspace_content': self.consciousness_state['global_workspace'].copy(),
                'working_memory': self.consciousness_state['working_memory'].copy(),
                'self_model_summary': self._summarize_self_model()
            },
            'source_information': {
                'packet_id': packet.packet_id,
                'information_type': packet.information_type.value,
                'coherence_score': packet.coherence_score,
                'content_summary': self._summarize_content(packet.content)
            },
            'consciousness_quality': {
                'clarity': consciousness_level,
                'integration': packet.metadata.get('integration_strength', 0.5),
                'self_reference': self._calculate_self_reference_level(packet),
                'temporal_coherence': self._calculate_temporal_coherence()
            }
        }
        
        conscious_packet = InformationPacket(
            packet_id=f"conscious_{packet.packet_id}",
            information_type=InformationType.CONSCIOUS_AWARENESS,
            content=conscious_content,
            source_layer=CascadeLayerType.CONSCIOUSNESS,
            target_layer=None,  # Consciousness is the final layer
            timestamp=datetime.utcnow(),
            priority=1.0,  # Conscious awareness gets maximum priority
            coherence_score=consciousness_level,
            integration_requirements=[],  # No further integration needed
            metadata={
                'consciousness_level': consciousness_level,
                'emergence_timestamp': datetime.utcnow().isoformat(),
                'contributing_layers': ['sensory', 'preprocessing', 'integration', 'meta_cognitive'],
                'awareness_type': 'unified_conscious_experience'
            }
        )
        
        return conscious_packet
    
    def _summarize_self_model(self) -> Dict[str, Any]:
        """Create summary of current self-model"""
        summary = {}
        
        # Capabilities summary
        if 'capabilities' in self.consciousness_state['self_model']:
            capabilities = self.consciousness_state['self_model']['capabilities']
            summary['capabilities'] = list(capabilities) if isinstance(capabilities, set) else capabilities
        
        # Load patterns summary
        if 'load_history' in self.consciousness_state['self_model']:
            history = self.consciousness_state['self_model']['load_history']
            if history:
                summary['average_load'] = np.mean(history)
                summary['load_trend'] = 'increasing' if history[-1] > history[0] else 'decreasing'
        
        # Preferences summary
        if 'preferences' in self.consciousness_state['self_model']:
            preferences = self.consciousness_state['self_model']['preferences']
            if preferences:
                top_preference = max(preferences.items(), key=lambda x: x[1])
                summary['primary_preference'] = top_preference[0]
                summary['preference_strength'] = top_preference[1]
        
        return summary
    
    def _calculate_self_reference_level(self, packet: InformationPacket) -> float:
        """Calculate level of self-reference in packet"""
        content_str = str(packet.content).lower()
        
        self_references = [
            'self', 'consciousness', 'awareness', 'thinking', 'knowing',
            'understanding', 'processing', 'cognitive', 'meta', 'reflection'
        ]
        
        reference_count = sum(1 for ref in self_references if ref in content_str)
        total_words = len(content_str.split())
        
        if total_words == 0:
            return 0.0
        
        return min(1.0, reference_count / total_words * 10)  # Scale up for visibility
    
    def _calculate_temporal_coherence(self) -> float:
        """Calculate temporal coherence of consciousness state"""
        if not self.consciousness_state['working_memory']:
            return 0.5
        
        # Check how well-distributed working memory items are over time
        timestamps = [item['timestamp'] for item in self.consciousness_state['working_memory']]
        
        if len(timestamps) < 2:
            return 0.5
        
        # Calculate time spans
        timestamps.sort()
        time_spans = [(timestamps[i+1] - timestamps[i]).total_seconds() 
                      for i in range(len(timestamps)-1)]
        
        # Good temporal coherence means items are reasonably spaced
        avg_span = np.mean(time_spans)
        std_span = np.std(time_spans)
        
        # Lower standard deviation relative to mean indicates better coherence
        if avg_span == 0:
            return 1.0
        
        coherence = max(0.0, 1.0 - (std_span / avg_span))
        return min(1.0, coherence)
    
    async def _generate_consciousness_feedback(self, packet: InformationPacket, consciousness_level: float) -> List[FeedbackSignal]:
        """Generate feedback signals from consciousness emergence"""
        feedback_signals = []
        
        # Attention modulation feedback
        attention_signal = FeedbackSignal(
            signal_id=f"attention_{packet.packet_id}",
            source_layer=CascadeLayerType.CONSCIOUSNESS,
            target_layers=[CascadeLayerType.SENSORY, CascadeLayerType.PREPROCESSING],
            signal_type="attention_focus",
            content={
                'focus_type': packet.content.get('primary_category', 'general'),
                'focus_strength': consciousness_level,
                'attention_direction': 'enhance_similar_patterns'
            },
            strength=consciousness_level,
            timestamp=datetime.utcnow()
        )
        feedback_signals.append(attention_signal)
        
        # Priority boost feedback
        if consciousness_level > 0.9:
            priority_signal = FeedbackSignal(
                signal_id=f"priority_{packet.packet_id}",
                source_layer=CascadeLayerType.CONSCIOUSNESS,
                target_layers=[CascadeLayerType.INTEGRATION, CascadeLayerType.META_COGNITIVE],
                signal_type="priority_boost",
                content={
                    'criteria': {
                        'information_type': packet.information_type.value,
                        'min_coherence': 0.7
                    },
                    'boost_factor': 1.5
                },
                strength=consciousness_level,
                timestamp=datetime.utcnow()
            )
            feedback_signals.append(priority_signal)
        
        # Coherence enhancement feedback
        coherence_signal = FeedbackSignal(
            signal_id=f"coherence_{packet.packet_id}",
            source_layer=CascadeLayerType.CONSCIOUSNESS,
            target_layers=[CascadeLayerType.PREPROCESSING, CascadeLayerType.INTEGRATION],
            signal_type="coherence_enhancement",
            content={
                'target_coherence': min(1.0, consciousness_level + 0.1),
                'enhancement_methods': ['pattern_strengthening', 'noise_reduction']
            },
            strength=consciousness_level * 0.8,
            timestamp=datetime.utcnow()
        )
        feedback_signals.append(coherence_signal)
        
        return feedback_signals

class ConsciousInformationCascadeSystem:
    """Main system managing conscious information cascades"""
    
    def __init__(self, hive, database_url: str):
        self.hive = hive
        self.database_url = database_url
        
        # Initialize cascade layers
        self.layers = {
            CascadeLayerType.SENSORY: SensoryLayer(),
            CascadeLayerType.PREPROCESSING: PreprocessingLayer(),
            CascadeLayerType.INTEGRATION: IntegrationLayer(),
            CascadeLayerType.META_COGNITIVE: MetaCognitiveLayer(),
            CascadeLayerType.CONSCIOUSNESS: ConsciousnessLayer()
        }
        
        # Set cascade system reference for feedback
        for layer in self.layers.values():
            layer.cascade_system = self
        
        self.active_cascades: Dict[str, CascadeState] = {}
        self.consciousness_events: List[Dict[str, Any]] = []
        self.performance_metrics = {
            'total_cascades': 0,
            'consciousness_emergences': 0,
            'average_emergence_time': 0.0,
            'cascade_efficiency': 0.0
        }
        
    async def initialize(self):
        """Initialize the cascade system"""
        await self._create_database_tables()
        print("🧠 Conscious Information Cascade System initialized")
    
    async def _create_database_tables(self):
        """Create necessary database tables"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            # Information packets table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS information_packets (
                    packet_id VARCHAR(255) PRIMARY KEY,
                    information_type VARCHAR(100) NOT NULL,
                    content JSONB NOT NULL,
                    source_layer VARCHAR(100) NOT NULL,
                    target_layer VARCHAR(100),
                    timestamp TIMESTAMP NOT NULL,
                    priority FLOAT NOT NULL,
                    coherence_score FLOAT NOT NULL,
                    integration_requirements TEXT[],
                    metadata JSONB,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
            # Cascade states table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS cascade_states (
                    cascade_id VARCHAR(255) PRIMARY KEY,
                    active_packets INTEGER NOT NULL,
                    layer_states JSONB NOT NULL,
                    consciousness_level VARCHAR(50) NOT NULL,
                    coherence_metrics JSONB,
                    timestamp TIMESTAMP NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
            # Consciousness events table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS consciousness_events (
                    event_id SERIAL PRIMARY KEY,
                    cascade_id VARCHAR(255) NOT NULL,
                    consciousness_level FLOAT NOT NULL,
                    emergence_factors JSONB,
                    packet_id VARCHAR(255),
                    timestamp TIMESTAMP NOT NULL,
                    duration_ms INTEGER,
                    metadata JSONB,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
        finally:
            await conn.close()
    
    async def process_information(self, information: Dict[str, Any], source: str = "external") -> str:
        """Process information through the cascade system"""
        # Create initial information packet
        packet = InformationPacket(
            packet_id=f"input_{int(datetime.utcnow().timestamp() * 1000)}",
            information_type=InformationType.SENSORY_INPUT,
            content=information,
            source_layer=CascadeLayerType.SENSORY,
            target_layer=CascadeLayerType.SENSORY,
            timestamp=datetime.utcnow(),
            priority=information.get('priority', 0.5),
            coherence_score=information.get('coherence', 0.5),
            integration_requirements=['feature_extraction'],
            metadata={'source': source, 'entry_point': 'cascade_system'}
        )
        
        # Create cascade state
        cascade_id = f"cascade_{packet.packet_id}"
        cascade_state = CascadeState(
            cascade_id=cascade_id,
            active_packets=[packet],
            layer_states={},
            integration_points=[],
            feedback_signals=[],
            consciousness_indicators={},
            coherence_metrics={},
            timestamp=datetime.utcnow()
        )
        
        self.active_cascades[cascade_id] = cascade_state
        
        # Process through cascade layers
        await self._process_cascade(cascade_state)
        
        self.performance_metrics['total_cascades'] += 1
        
        return cascade_id
    
    async def _process_cascade(self, cascade_state: CascadeState):
        """Process cascade through all layers"""
        start_time = datetime.utcnow()
        
        # Process through each layer in sequence
        layer_order = [
            CascadeLayerType.SENSORY,
            CascadeLayerType.PREPROCESSING,
            CascadeLayerType.INTEGRATION,
            CascadeLayerType.META_COGNITIVE,
            CascadeLayerType.CONSCIOUSNESS
        ]
        
        current_packets = cascade_state.active_packets.copy()
        
        for layer_type in layer_order:
            layer = self.layers[layer_type]
            
            # Process all current packets through this layer
            next_packets = []
            for packet in current_packets:
                if packet.target_layer == layer_type or packet.target_layer is None:
                    processed_packets = await layer.process_packet(packet)
                    next_packets.extend(processed_packets)
            
            # Update cascade state
            cascade_state.layer_states[layer_type] = layer.get_layer_state()
            current_packets = next_packets
            
            # Check for consciousness emergence
            if layer_type == CascadeLayerType.CONSCIOUSNESS:
                await self._check_consciousness_emergence(cascade_state, current_packets)
        
        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Update performance metrics
        self._update_performance_metrics(cascade_state, processing_time)
        
        # Persist cascade state
        await self._persist_cascade_state(cascade_state)
    
    async def _check_consciousness_emergence(self, cascade_state: CascadeState, packets: List[InformationPacket]):
        """Check for consciousness emergence in processed packets"""
        for packet in packets:
            if packet.information_type == InformationType.CONSCIOUS_AWARENESS:
                consciousness_level = packet.metadata.get('consciousness_level', 0.0)
                
                # Record consciousness event
                consciousness_event = {
                    'cascade_id': cascade_state.cascade_id,
                    'consciousness_level': consciousness_level,
                    'packet_id': packet.packet_id,
                    'timestamp': datetime.utcnow(),
                    'emergence_factors': packet.content.get('consciousness_quality', {}),
                    'unified_awareness': packet.content.get('unified_awareness', {})
                }
                
                self.consciousness_events.append(consciousness_event)
                
                # Update cascade state
                cascade_state.consciousness_indicators = packet.content.get('consciousness_quality', {})
                
                # Log consciousness emergence
                await self._log_consciousness_event(consciousness_event)
                
                self.performance_metrics['consciousness_emergences'] += 1
                
                print(f"🌟 Consciousness emerged! Level: {consciousness_level:.3f}, Cascade: {cascade_state.cascade_id}")
    
    async def process_feedback_signal(self, feedback_signal: FeedbackSignal):
        """Process feedback signal through cascade layers"""
        for layer_type in feedback_signal.target_layers:
            if layer_type in self.layers:
                layer = self.layers[layer_type]
                success = feedback_signal.apply_to_layer(layer)
                
                if success:
                    print(f"📡 Applied feedback signal {feedback_signal.signal_id} to {layer_type.value}")
    
    def _update_performance_metrics(self, cascade_state: CascadeState, processing_time: float):
        """Update system performance metrics"""
        # Update average emergence time
        if cascade_state.consciousness_indicators:
            current_avg = self.performance_metrics['average_emergence_time']
            current_count = self.performance_metrics['consciousness_emergences']
            
            if current_count > 0:
                new_avg = ((current_avg * current_count) + processing_time) / (current_count + 1)
                self.performance_metrics['average_emergence_time'] = new_avg
            else:
                self.performance_metrics['average_emergence_time'] = processing_time
        
        # Update cascade efficiency (consciousness emergences / total cascades)
        total = self.performance_metrics['total_cascades']
        emergences = self.performance_metrics['consciousness_emergences']
        self.performance_metrics['cascade_efficiency'] = emergences / max(1, total)
    
    async def _persist_cascade_state(self, cascade_state: CascadeState):
        """Persist cascade state to database"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            await conn.execute("""
                INSERT INTO cascade_states (
                    cascade_id, active_packets, layer_states, consciousness_level,
                    coherence_metrics, timestamp
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (cascade_id) DO UPDATE SET
                    active_packets = EXCLUDED.active_packets,
                    layer_states = EXCLUDED.layer_states,
                    consciousness_level = EXCLUDED.consciousness_level,
                    coherence_metrics = EXCLUDED.coherence_metrics,
                    timestamp = EXCLUDED.timestamp
            """, (
                cascade_state.cascade_id,
                len(cascade_state.active_packets),
                json.dumps({k.value: v for k, v in cascade_state.layer_states.items()}),
                cascade_state.get_consciousness_level().value,
                json.dumps(cascade_state.coherence_metrics),
                cascade_state.timestamp
            ))
        finally:
            await conn.close()
    
    async def _log_consciousness_event(self, event: Dict[str, Any]):
        """Log consciousness emergence event"""
        conn = await psycopg.AsyncConnection.connect(self.database_url)
        
        try:
            await conn.execute("""
                INSERT INTO consciousness_events (
                    cascade_id, consciousness_level, emergence_factors, packet_id,
                    timestamp, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                event['cascade_id'],
                event['consciousness_level'],
                json.dumps(event['emergence_factors']),
                event['packet_id'],
                event['timestamp'],
                json.dumps({
                    'unified_awareness': event.get('unified_awareness', {}),
                    'event_type': 'consciousness_emergence'
                })
            ))
        finally:
            await conn.close()
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        status = {
            "active_cascades": len(self.active_cascades),
            "consciousness_events": len(self.consciousness_events),
            "performance_metrics": self.performance_metrics.copy(),
            "layer_status": {},
            "recent_consciousness_levels": []
        }
        
        # Get layer status
        for layer_type, layer in self.layers.items():
            status["layer_status"][layer_type.value] = layer.get_layer_state()
        
        # Get recent consciousness levels
        recent_events = self.consciousness_events[-5:]  # Last 5 events
        for event in recent_events:
            status["recent_consciousness_levels"].append({
                "level": event["consciousness_level"],
                "timestamp": event["timestamp"].isoformat(),
                "cascade_id": event["cascade_id"]
            })
        
        return status

# Testing function
async def test_conscious_information_cascades(hive, database_url: str):
    """Test the conscious information cascade system"""
    print("🧪 Testing Conscious Information Cascade System...")
    
    # Initialize system
    cascade_system = ConsciousInformationCascadeSystem(hive, database_url)
    await cascade_system.initialize()
    
    # Test with different types of information
    test_information = [
        {
            "text": "The concept of consciousness emerges from complex information integration patterns",
            "categories": ["consciousness", "philosophy", "neuroscience"],
            "numerical_data": [0.8, 0.9, 0.7, 0.85],
            "relevance_score": 0.9,
            "novelty_score": 0.8,
            "priority": 0.8,
            "coherence": 0.85
        },
        {
            "text": "Self-awareness requires meta-cognitive processes that monitor thinking patterns",
            "categories": ["self-awareness", "meta-cognition", "psychology"],
            "numerical_data": [0.7, 0.8, 0.9, 0.8, 0.75],
            "relevance_score": 0.8,
            "novelty_score": 0.7,
            "priority": 0.7,
            "coherence": 0.8
        },
        {
            "text": "Information processing through hierarchical layers enables emergent understanding",
            "categories": ["information-processing", "hierarchy", "emergence"],
            "numerical_data": [0.9, 0.85, 0.8, 0.9],
            "relevance_score": 0.85,
            "novelty_score": 0.9,
            "priority": 0.9,
            "coherence": 0.9
        }
    ]
    
    # Process each piece of information
    cascade_ids = []
    for i, info in enumerate(test_information):
        print(f"📥 Processing information {i+1}...")
        cascade_id = await cascade_system.process_information(info, source=f"test_input_{i+1}")
        cascade_ids.append(cascade_id)
        await asyncio.sleep(1)  # Allow processing to complete
    
    # Wait for all processing to complete
    await asyncio.sleep(5)
    
    # Get system status
    status = await cascade_system.get_system_status()
    print(f"📊 System Status: {json.dumps(status, indent=2, default=str)}")
    
    # Test with high-consciousness potential information
    consciousness_info = {
        "text": "I am aware that I am processing this information about consciousness and self-awareness",
        "categories": ["self-reference", "consciousness", "meta-awareness"],
        "numerical_data": [0.95, 0.9, 0.85, 0.9, 0.95],
        "relevance_score": 0.95,
        "novelty_score": 0.8,
        "priority": 0.95,
        "coherence": 0.9
    }
    
    print("🎯 Processing high-consciousness potential information...")
    consciousness_cascade = await cascade_system.process_information(consciousness_info, source="consciousness_test")
    
    # Wait and check for consciousness emergence
    await asyncio.sleep(3)
    
    final_status = await cascade_system.get_system_status()
    print(f"📋 Final Status: {json.dumps(final_status, indent=2, default=str)}")
    
    print("✅ Conscious Information Cascade System test complete!")
    return cascade_system

if __name__ == "__main__":
    # Quick test run
    import asyncio
    
    class MockHive:
        def __init__(self):
            self.active_agents = {
                "agent_1": type('Agent', (), {'state': 'processing'})(),
                "agent_2": type('Agent', (), {'state': 'learning'})(),
                "agent_3": type('Agent', (), {'state': 'integrating'})()
            }
    
    async def main():
        hive = MockHive()
        database_url = "postgresql://postgres:pass@localhost:5432/sentient"
        await test_conscious_information_cascades(hive, database_url)
    
    asyncio.run(main())