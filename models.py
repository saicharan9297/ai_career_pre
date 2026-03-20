from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    
    # Onboarding Data
    age = db.Column(db.Integer)
    education_level = db.Column(db.String(100))
    available_time = db.Column(db.String(100)) # e.g., "Full-time", "2 hours/day"
    desired_role = db.Column(db.String(100))
    prep_weeks = db.Column(db.Integer, default=1)
    readiness_score = db.Column(db.Integer, default=0)
    completed_modules = db.Column(db.String(500), default="") # Comma-separated indices
    
    sessions = db.relationship('InterviewSession', backref='user', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50)) # Coding, Core CS, HR
    sub_category = db.Column(db.String(100)) # e.g., "Data Structures", "Recursion"
    difficulty = db.Column(db.String(20)) # Easy, Medium, Hard
    question_text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text)
    hint = db.Column(db.Text)

class InterviewSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(100))
    score = db.Column(db.Integer)
    weak_areas = db.Column(db.String(500)) # Comma-separated list

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    sub_category = db.Column(db.String(100))
    week_number = db.Column(db.Integer, default=1)
    difficulty = db.Column(db.String(20))
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False) # A, B, C, or D

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))
    week_number = db.Column(db.Integer, default=1)
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    prep_weeks = db.Column(db.Integer, default=1)
    completed_modules = db.Column(db.String(500), default="")
    readiness_score = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
