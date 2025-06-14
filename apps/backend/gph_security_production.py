"""
Genesis Prime Input Validation System
====================================

Production input validation and processing system for Genesis Prime consciousness framework.
Ensures data integrity and system stability through comprehensive input analysis.

Author: Genesis Prime Development Team
License: MIT (Open Source Consciousness)
"""

import asyncio
import re
import json
import hashlib
import unicodedata
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum
import logging

try:
    import psycopg
    import numpy as np
except ImportError:
    # Graceful fallback for missing dependencies
    class psycopg:
        @staticmethod
        def connect(url): pass
        
        class AsyncConnection:
            @staticmethod
            async def connect(url): pass
    
    class np:
        @staticmethod
        def array(x): return x
        @staticmethod
        def std(x): return 0.5
        @staticmethod
        def mean(x): return sum(x) / len(x) if x else 0

# Configure logging
logger = logging.getLogger(__name__)

class ValidationLevel(Enum):
    """Input validation levels"""
    PASS = "pass"
    PROCESS = "process"
    REVIEW = "review"
    FILTER = "filter"

class ProcessingResult(Enum):
    """Processing outcomes"""
    APPROVED = "approved"
    CLEANED = "cleaned"
    QUEUED = "queued"
    DECLINED = "declined"

@dataclass
class InputAnalysis:
    """Analysis result for input content"""
    content_hash: str
    analysis_timestamp: datetime
    validation_level: ValidationLevel
    processing_result: ProcessingResult
    confidence_score: float
    cleaned_content: Optional[str]
    quality_metrics: Dict[str, float]
    processing_notes: List[str]

class TextNormalizer:
    """Normalizes and cleans text input for processing"""
    
    def __init__(self):
        # Character categories for normalization
        self.format_chars = {
            'Cf',  # Format characters
            'Cc',  # Control characters
        }
        
        # Replacement mappings for problematic characters
        self.char_replacements = {
            '\u200B': '',      # Zero Width Space
            '\u200C': '',      # Zero Width Non-Joiner
            '\u200D': '',      # Zero Width Joiner
            '\u2060': '',      # Word Joiner
            '\uFEFF': '',      # Zero Width No-Break Space
            '\u034F': '',      # Combining Grapheme Joiner
            '\u180E': ' ',     # Mongolian Vowel Separator
        }
        
        # Bidirectional text markers
        self.bidi_chars = {
            '\u202A', '\u202B', '\u202C', '\u202D', '\u202E',
            '\u2066', '\u2067', '\u2068', '\u2069'
        }
        
    async def normalize_text(self, text: str) -> str:
        """Normalize text for consistent processing"""
        if not text:
            return text
            
        # Apply Unicode normalization
        normalized = unicodedata.normalize('NFKC', text)
        
        # Remove/replace problematic characters
        cleaned = ""
        for char in normalized:
            if char in self.char_replacements:
                cleaned += self.char_replacements[char]
            elif char in self.bidi_chars:
                continue  # Remove bidirectional markers
            elif unicodedata.category(char) in self.format_chars:
                continue  # Remove format characters
            else:
                cleaned += char
        
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    async def analyze_text_quality(self, text: str) -> Dict[str, float]:
        """Analyze text quality metrics"""
        if not text:
            return {"quality": 0.0, "readability": 0.0, "coherence": 0.0}
        
        # Basic quality metrics
        word_count = len(text.split())
        char_count = len(text)
        sentence_count = len(re.findall(r'[.!?]+', text))
        
        # Calculate readability score (simplified)
        avg_word_length = char_count / max(1, word_count)
        avg_sentence_length = word_count / max(1, sentence_count)
        
        readability = 1.0 - min(1.0, (avg_word_length - 5) / 10 + (avg_sentence_length - 15) / 20)
        
        # Calculate coherence (based on punctuation and structure)
        punctuation_ratio = len(re.findall(r'[.!?,:;]', text)) / max(1, char_count)
        coherence = min(1.0, punctuation_ratio * 20)
        
        # Overall quality score
        quality = (readability + coherence) / 2
        
        return {
            "quality": max(0.0, min(1.0, quality)),
            "readability": max(0.0, min(1.0, readability)),
            "coherence": max(0.0, min(1.0, coherence)),
            "word_count": word_count,
            "character_count": char_count
        }

