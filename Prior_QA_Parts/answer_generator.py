"""
AI-based Answer Generator for Knowledge Expansion.

This module analyzes user's answers and personality profile to generate new answers
that maintain consistency with the user's style, beliefs, and personality traits.
It also supports category-based routing for better distribution of answers.
"""
import os
import json
import random
import re
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict
import datetime

# Import personality profile for style analysis
from personality_profile import PersonalityProfile
# Import category router for question categorization and routing
from category_router import CategoryRouter

# Set up logging
logger = logging.getLogger('answer_generator')

class AnswerGenerator:
    """
    Generates AI-based answers that match the user's style and personality.
    Supports category-based routing for question distribution.
    """
    
    def __init__(self, user_answers_path: str, thousand_questions_path: str = None, categories_path: str = None):
        """
        Initialize the answer generator.
        
        Args:
            user_answers_path: Path to the JSON file containing user answers
            thousand_questions_path: Path to the thousand questions file
            categories_path: Optional path to save/load category assignments
        """
        self.user_answers_path = user_answers_path
        self.thousand_questions_path = thousand_questions_path
        self.categories_path = categories_path
        self.user_answers = {}
        self.all_questions = {}
        self.personality_profile = None
        self.style_patterns = {}
        self.category_router = None
        
        # Load user answers
        self._load_user_answers()
        
        # Load all questions if path provided
        if thousand_questions_path and os.path.exists(thousand_questions_path):
            self._load_all_questions()
            
            # Initialize category router with questions
            if not self.categories_path:
                # Default path for category assignments if not specified
                data_dir = os.path.dirname(user_answers_path)
                self.categories_path = os.path.join(data_dir, 'category_assignments.json')
            
            self.category_router = CategoryRouter(
                questions_path=thousand_questions_path,
                categories_path=self.categories_path
            )
            logger.info("Category router initialized with question categories")
        
        # Extract style patterns from user answers
        self._analyze_user_style()
    
    def _load_user_answers(self) -> None:
        """
        Load user answers from the JSON file.
        """
        try:
            if os.path.exists(self.user_answers_path):
                with open(self.user_answers_path, 'r') as f:
                    self.user_answers = json.load(f)
                logger.info(f"Loaded {len(self.user_answers)} user answers")
            else:
                logger.warning(f"User answers file not found: {self.user_answers_path}")
        except Exception as e:
            logger.error(f"Error loading user answers: {e}")
            self.user_answers = {}
    
    def _load_all_questions(self) -> None:
        """
        Load all questions from the thousand questions file.
        """
        try:
            with open(self.thousand_questions_path, 'r') as f:
                lines = f.readlines()
            
            # Parse questions (assuming format: "Q{id}: {question_text}")
            for line in lines:
                if line.strip() and line.startswith('Q'):
                    try:
                        q_id_str = line.split(':', 1)[0].strip()[1:]
                        q_id = int(q_id_str)
                        question_text = line.split(':', 1)[1].strip()
                        self.all_questions[q_id] = question_text
                    except Exception as e:
                        logger.warning(f"Error parsing question line: {line} - {e}")
            
            logger.info(f"Loaded {len(self.all_questions)} questions")
        except Exception as e:
            logger.error(f"Error loading questions: {e}")
            self.all_questions = {}
    
    def _analyze_user_style(self) -> None:
        """
        Analyze user's writing style from their answers.
        """
        if not self.user_answers:
            logger.warning("No user answers to analyze style")
            return
        
        # Collect style metrics
        answer_texts = [item.get('answer', '') for item in self.user_answers.values()]
        
        # Basic style patterns
        self.style_patterns = {
            'avg_sentence_length': self._calculate_avg_sentence_length(answer_texts),
            'avg_word_length': self._calculate_avg_word_length(answer_texts),
            'sentence_starters': self._extract_sentence_starters(answer_texts),
            'transition_phrases': self._extract_transition_phrases(answer_texts),
            'common_phrases': self._extract_common_phrases(answer_texts),
            'punctuation_frequency': self._analyze_punctuation(answer_texts),
            'formatting_style': self._analyze_formatting(answer_texts)
        }
        
        logger.info("User style analysis complete")
    
    def _calculate_avg_sentence_length(self, texts: List[str]) -> float:
        """
        Calculate the average sentence length in words.
        """
        all_sentences = []
        for text in texts:
            sentences = re.split(r'[.!?]+', text)
            all_sentences.extend([s.strip() for s in sentences if s.strip()])
        
        if not all_sentences:
            return 15.0  # Default if no sentences
        
        word_counts = [len(re.findall(r'\w+', sentence)) for sentence in all_sentences]
        return sum(word_counts) / len(word_counts) if word_counts else 15.0
    
    def _calculate_avg_word_length(self, texts: List[str]) -> float:
        """
        Calculate the average word length in characters.
        """
        all_words = []
        for text in texts:
            words = re.findall(r'\w+', text.lower())
            all_words.extend(words)
        
        if not all_words:
            return 5.0  # Default if no words
        
        return sum(len(word) for word in all_words) / len(all_words)
    
    def _extract_sentence_starters(self, texts: List[str]) -> List[str]:
        """
        Extract common sentence starters.
        """
        starters = []
        for text in texts:
            sentences = re.split(r'[.!?]+', text)
            for sentence in sentences:
                if sentence.strip():
                    words = sentence.strip().split()
                    if words:
                        starters.append(words[0])
        
        # Get top starters
        starter_counts = defaultdict(int)
        for starter in starters:
            starter_counts[starter.lower()] += 1
        
        # Return top 10 starters
        return [s for s, _ in sorted(starter_counts.items(), key=lambda x: x[1], reverse=True)[:10]]
    
    def _extract_transition_phrases(self, texts: List[str]) -> List[str]:
        """
        Extract transition phrases the user tends to use.
        """
        common_transitions = [
            "however", "therefore", "moreover", "furthermore", "consequently",
            "in addition", "nevertheless", "in contrast", "for example", "in conclusion",
            "as a result", "on the other hand", "similarly", "in fact", "indeed"
        ]
        
        used_transitions = []
        for text in texts:
            text_lower = text.lower()
            for transition in common_transitions:
                if transition in text_lower:
                    used_transitions.append(transition)
        
        # Count frequencies
        transition_counts = defaultdict(int)
        for transition in used_transitions:
            transition_counts[transition] += 1
        
        # Return most used transitions
        return [t for t, _ in sorted(transition_counts.items(), key=lambda x: x[1], reverse=True)]
    
    def _extract_common_phrases(self, texts: List[str]) -> List[str]:
        """
        Extract common phrases or expressions used by the user.
        """
        # This is a simplified implementation
        # A more sophisticated approach would use n-gram analysis
        common_phrases = [
            "I believe", "I think", "in my opinion", "I feel that",
            "it seems to me", "I would say", "I consider", "from my perspective"
        ]
        
        phrase_counts = defaultdict(int)
        for text in texts:
            text_lower = text.lower()
            for phrase in common_phrases:
                if phrase.lower() in text_lower:
                    phrase_counts[phrase] += 1
        
        # Return phrases found in user's text
        return [p for p, count in phrase_counts.items() if count > 0]
    
    def _analyze_punctuation(self, texts: List[str]) -> Dict[str, float]:
        """
        Analyze punctuation usage patterns.
        """
        punctuation_marks = {'.': 0, ',': 0, '!': 0, '?': 0, ';': 0, ':': 0, '-': 0}
        total_chars = 0
        
        for text in texts:
            total_chars += len(text)
            for mark in punctuation_marks:
                punctuation_marks[mark] += text.count(mark)
        
        # Calculate frequency per 100 characters
        if total_chars > 0:
            for mark in punctuation_marks:
                punctuation_marks[mark] = (punctuation_marks[mark] / total_chars) * 100
        
        return punctuation_marks
    
    def _analyze_formatting(self, texts: List[str]) -> Dict[str, bool]:
        """
        Analyze text formatting preferences.
        """
        format_patterns = {
            'uses_lists': False,
            'uses_bullet_points': False,
            'uses_numbered_lists': False,
            'uses_paragraphs': False,
            'uses_quotes': False
        }
        
        combined_text = ' '.join(texts)
        
        # Check for lists and bullet points
        if re.search(r'•|\*|-\s', combined_text):
            format_patterns['uses_bullet_points'] = True
            format_patterns['uses_lists'] = True
        
        # Check for numbered lists
        if re.search(r'\d+\.\s', combined_text):
            format_patterns['uses_numbered_lists'] = True
            format_patterns['uses_lists'] = True
        
        # Check for paragraphs (multiple newlines)
        if re.search(r'\n\s*\n', combined_text):
            format_patterns['uses_paragraphs'] = True
        
        # Check for quotes
        if '"' in combined_text or "'" in combined_text:
            format_patterns['uses_quotes'] = True
        
        return format_patterns
    
    def initialize_with_personality(self, profile_path: str) -> None:
        """
        Initialize with a personality profile to influence answer generation.
        
        Args:
            profile_path: Path to the personality profile JSON file
        """
        self.personality_profile = PersonalityProfile(profile_path)
        logger.info("Initialized with personality profile")
    
    def generate_answers(self, num_answers: int = 100, persona_path: str = None, 
                      use_categories: bool = True, balance_categories: bool = True) -> Dict[str, Any]:
        """
        Generate AI-based answers for questions not answered by the user.
        
        Args:
            num_answers: Maximum number of answers to generate
            persona_path: Optional path to a personality profile
            use_categories: Whether to use category-based routing
            balance_categories: Whether to balance questions across categories
            
        Returns:
            Dictionary of generated answers
        """
        if persona_path:
            self.initialize_with_personality(persona_path)
        
        logger.info(f"Starting AI-based answer generation for up to {num_answers} questions")
        
        # Identify questions already answered by the user
        user_question_ids = set(int(a.get('question_id', 0)) for a in self.user_answers.values())
        
        # Select questions to answer based on category routing if available
        questions_to_answer = []
        
        if use_categories and self.category_router:
            logger.info("Using category-based routing for question selection")
            
            if balance_categories:
                # Get a balanced selection of questions across categories
                questions_to_answer = self.category_router.get_balanced_questions(
                    num_questions=num_answers,
                    exclude_ids=user_question_ids
                )
                logger.info(f"Selected {len(questions_to_answer)} questions using balanced category distribution")
            else:
                # Get questions randomly from all categories
                unanswered_ids = [qid for qid in self.all_questions.keys() if qid not in user_question_ids]
                random.shuffle(unanswered_ids)
                selected_ids = unanswered_ids[:num_answers]
                questions_to_answer = [
                    (qid, self.all_questions.get(qid, f"Question {qid}"))
                    for qid in selected_ids
                ]
                logger.info(f"Selected {len(questions_to_answer)} questions using random selection")
        else:
            # Traditional method without category routing
            logger.info("Using traditional method for question selection (no categories)")
            unanswered_ids = [qid for qid in self.all_questions.keys() if qid not in user_question_ids]
            random.shuffle(unanswered_ids)  # Randomize selection
            selected_ids = unanswered_ids[:num_answers]
            questions_to_answer = [
                (qid, self.all_questions.get(qid, f"Question {qid}"))
                for qid in selected_ids
            ]
        
        # Generate answers for selected questions
        generated_answers = {}
        categories_used = defaultdict(int)
        
        for qid, question_text in questions_to_answer:
            try:
                # Generate an answer based on user style and personality
                answer = self._generate_answer_for_question(question_text)
                
                # Get category if available
                category = None
                if self.category_router:
                    category = self.category_router.get_question_category(qid)
                    if category:
                        categories_used[category] += 1
                
                # Save generated answer with category information
                answer_entry = {
                    "question_id": qid,
                    "question": question_text,
                    "answer": answer,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "source": "ai"
                }
                
                # Add category if available
                if category:
                    answer_entry["category"] = category
                
                generated_answers[f"ai_{qid}"] = answer_entry
                logger.debug(f"Generated answer for question {qid}" + 
                           (f" (category: {category})" if category else ""))
            except Exception as e:
                logger.error(f"Error generating answer for question {qid}: {e}")
        
        # Log category distribution if categories were used
        if use_categories and self.category_router and categories_used:
            logger.info("Category distribution of generated answers:")
            for category, count in sorted(categories_used.items()):
                logger.info(f"  {category}: {count} answers")
        
        logger.info(f"Generated {len(generated_answers)} AI answers")
        return generated_answers
    
    def _generate_answer_for_question(self, question: str) -> str:
        """
        Generate an answer for a specific question based on style analysis.
        
        Args:
            question: The question to answer
            
        Returns:
            Generated answer text
        """
        # Analyze question category and type
        question_type = self._analyze_question_type(question)
        
        # Select most similar answered questions as references
        reference_answers = self._find_similar_answered_questions(question)
        
        # Generate answer based on style patterns and references
        answer_text = self._craft_answer(question, question_type, reference_answers)
        
        return answer_text
    
    def _analyze_question_type(self, question: str) -> str:
        """
        Analyze the type of question (philosophical, personal, etc.)
        
        Args:
            question: The question text
            
        Returns:
            Question type classification
        """
        question_lower = question.lower()
        
        # Simple rule-based classification
        if any(word in question_lower for word in ["think", "believe", "opinion", "philosophy", "ethical", "moral"]):
            return "philosophical"
        elif any(word in question_lower for word in ["you", "your", "yourself"]):
            return "personal"
        elif any(word in question_lower for word in ["define", "what is", "explain", "describe"]):
            return "definitional"
        elif any(word in question_lower for word in ["how", "process", "steps", "method"]):
            return "procedural"
        elif any(word in question_lower for word in ["why", "reason", "cause"]):
            return "explanatory"
        else:
            return "general"
    
    def _find_similar_answered_questions(self, target_question: str) -> List[str]:
        """
        Find similar questions that have been answered by the user.
        
        Args:
            target_question: Question to find similar answered questions for
            
        Returns:
            List of reference answers
        """
        # This is a simplified implementation
        # A more sophisticated approach would use embedding similarity
        
        target_words = set(re.findall(r'\w+', target_question.lower()))
        
        # Calculate similarity based on word overlap
        similarities = []
        for item in self.user_answers.values():
            question = item.get('question', '')
            answer = item.get('answer', '')
            
            if question and answer:
                question_words = set(re.findall(r'\w+', question.lower()))
                overlap = len(target_words.intersection(question_words))
                similarities.append((overlap, answer))
        
        # Sort by similarity (higher is better)
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        # Return top 3 most similar answers
        return [answer for _, answer in similarities[:3]]
    
    def _craft_answer(self, question: str, question_type: str, reference_answers: List[str]) -> str:
        """
        Craft an answer based on the question type and reference answers.
        
        Args:
            question: The question to answer
            question_type: Type of question classification
            reference_answers: Similar answers to use as reference
            
        Returns:
            Crafted answer text
        """
        # Use personality profile if available
        if self.personality_profile:
            # Let personality profile handle the response generation
            # This is a simplified representation
            return self.personality_profile.generate_response(question, question_type)
        
        # Otherwise use style patterns to craft an answer
        avg_sentence_length = self.style_patterns.get('avg_sentence_length', 15)
        common_starters = self.style_patterns.get('sentence_starters', [])
        transition_phrases = self.style_patterns.get('transition_phrases', [])
        common_phrases = self.style_patterns.get('common_phrases', [])
        
        # Construct answer components
        components = []
        
        # Opening sentence with common phrase
        if common_phrases and random.random() < 0.7:
            opener = random.choice(common_phrases) + ", " + self._generate_sentence_for_question(question, question_type)
            components.append(opener)
        else:
            if common_starters:
                opener = random.choice(common_starters) + " " + self._generate_sentence_fragment()
            else:
                opener = self._generate_sentence_for_question(question, question_type)
            components.append(opener)
        
        # Middle sentences with transition
        if transition_phrases and random.random() < 0.6:
            transition = random.choice(transition_phrases).capitalize() + ", " + self._generate_sentence_fragment()
            components.append(transition)
        
        # Add another sentence
        components.append(self._generate_sentence_fragment())
        
        # Closing sentence
        closer = self._generate_closing_sentence(question_type)
        components.append(closer)
        
        # Join all parts with appropriate spacing
        answer = " ".join(components)
        
        # Incorporate formatting preferences
        if self.style_patterns.get('formatting_style', {}).get('uses_paragraphs', False) and random.random() < 0.3:
            # Split into paragraphs
            mid_point = len(answer) // 2
            space_near_midpoint = answer.find(". ", mid_point - 20, mid_point + 20)
            if space_near_midpoint > 0:
                answer = answer[:space_near_midpoint+1] + "\n\n" + answer[space_near_midpoint+1:].strip()
        
        return answer
    
    def _generate_sentence_for_question(self, question: str, question_type: str) -> str:
        """
        Generate a sentence appropriate for the question type.
        
        Args:
            question: The question text
            question_type: Type of question
            
        Returns:
            Generated sentence
        """
        if question_type == "philosophical":
            templates = [
                "I believe that philosophical questions like this require deep reflection.",
                "This question touches on fundamental aspects of existence and consciousness.",
                "When I contemplate this philosophical question, I find myself considering multiple perspectives."
            ]
        elif question_type == "personal":
            templates = [
                "From my perspective, this is a deeply personal matter that shapes how I interact with the world.",
                "I've often reflected on my own experiences when considering this question.",
                "My personal journey has led me to develop specific thoughts on this matter."
            ]
        elif question_type == "definitional":
            templates = [
                "I would define this concept based on both established understanding and personal insight.",
                "The definition of this term encompasses several important dimensions.",
                "When defining this concept, it's important to consider its various applications."
            ]
        elif question_type == "procedural":
            templates = [
                "The process involved can be understood through several key steps.",
                "I approach this type of situation methodically, considering all relevant factors.",
                "There's a logical sequence of considerations when addressing this."
            ]
        elif question_type == "explanatory":
            templates = [
                "There are multiple factors that contribute to this phenomenon.",
                "Understanding the reasons behind this requires examining several perspectives.",
                "I see several key reasons that help explain this situation."
            ]
        else:  # general
            templates = [
                "This question raises interesting points about how we understand the world.",
                "I've developed certain perspectives on this topic through experience and reflection.",
                "There are multiple dimensions to consider when exploring this question."
            ]
        
        return random.choice(templates)
    
    def _generate_sentence_fragment(self) -> str:
        """
        Generate a generic sentence fragment to continue an answer.
        
        Returns:
            Generated sentence fragment
        """
        fragments = [
            "this perspective allows for a deeper understanding of the underlying principles.",
            "examining this from multiple angles reveals important nuances.",
            "there are important considerations that influence how we approach this.",
            "my experiences have shaped my understanding in significant ways.",
            "the context surrounding this question significantly impacts how we answer it.",
            "balancing different viewpoints leads to a more comprehensive understanding.",
            "integrating various sources of knowledge creates a richer perspective."
        ]
        
        return random.choice(fragments)
    
    def _generate_closing_sentence(self, question_type: str) -> str:
        """
        Generate a closing sentence appropriate for the question type.
        
        Args:
            question_type: Type of question
            
        Returns:
            Generated closing sentence
        """
        if question_type == "philosophical":
            closers = [
                "Ultimately, this philosophical inquiry leads us to examine our fundamental assumptions about reality.",
                "The answer to this philosophical question continues to evolve as my understanding deepens.",
                "Perhaps the true value lies not in a definitive answer, but in the exploration itself."
            ]
        else:
            closers = [
                "I continue to refine my understanding of this as I gain new insights and experiences.",
                "While this represents my current perspective, I remain open to evolving my viewpoint.",
                "There's a richness to this topic that invites ongoing exploration and reflection.",
                "I find that approaching this with curiosity rather than certainty leads to greater insight."
            ]
        
        return random.choice(closers)
