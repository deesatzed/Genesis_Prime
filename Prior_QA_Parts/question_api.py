"""
Question API Module

This module provides Flask API endpoints for the Thousand Questions implementation,
allowing access to question sampling, user response collection, and personality profiling.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Blueprint, request, jsonify, current_app

from thousand_questions import QuestionManager, PersonalityProfiler, get_question_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('question_api')

# Create Blueprint
question_api = Blueprint('question_api', __name__)

# Shared instances
_question_manager = None
_personality_profiler = None

def get_manager():
    """Get or create a QuestionManager instance."""
    global _question_manager
    if _question_manager is None:
        _question_manager = get_question_manager()
    return _question_manager

def get_profiler():
    """Get or create a PersonalityProfiler instance."""
    global _personality_profiler
    if _personality_profiler is None:
        _personality_profiler = PersonalityProfiler(get_manager())
    return _personality_profiler

@question_api.route('/api/questions/config', methods=['GET', 'POST'])
def question_config():
    """Get or update question configuration."""
    manager = get_manager()
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            if 'sample_count' in data:
                count = int(data['sample_count'])
                manager.config.set_sample_questions_count(count)
            
            if 'llm_model' in data:
                model = data['llm_model']
                manager.config.set_llm_model(model)
            
            if 'random_seed' in data:
                seed = int(data['random_seed'])
                manager.config.set_random_seed(seed)
            
            if 'narrative_chapters_enabled' in data:
                enabled = bool(data['narrative_chapters_enabled'])
                manager.config.set_narrative_chapters_enabled(enabled)
            
            return jsonify({
                'status': 'success',
                'message': 'Configuration updated successfully',
                'config': manager.config.get_config_dict()
            })
        
        except ValueError as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
        
        except Exception as e:
            logger.error(f"Error updating configuration: {e}")
            return jsonify({
                'status': 'error',
                'message': f"Error updating configuration: {str(e)}"
            }), 500
    
    # GET request
    return jsonify({
        'status': 'success',
        'config': manager.config.get_config_dict()
    })

@question_api.route('/api/questions/sample', methods=['GET'])
def get_sample_questions():
    """Get a sample of questions based on current configuration."""
    manager = get_manager()
    
    try:
        # Get optional count parameter
        count = request.args.get('count', None)
        if count is not None:
            count = int(count)
        
        # Select sample questions
        questions = manager.select_sample_questions(count)
        
        return jsonify({
            'status': 'success',
            'count': len(questions),
            'questions': questions
        })
    
    except Exception as e:
        logger.error(f"Error getting sample questions: {e}")
        return jsonify({
            'status': 'error',
            'message': f"Error getting sample questions: {str(e)}"
        }), 500

@question_api.route('/api/questions/chapters', methods=['GET'])
def get_chapter_questions():
    """Get questions mapped to narrative chapters."""
    manager = get_manager()
    
    try:
        # Get optional chapter count parameter
        num_chapters = request.args.get('chapters', 5)
        num_chapters = int(num_chapters)
        
        logger.info(f"Mapping questions to {num_chapters} chapters")
        
        # Check if we have questions loaded
        if not manager.questions:
            logger.warning("No questions loaded in manager, attempting to reload")
            manager._load_questions()
            
            # If still no questions, create default questions
            if not manager.questions:
                logger.warning("Creating default questions as fallback")
                default_questions = []
                for i in range(1, 51):  # Create 50 default questions
                    default_questions.append({
                        "id": i,
                        "text": f"Default question {i} for testing purposes",
                        "category": "general",
                        "difficulty": 3,
                        "personal": False
                    })
                manager.questions = default_questions
                manager._categorize_questions()
        
        # Map questions to chapters
        chapter_map = manager.map_questions_to_chapters(num_chapters)
        
        # If chapter_map is empty, create a default mapping
        if not chapter_map:
            logger.warning("Creating default chapter mapping as fallback")
            chapter_map = {}
            questions_per_chapter = len(manager.questions) // num_chapters
            remainder = len(manager.questions) % num_chapters
            
            question_index = 0
            for chapter in range(1, num_chapters + 1):
                chapter_count = questions_per_chapter + (1 if chapter <= remainder else 0)
                chapter_questions = manager.questions[question_index:question_index + chapter_count]
                chapter_map[chapter] = chapter_questions
                question_index += chapter_count
        
        # Convert to list format for easier consumption by frontend
        chapters = []
        for chapter_num, questions in chapter_map.items():
            chapters.append({
                'chapter': chapter_num,
                'questions': questions,
                'count': len(questions)
            })
        
        logger.info(f"Successfully mapped {sum(len(ch['questions']) for ch in chapters)} questions to {len(chapters)} chapters")
        
        return jsonify({
            'status': 'success',
            'chapters': chapters,
            'total_questions': sum(len(ch['questions']) for ch in chapters)
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Error mapping questions to chapters: {e}\n{error_details}")
        
        # Return a fallback response with empty chapters
        fallback_chapters = []
        for chapter in range(1, num_chapters + 1):
            fallback_chapters.append({
                'chapter': chapter,
                'questions': [],
                'count': 0
            })
        
        return jsonify({
            'status': 'partial',
            'message': f"Error occurred but providing fallback: {str(e)}",
            'chapters': fallback_chapters,
            'total_questions': 0
        })

@question_api.route('/api/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Get a specific question by ID."""
    manager = get_manager()
    
    try:
        question = manager.get_question_by_id(question_id)
        if question is None:
            return jsonify({
                'status': 'error',
                'message': f"Question with ID {question_id} not found"
            }), 404
        
        return jsonify({
            'status': 'success',
            'question': question
        })
    
    except Exception as e:
        logger.error(f"Error getting question {question_id}: {e}")
        return jsonify({
            'status': 'error',
            'message': f"Error getting question: {str(e)}"
        }), 500