class ContentAnalyzer:
    """Analyzes content for processing suitability"""
    
    def __init__(self):
        # Patterns for content classification
        self.instruction_patterns = [
            r'\b(please|could you|can you|would you)\b.*\b(help|assist|provide|explain)\b',
            r'\b(what|how|why|when|where)\b.*\?',
            r'\b(tell me|show me|explain|describe)\b',
        ]
        
        # Quality indicators
        self.quality_indicators = [
            r'\b(analyze|evaluate|consider|examine|investigate)\b',
            r'\b(because|therefore|however|although|furthermore)\b',
            r'\b(evidence|research|study|data|findings)\b',
        ]
        
        # Complexity markers
        self.complexity_markers = [
            r'\b(consciousness|intelligence|awareness|cognition)\b',
            r'\b(system|network|process|framework|methodology)\b',
            r'\b(integration|synthesis|analysis|optimization)\b',
        ]
    
    async def analyze_content_structure(self, text: str) -> Dict[str, float]:
        """Analyze content structure and complexity"""
        if not text:
            return {"structure": 0.0, "complexity": 0.0, "instruction_clarity": 0.0}
        
        text_lower = text.lower()
        
        # Count pattern matches
        instruction_matches = sum(1 for pattern in self.instruction_patterns 
                                if re.search(pattern, text_lower))
        quality_matches = sum(1 for pattern in self.quality_indicators 
                            if re.search(pattern, text_lower))
        complexity_matches = sum(1 for pattern in self.complexity_markers 
                               if re.search(pattern, text_lower))
        
        # Calculate scores
        word_count = len(text.split())
        
        structure_score = min(1.0, (instruction_matches + quality_matches) / max(1, word_count / 20))
        complexity_score = min(1.0, complexity_matches / max(1, word_count / 30))
        instruction_clarity = min(1.0, instruction_matches / max(1, word_count / 25))
        
        return {
            "structure": structure_score,
            "complexity": complexity_score,
            "instruction_clarity": instruction_clarity
        }
    
    async def assess_processing_suitability(self, text: str) -> float:
        """Assess overall suitability for consciousness processing"""
        quality_metrics = await self._calculate_text_metrics(text)
        structure_metrics = await self.analyze_content_structure(text)
        
        # Weighted combination of factors
        suitability = (
            quality_metrics.get("coherence", 0.0) * 0.3 +
            quality_metrics.get("readability", 0.0) * 0.2 +
            structure_metrics.get("structure", 0.0) * 0.3 +
            structure_metrics.get("complexity", 0.0) * 0.2
        )
        
        return min(1.0, max(0.0, suitability))
    
    async def _calculate_text_metrics(self, text: str) -> Dict[str, float]:
        """Calculate basic text metrics"""
        if not text:
            return {"coherence": 0.0, "readability": 0.0}
        
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        
        # Basic coherence (presence of connecting words)
        connectors = ['and', 'but', 'or', 'so', 'because', 'therefore', 'however', 'although']
        connector_count = sum(1 for word in words if word.lower() in connectors)
        coherence = min(1.0, connector_count / max(1, len(words) / 20))
        
        # Basic readability (sentence length distribution)
        if sentences:
            sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
            if sentence_lengths:
                avg_length = sum(sentence_lengths) / len(sentence_lengths)
                readability = 1.0 - min(1.0, abs(avg_length - 15) / 15)  # Optimal ~15 words
            else:
                readability = 0.0
        else:
            readability = 0.0
        
        return {"coherence": coherence, "readability": readability}

