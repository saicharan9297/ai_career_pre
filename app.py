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
        return db.session.get(User, int(user_id))

    @app.after_request
    def add_header(response):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
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
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
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
        from models import QuizAttempt
        roadmap_data = generate_roadmap(current_user)
        
        # Get list of weeks where the user has passed the quiz (>= 70%)
        passed_attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()
        passed_weeks = [
            a.week_number for a in passed_attempts 
            if a.score >= (a.total_questions * 0.7)
        ]
        
        return render_template('dashboard.html', user=current_user, roadmap=roadmap_data, passed_weeks=passed_weeks)

    @app.route('/interview')
    @login_required
    def interview():
        from flask import session
        from models import Question
        
        # If no session initialized, redirect to start
        if 'interview_questions' not in session:
            return redirect(url_for('start_interview'))
            
        current_idx = session.get('current_question_idx', 0)
        questions_ids = session.get('interview_questions', [])
        
        if current_idx >= len(questions_ids):
            return redirect(url_for('interview_result'))
            
        q_id = questions_ids[current_idx]
        question = db.session.get(Question, q_id)
        
        return render_template('interview.html', 
                               user=current_user, 
                               question=question, 
                               current_num=current_idx + 1, 
                               total_num=len(questions_ids))

    @app.route('/start_interview')
    @login_required
    def start_interview():
        from core.interview_engine import get_interview_session_questions
        from flask import session
        
        questions = get_interview_session_questions(current_user)
        session['interview_questions'] = [q.id for q in questions]
        session['current_question_idx'] = 0
        session['interview_answers'] = []
        session.modified = True
        
        return redirect(url_for('interview'))

    @app.route('/submit_answer', methods=['POST'])
    @login_required
    def submit_answer():
        from flask import session
        from models import Question
        from core.interview_engine import evaluate_answer
        
        q_id = request.form.get('question_id')
        user_answer = request.form.get('user_answer')
        
        question = db.session.get(Question, q_id)
        score, feedback = evaluate_answer(question, user_answer)
        
        answers = session.get('interview_answers', [])
        answers.append({
            'question_text': question.question_text,
            'user_answer': user_answer,
            'score': score,
            'feedback': feedback
        })
        session['interview_answers'] = answers
        session['current_question_idx'] = session.get('current_question_idx', 0) + 1
        session.modified = True
        
        if session['current_question_idx'] >= len(session['interview_questions']):
            return redirect(url_for('interview_result'))
            
        return redirect(url_for('interview'))

    @app.route('/interview_result')
    @login_required
    def interview_result():
        from flask import session
        from models import InterviewSession
        
        answers = session.get('interview_answers', [])
        if not answers:
            return redirect(url_for('dashboard'))
            
        total_score = sum(a['score'] for a in answers)
        avg_score = int(total_score / len(answers)) if answers else 0
        
        # Save to database
        new_session = InterviewSession(
            user_id=current_user.id,
            role=current_user.desired_role,
            score=avg_score,
            weak_areas="" # Could be parsed from low scores
        )
        db.session.add(new_session)
        db.session.commit()
        
        # Clear session
        session.pop('interview_questions', None)
        session.pop('current_question_idx', None)
        session.pop('interview_answers', None)
        
        return render_template('interview_result.html', user=current_user, answers=answers, final_score=avg_score)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

@app.route('/toggle_module/<int:module_idx>')
@login_required
def toggle_module(module_idx):
    from models import QuizAttempt
    
    week_num = module_idx + 1
    module_str = str(module_idx)
    completed = current_user.completed_modules.split(',') if current_user.completed_modules else []
    
    if module_str in completed:
        # User wants to STUDY AGAIN - Mark as incomplete
        completed.remove(module_str)
        
        # Reset quiz status for this week by deleting attempts
        QuizAttempt.query.filter_by(user_id=current_user.id, week_number=week_num).delete()
        
        flash(f"Week {week_num} marked as incomplete. You can now study again and redo the quiz!", category='info')
    else:
        # User wants to MARK AS COMPLETE
        # Check if a quiz for this week has been passed (at least 70% score)
        passed_quiz = QuizAttempt.query.filter_by(
            user_id=current_user.id, 
            week_number=week_num
        ).filter(QuizAttempt.score >= (QuizAttempt.total_questions * 0.7)).first()
        
        if not passed_quiz:
            flash(f"You must pass the quiz for Week {week_num} with at least 70% before marking it as complete!", category='error')
            return redirect(url_for('dashboard'))

        completed.append(module_str)
        flash(f"Week {week_num} marked as complete!", category='success')
    
    current_user.completed_modules = ','.join(completed)
    
    # Update progress-based score
    total_modules = current_user.prep_weeks or 1
    progress_score = (len(completed) / total_modules) * 100
    current_user.readiness_score = int(progress_score)
    
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    from core.quiz_engine import get_quiz_questions
    from models import QuizQuestion, QuizAttempt
    
    week = request.args.get('week', 1, type=int)
    
    if request.method == 'POST':
        # Score the quiz
        score = 0
        total = 0
        form_week = request.form.get('week_number', 1, type=int)
        for key, value in request.form.items():
            if key.startswith('q_'):
                q_id = int(key.split('_')[1])
                q = db.session.get(QuizQuestion, q_id)
                if q and q.correct_option == value:
                    score += 1
                total += 1
        
        attempt = QuizAttempt(
            user_id=current_user.id,
            category=current_user.desired_role,
            week_number=form_week,
            score=score,
            total_questions=total
        )
        db.session.add(attempt)
        
        # Automatically mark module as complete if passed (>= 70%)
        if total > 0 and (score / total) >= 0.7:
            # Note: module_idx is 0-based, so week 1 = 0
            module_idx = form_week - 1
            completed = current_user.completed_modules.split(',') if current_user.completed_modules else []
            module_str = str(module_idx)
            
            if module_str not in completed:
                completed.append(module_str)
                current_user.completed_modules = ','.join(completed)
                
                # Update readiness score
                total_modules = current_user.prep_weeks or 1
                progress_score = (len(completed) / total_modules) * 100
                current_user.readiness_score = int(progress_score)
                flash(f"Congratulations! You passed Week {form_week} and it's been marked as complete.", category='success')
        
        db.session.commit()
        return redirect(url_for('quiz_result', attempt_id=attempt.id))
        
    questions = get_quiz_questions(current_user, week_number=week)
    return render_template('quiz.html', questions=questions, week=week)

@app.route('/quiz_result/<int:attempt_id>')
@login_required
def quiz_result(attempt_id):
    from models import QuizAttempt
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    return render_template('quiz_result.html', attempt=attempt)

if __name__ == '__main__':
    app.run(debug=True)
