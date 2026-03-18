from models import Question
import random

def get_next_question(user, previous_correct=None, current_difficulty="Easy"):
    """
    Adaptive logic:
    1. If previous_correct is None -> Start with Easy.
    2. If previous_correct is True -> Increase difficulty (Easy->Medium->Hard).
    3. If previous_correct is False -> Decrease difficulty (Hard->Medium->Easy).
    """
    difficulties = ["Easy", "Medium", "Hard"]
    idx = difficulties.index(current_difficulty)

    if previous_correct is True:
        idx = min(idx + 1, 2)
    elif previous_correct is False:
        idx = max(idx - 1, 0)
    
    new_diff = difficulties[idx]
    role = (user.desired_role or "").lower()
    
    # 1. Detect role type
    tech_keywords = ['engineer', 'developer', 'coding', 'ai', 'data', 'software', 'tech', 'programmer', 'web', 'frontend', 'backend', 'fullstack', 'devops', 'stack', 'cloud', 'security', 'machine learning', 'data science']
    is_tech = any(kw in role for kw in tech_keywords)
    
    # 2. Fetch all questions for current difficulty
    all_diff_questions = Question.query.filter_by(difficulty=new_diff).all()
    
    # 3. Filter by role type (strict exclusion for non-tech)
    if not is_tech:
        # Exclude tech categories for non-tech roles
        suitable_pool = [q for q in all_diff_questions if q.category not in ["Coding", "Core CS"]]
    else:
        # If tech, prioritize tech categories
        suitable_pool = all_diff_questions

    # 4. Attempt role-specific match within the suitable pool
    role_questions = [q for q in suitable_pool if role in (q.category or "").lower() or role in (q.sub_category or "").lower() or role in q.question_text.lower()]
    
    # 5. Fallback logic: role_specific -> suitable pool -> HR/Professional pool -> Anyone
    if role_questions:
        final_pool = role_questions
    elif is_tech:
        # If tech but no role match, stay in tech categories if possible
        tech_pool = [q for q in all_diff_questions if q.category in ["Coding", "Core CS"]]
        final_pool = tech_pool if tech_pool else all_diff_questions
    elif suitable_pool:
        # If no role match but have suitable non-tech questions, use those
        final_pool = suitable_pool
    else:
        # Last ditch fallback to Professional/HR. IAS is excluded from general tech fallback.
        fallback_pool = Question.query.filter(Question.category.in_(["HR", "Professional"])).all()
        final_pool = fallback_pool if fallback_pool else all_diff_questions
    
    return random.choice(final_pool) if final_pool else None