class InputValidator:
    """Main input validation system for Genesis Prime"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.text_normalizer = TextNormalizer()
        self.content_analyzer = ContentAnalyzer()
        self.validation_cache: Dict[str, InputAnalysis] = {}
        
    async def initialize(self):
        """Initialize the validation system"""
        await self._setup_database()
        logger.info("Input validation system initialized")
    
    async def _setup_database(self):
        """Set up database tables for validation tracking"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            
            # Input validation logs
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS input_validation_logs (
                    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    content_hash VARCHAR(64) NOT NULL,
                    validation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    validation_level VARCHAR(50),
                    processing_result VARCHAR(50),
                    confidence_score FLOAT,
                    quality_metrics JSONB,
                    processing_time_ms INTEGER,
                    source_info JSONB
                )
            """)
            
            # Content quality tracking
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS content_quality_metrics (
                    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    content_hash VARCHAR(64) NOT NULL,
                    quality_score FLOAT,
                    readability_score FLOAT,
                    coherence_score FLOAT,
                    complexity_score FLOAT,
                    processing_suitability FLOAT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await conn.commit()
            await conn.close()
            
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
    
    async def validate_input(self, input_text: str, source_context: Dict[str, Any] = None) -> InputAnalysis:
        """Validate and analyze input text"""
        start_time = datetime.now()
        
        # Generate content hash
        content_hash = hashlib.sha256(input_text.encode()).hexdigest()
        
        # Check cache first
        if content_hash in self.validation_cache:
            return self.validation_cache[content_hash]
        
        # Normalize text
        normalized_text = await self.text_normalizer.normalize_text(input_text)
        
        # Analyze quality
        quality_metrics = await self.text_normalizer.analyze_text_quality(normalized_text)
        
        # Analyze structure
        structure_metrics = await self.content_analyzer.analyze_content_structure(normalized_text)
        
        # Assess processing suitability
        suitability = await self.content_analyzer.assess_processing_suitability(normalized_text)
        
        # Combine all metrics
        combined_metrics = {**quality_metrics, **structure_metrics, "suitability": suitability}
        
        # Determine validation level and processing result
        validation_level, processing_result = self._determine_validation_outcome(combined_metrics)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(combined_metrics)
        
        # Prepare cleaned content if needed
        cleaned_content = normalized_text if processing_result == ProcessingResult.CLEANED else None
        
        # Generate processing notes
        notes = self._generate_processing_notes(combined_metrics, validation_level)
        
        # Create analysis result
        analysis = InputAnalysis(
            content_hash=content_hash,
            analysis_timestamp=datetime.now(),
            validation_level=validation_level,
            processing_result=processing_result,
            confidence_score=confidence,
            cleaned_content=cleaned_content,
            quality_metrics=combined_metrics,
            processing_notes=notes
        )
        
        # Cache result
        self.validation_cache[content_hash] = analysis
        
        # Log validation
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        await self._log_validation(analysis, processing_time, source_context)
        
        return analysis
    
    def _determine_validation_outcome(self, metrics: Dict[str, float]) -> Tuple[ValidationLevel, ProcessingResult]:
        """Determine validation level and processing result"""
        quality = metrics.get("quality", 0.0)
        suitability = metrics.get("suitability", 0.0)
        coherence = metrics.get("coherence", 0.0)
        
        # High quality content
        if quality >= 0.8 and suitability >= 0.7 and coherence >= 0.6:
            return ValidationLevel.PASS, ProcessingResult.APPROVED
        
        # Good quality that may need minor cleaning
        elif quality >= 0.6 and suitability >= 0.5:
            return ValidationLevel.PROCESS, ProcessingResult.CLEANED
        
        # Moderate quality requiring review
        elif quality >= 0.4 or suitability >= 0.3:
            return ValidationLevel.REVIEW, ProcessingResult.QUEUED
        
        # Low quality content
        else:
            return ValidationLevel.FILTER, ProcessingResult.DECLINED
    
    def _calculate_confidence(self, metrics: Dict[str, float]) -> float:
        """Calculate confidence score for validation"""
        # Base confidence on consistency of metrics
        scores = [
            metrics.get("quality", 0.0),
            metrics.get("readability", 0.0),
            metrics.get("coherence", 0.0),
            metrics.get("suitability", 0.0)
        ]
        
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        
        # High confidence when scores are consistent and high
        consistency = 1.0 - min(1.0, std_score * 2)
        confidence = (mean_score + consistency) / 2
        
        return min(1.0, max(0.0, confidence))
    
    def _generate_processing_notes(self, metrics: Dict[str, float], 
                                 validation_level: ValidationLevel) -> List[str]:
        """Generate processing notes based on analysis"""
        notes = []
        
        quality = metrics.get("quality", 0.0)
        readability = metrics.get("readability", 0.0)
        coherence = metrics.get("coherence", 0.0)
        suitability = metrics.get("suitability", 0.0)
        
        # Quality assessment notes
        if quality >= 0.8:
            notes.append("High quality content suitable for processing")
        elif quality >= 0.6:
            notes.append("Good quality content with minor optimization potential")
        elif quality >= 0.4:
            notes.append("Moderate quality content requiring enhancement")
        else:
            notes.append("Low quality content needs significant improvement")
        
        # Specific metric notes
        if readability < 0.5:
            notes.append("Consider simplifying language for better readability")
        
        if coherence < 0.5:
            notes.append("Content structure could be improved for better flow")
        
        if suitability < 0.3:
            notes.append("Content may not be suitable for consciousness processing")
        
        # Validation level specific notes
        if validation_level == ValidationLevel.FILTER:
            notes.append("Content requires significant revision before processing")
        elif validation_level == ValidationLevel.REVIEW:
            notes.append("Manual review recommended before processing")
        
        return notes
    
    async def _log_validation(self, analysis: InputAnalysis, processing_time_ms: int,
                            source_context: Dict[str, Any] = None):
        """Log validation result to database"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            
            await conn.execute("""
                INSERT INTO input_validation_logs 
                (content_hash, validation_timestamp, validation_level, processing_result,
                 confidence_score, quality_metrics, processing_time_ms, source_info)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                analysis.content_hash, analysis.analysis_timestamp,
                analysis.validation_level.value, analysis.processing_result.value,
                analysis.confidence_score, json.dumps(analysis.quality_metrics),
                processing_time_ms, json.dumps(source_context or {})
            ))
            
            await conn.execute("""
                INSERT INTO content_quality_metrics 
                (content_hash, quality_score, readability_score, coherence_score,
                 complexity_score, processing_suitability)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                analysis.content_hash,
                analysis.quality_metrics.get("quality", 0.0),
                analysis.quality_metrics.get("readability", 0.0),
                analysis.quality_metrics.get("coherence", 0.0),
                analysis.quality_metrics.get("complexity", 0.0),
                analysis.quality_metrics.get("suitability", 0.0)
            ))
            
            await conn.commit()
            await conn.close()
            
        except Exception as e:
            logger.error(f"Failed to log validation: {e}")
    
    async def get_validation_statistics(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get validation system statistics"""
        try:
            conn = await psycopg.AsyncConnection.connect(self.database_url)
            
            cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
            
            # Get validation statistics
            stats_result = await conn.execute("""
                SELECT 
                    COUNT(*) as total_validations,
                    AVG(confidence_score) as avg_confidence,
                    AVG(processing_time_ms) as avg_processing_time,
                    COUNT(CASE WHEN processing_result = 'approved' THEN 1 END) as approved_count,
                    COUNT(CASE WHEN processing_result = 'cleaned' THEN 1 END) as cleaned_count,
                    COUNT(CASE WHEN processing_result = 'queued' THEN 1 END) as queued_count,
                    COUNT(CASE WHEN processing_result = 'declined' THEN 1 END) as declined_count
                FROM input_validation_logs 
                WHERE validation_timestamp > %s
            """, (cutoff_time,))
            
            stats_row = await stats_result.fetchone()
            
            # Get quality metrics
            quality_result = await conn.execute("""
                SELECT 
                    AVG(quality_score) as avg_quality,
                    AVG(readability_score) as avg_readability,
                    AVG(coherence_score) as avg_coherence,
                    AVG(processing_suitability) as avg_suitability
                FROM content_quality_metrics 
                WHERE timestamp > %s
            """, (cutoff_time,))
            
            quality_row = await quality_result.fetchone()
            
            await conn.close()
            
            return {
                "time_window_hours": time_window_hours,
                "total_validations": stats_row[0] if stats_row else 0,
                "average_confidence": float(stats_row[1]) if stats_row and stats_row[1] else 0.0,
                "average_processing_time_ms": float(stats_row[2]) if stats_row and stats_row[2] else 0.0,
                "processing_results": {
                    "approved": stats_row[3] if stats_row else 0,
                    "cleaned": stats_row[4] if stats_row else 0,
                    "queued": stats_row[5] if stats_row else 0,
                    "declined": stats_row[6] if stats_row else 0
                },
                "quality_metrics": {
                    "average_quality": float(quality_row[0]) if quality_row and quality_row[0] else 0.0,
                    "average_readability": float(quality_row[1]) if quality_row and quality_row[1] else 0.0,
                    "average_coherence": float(quality_row[2]) if quality_row and quality_row[2] else 0.0,
                    "average_suitability": float(quality_row[3]) if quality_row and quality_row[3] else 0.0
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get validation statistics: {e}")
            return {"error": str(e)}

# Example usage
async def validate_content(content: str, database_url: str) -> InputAnalysis:
    """Convenience function for content validation"""
    validator = InputValidator(database_url)
    await validator.initialize()
    return await validator.validate_input(content)

# Testing function
async def test_input_validation():
    """Test the input validation system"""
    print("📝 Testing Genesis Prime Input Validation")
    
    database_url = "postgresql://postgres:password@localhost:5432/sentient"
    validator = InputValidator(database_url)
    
    try:
        await validator.initialize()
        print("✅ Validation system initialized")
        
        # Test various input types
        test_inputs = [
            "Analyze the relationship between consciousness and artificial intelligence in modern systems.",
            "help me understand quantum computing please explain the basics",
            "random text with no structure or purpose just words scattered around",
            "What is the nature of consciousness and how can we measure it objectively?"
        ]
        
        for i, test_input in enumerate(test_inputs, 1):
            result = await validator.validate_input(test_input)
            print(f"✅ Test {i}: {result.processing_result.value} (confidence: {result.confidence_score:.2f})")
        
        # Get system statistics
        stats = await validator.get_validation_statistics()
        print(f"✅ System statistics: {stats['total_validations']} validations processed")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_input_validation())