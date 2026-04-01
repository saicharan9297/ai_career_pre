import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    GEMINI_API_KEY = GEMINI_API_KEY.strip().strip("'").strip('"')
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    model = None

import requests
import json

def call_llm(prompt):
    """
    Uses the configured Gemini SDK to generate content.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found in environment."
    
    if not model:
        return "Error: Gemini model not initialized."
        
    try:
        response = model.generate_content(prompt)
        if response.text:
            return response.text
        return "Error: AI returned empty response."
    except Exception as e:
        print(f"DEBUG: AI Call Error: {str(e)}")
        return f"Error calling AI API: {str(e)}"

def evaluate_answer_ai(question_text, correct_answer, user_answer):
    """
    Uses LLM to evaluate a student's answer.
    """
    prompt = f"""
    You are an expert career interviewer. 
    Evaluate the following student's answer based on the question and the expected correct points.
    
    Question: {question_text}
    Expected Points: {correct_answer}
    Student Answer: {user_answer}
    
    Return a JSON object with:
    1. "score": An integer from 0 to 100.
    2. "feedback": A short, encouraging but critical feedback (2-3 sentences).
    3. "key_points_missed": A list of points the student missed.
    
    Return ONLY the JSON.
    """
    return call_llm(prompt)

def generate_roadmap_ai(user_profile, search_context):
    """
    Generates a personalized roadmap using RAG (search_context).
    Returns a JSON string.
    """
    prompt = f"""
    You are a professional career counselor. Generate a personalized {user_profile['prep_weeks']} week roadmap for:
    Role: {user_profile['desired_role']}
    Education: {user_profile['education_level']}
    
    Use the following curriculum data as context (RAG):
    {search_context}
    
    Return ONLY a JSON array of objects. Each object represents a week and MUST have:
    - "title": (e.g., "Week 1: Introduction to {user_profile['desired_role']}")
    - "subjects": A list of 3-4 objects, each with:
        - "name": (Subject title)
        - "content": (Brief description of what to study)
    
    Return ONLY the JSON. Do not include markdown formatting like ```json.
    """
    return call_llm(prompt)

def generate_quiz_ai(subject_name, subject_content, count=5):
    """
    Generates MCQs using LLM for a specific subject.
    """
    prompt = f"""
    You are an expert examiner. Generate {count} multiple-choice questions (MCQs) for the following topic:
    Topic: {subject_name}
    Context: {subject_content}
    
    For each question, provide:
    1. Question text
    2. 4 Options (A, B, C, D)
    3. The Correct Option (just the letter A, B, C, or D)
    
    Return ONLY a JSON array of objects with the following keys:
    "question_text", "option_a", "option_b", "option_c", "option_d", "correct_option"
    """
    return call_llm(prompt)