def store_answer_locally(question_id, question_text, response, metadata=None):
    """Store a user's answer in the local JSON storage.
    
    Args:
        question_id (int): The ID of the question
        question_text (str): The text of the question
        response (str): The user's response
        metadata (dict, optional): Additional metadata about the answer
    
    Returns:
        bool: True if storage was successful, False otherwise
    """
    try:
        # Get the storage path from config
        manager = get_manager()
        user_answers_path = manager.config.base_config.USER_ANSWERS_PATH
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(user_answers_path), exist_ok=True)
        
        # Load existing answers if available
        answers = {}
        if os.path.exists(user_answers_path):
            try:
                with open(user_answers_path, 'r') as f:
                    answers = json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in {user_answers_path}, starting fresh")
        
        # Add or update this answer
        if metadata is None:
            metadata = {}
        
        answer_key = str(question_id)  # Ensure key is a string for JSON
        answers[answer_key] = {
            "question_id": question_id,
            "question": question_text,
            "answer": response,
            "timestamp": metadata.get("timestamp", datetime.now().isoformat()),
            "chapter_id": metadata.get("chapter_id"),
            "category": metadata.get("category"),
            "source": "user"  # Mark this as user-provided
        }
        
        # Save with atomic operation to prevent corruption
        temp_path = user_answers_path + ".tmp"
        with open(temp_path, 'w') as f:
            json.dump(answers, f, indent=2)
        os.replace(temp_path, user_answers_path)
        
        logger.info(f"Successfully stored answer for question {question_id} locally")
        return True
    except Exception as e:
        logger.error(f"Error storing answer locally: {e}")
        return False

