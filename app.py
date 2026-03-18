from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev_key_ai_career'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            else:
                new_user = User(
                    username=username, 
                    email=email, 
                    password=generate_password_hash(password, method='scrypt')
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created! Please complete your onboarding.', category='success')
                return redirect(url_for('onboarding'))
        
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    if not user.desired_role:
                        return redirect(url_for('onboarding'))
                    return redirect(url_for('dashboard'))
                else:
                    flash('Incorrect password.', category='error')
            else:
                flash('Email does not exist.', category='error')
                
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/onboarding', methods=['GET', 'POST'])
    @login_required
    def onboarding():
        if request.method == 'POST':
            try:
                new_role = request.form.get('desired_role')
                new_weeks = int(request.form.get('prep_weeks') or 1)
                
                if current_user.desired_role != new_role or current_user.prep_weeks != new_weeks:
                    current_user.completed_modules = ""
                    current_user.readiness_score = 0
                
                current_user.age = request.form.get('age')
                current_user.education_level = request.form.get('education_level')
                current_user.available_time = request.form.get('available_time')
                current_user.desired_role = new_role
                current_user.prep_weeks = new_weeks
                db.session.commit()
                flash(f'Your roadmap for {new_role} has been updated!', category='success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating roadmap: {str(e)}', category='error')
        return render_template('onboarding.html')
    @app.route('/dashboard')
    @login_required
    def dashboard():
        from core.roadmap import generate_roadmap
        roadmap_data = generate_roadmap(current_user)
        return render_template('dashboard.html', user=current_user, roadmap=roadmap_data)

    @app.route('/interview', methods=['GET', 'POST'])
    @login_required
    def interview():
        from core.adaptive_interview import get_next_question
        from models import Question
        
        if request.method == 'POST':
            q_id = request.form.get('question_id')
            user_answer = request.form.get('user_answer').lower()
            current_diff = request.form.get('current_difficulty')
            
            question = Question.query.get(q_id)
            # Simple simulation of evaluation (keyword matching)
            correct = any(word in user_answer for word in question.correct_answer.lower().split())
            
            if correct:
                flash(f"Correct! well done. Moving to harder questions.", category='success')
                current_user.readiness_score = min(current_user.readiness_score + 5, 100)
            else:
                flash(f"Incorrect. The correct answer was: {question.correct_answer}. Let's try an easier one.", category='error')
                current_user.readiness_score = max(current_user.readiness_score - 2, 0)
            
            db.session.commit()
            
            # Fetch next adaptive question
            next_q = get_next_question(current_user, previous_correct=correct, current_difficulty=current_diff)
            return render_template('interview.html', user=current_user, question=next_q)

        # Initial question
        initial_q = get_next_question(current_user)
        return render_template('interview.html', user=current_user, question=initial_q)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

@app.route('/toggle_module/<int:module_idx>')
@login_required
def toggle_module(module_idx):
    completed = current_user.completed_modules.split(',') if current_user.completed_modules else []
    module_str = str(module_idx)
    
    if module_str in completed:
        completed.remove(module_str)
    else:
        completed.append(module_str)
    
    current_user.completed_modules = ','.join(completed)
    
    # Simple progress-based score update
    total_modules = current_user.prep_weeks or 1
    progress_score = (len(completed) / total_modules) * 100
    # Blend with existing score (weighted towards progress)
    current_user.readiness_score = int(progress_score)
    
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    from core.quiz_engine import get_quiz_questions
    if request.method == 'POST':
        # Score the quiz
        score = 0
        total = 0
        for key, value in request.form.items():
            if key.startswith('q_'):
                q_id = int(key.split('_')[1])
                q = QuizQuestion.query.get(q_id)
                if q and q.correct_option == value:
                    score += 1
                total += 1
        
        attempt = QuizAttempt(
            user_id=current_user.id,
            category=current_user.desired_role,
            score=score,
            total_questions=total
        )
        db.session.add(attempt)
        db.session.commit()
        return redirect(url_for('quiz_result', attempt_id=attempt.id))
        
    questions = get_quiz_questions(current_user)
    return render_template('quiz.html', questions=questions)

@app.route('/quiz_result/<int:attempt_id>')
@login_required
def quiz_result(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    return render_template('quiz_result.html', attempt=attempt)

if __name__ == '__main__':
    app.run(debug=True)