async def send_answer_to_mcp_hub(question_id, question_text, response, metadata=None):
    """Send a user's answer to the MCP Hub for distributed storage.
    
    Args:
        question_id (int): The ID of the question
        question_text (str): The text of the question
        response (str): The user's response
        metadata (dict, optional): Additional metadata about the answer
    
    Returns:
        bool: True if successfully sent to MCP Hub, False otherwise
    """
    try:
        import aiohttp
        
        # Get MCP Hub URL from config
        manager = get_manager()
        mcp_hub_url = manager.config.base_config.MCP_HUB_URL
        
        if metadata is None:
            metadata = {}
        
        # Prepare payload for MCP Hub
        payload = {
            "question_id": str(question_id),
            "question": question_text,
            "answer": response,
            "metadata": {
                "timestamp": metadata.get("timestamp", datetime.now().isoformat()),
                "chapter_id": metadata.get("chapter_id"),
                "category": metadata.get("category"),
                "source": "user"
            }
        }
        
        # Send to MCP Hub
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{mcp_hub_url}/api/qa/store",
                json=payload,
                timeout=5  # 5 seconds timeout
            ) as response:
                if response.status == 200:
                    logger.info(f"Successfully sent answer for question {question_id} to MCP Hub")
                    return True
                else:
                    logger.warning(f"Failed to send answer to MCP Hub: {await response.text()}")
                    return False
    except Exception as e:
        logger.error(f"Error sending answer to MCP Hub: {e}")
        return False

@question_api.route('/api/questions/<int:question_id>/response', methods=['POST'])
def save_response(question_id):
    """Save a user's response to a question."""
    manager = get_manager()
    
    try:
        # Validate request data
        data = request.get_json()
        if 'response' not in data:
            return jsonify({
                'status': 'error',
                'message': "Response field is required"
            }), 400
        
        # Get the response text and question details
        response_text = data['response']
        question = manager.get_question_by_id(question_id)
        
        if not question:
            return jsonify({
                'status': 'error', 
                'message': f"Question {question_id} not found"
            }), 404
        
        question_text = question.get("text", "")
        category = question.get("category", "general")
        
        # Prepare metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "chapter_id": data.get("chapter_id"),
            "category": category
        }
        
        # Always store locally first
        local_success = store_answer_locally(
            question_id, 
            question_text, 
            response_text, 
            metadata
        )
        
        # Also try to save in the traditional way (updates the original dataset)
        # This is for backward compatibility
        manager.save_user_response(question_id, response_text)
        
        # Attempt to send to MCP Hub (non-blocking)
        # We use a background thread to avoid blocking the response
        import threading
        import asyncio
        
        def send_to_hub_background():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                hub_success = loop.run_until_complete(
                    send_answer_to_mcp_hub(question_id, question_text, response_text, metadata)
                )
                logger.info(f"MCP Hub storage result: {hub_success}")
            finally:
                loop.close()
        
        # Start background thread for MCP Hub storage
        hub_thread = threading.Thread(target=send_to_hub_background)
        hub_thread.daemon = True
        hub_thread.start()
        
        # Update personality profile
        profiler = get_profiler()
        profile = profiler.get_profile()
        
        # Determine response status based on local storage success
        if not local_success:
            return jsonify({
                'status': 'warning',
                'message': f"Response saved for question {question_id}. Could not store answer locally.",
                'storage': {
                    'local': local_success,
                    'mcp_hub_requested': True
                },
                'profile_updated': True,
                'profile_confidence': profile['confidence']
            })
        
        return jsonify({
            'status': 'success',
            'message': f"Response saved for question {question_id}",
            'storage': {
                'local': local_success,
                'mcp_hub_requested': True
            },
            'profile_updated': True,
            'profile_confidence': profile['confidence']
        })
    
    except Exception as e:
        logger.error(f"Error saving response for question {question_id}: {e}")
        return jsonify({
            'status': 'error',
            'message': f"Error saving response: {str(e)}"
        }), 500

@question_api.route('/api/questions/profile', methods=['GET'])
def get_personality_profile():
    """Get the current personality profile based on user responses."""
    profiler = get_profiler()
    
    try:
        profile = profiler.get_profile()
        
        return jsonify({
            'status': 'success',
            'profile': profile
        })
    
    except Exception as e:
        logger.error(f"Error getting personality profile: {e}")
        return jsonify({
            'status': 'error',
            'message': f"Error getting personality profile: {str(e)}"
        }), 500

# Register the blueprint with the Flask app
def register_question_api(app):
    """Register the question API blueprint with the Flask app."""
    app.register_blueprint(question_api)
    logger.info("Registered question API blueprint")
