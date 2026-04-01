from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager
import os
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev_key_ai_career'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    
    # Ensure instance folder exists
    if not os.path.exists(os.path.join(basedir, 'instance')):
        os.makedirs(os.path.join(basedir, 'instance'))

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

    @app.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        if request.method == 'POST':
            email = request.form.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                token = secrets.token_urlsafe(32)
                user.reset_token = token
                user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
                db.session.commit()
                
                return redirect(url_for('reset_password', token=token))
            else:
                flash('Email not found.', category='error')
        return render_template('forgot_password.html')

    @app.route('/reset-password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        user = User.query.filter_by(reset_token=token).first()
        
        if not user or user.reset_token_expiry < datetime.utcnow():
            flash('Invalid or expired token.', category='error')
            return redirect(url_for('forgot_password'))
            
        if request.method == 'POST':
            password = request.form.get('password')
            user.password = generate_password_hash(password, method='scrypt')
            user.reset_token = None
            user.reset_token_expiry = None
            db.session.commit()
            flash('Password reset successful! Please login.', category='success')
            return redirect(url_for('login'))
            
        return render_template('reset_password.html', token=token)

    @app.route('/onboarding', methods=['GET', 'POST'])
    @login_required
    def onboarding():
        role_query = request.args.get('role', '')
        from models import UserProgress
        if request.method == 'POST':
            print(f"DEBUG ONBOARDING: form={request.form}")
            try:
                new_role = request.form.get('desired_role', '').strip()
                if not new_role:
                    flash('Desired role cannot be empty.', category='error')
                    return redirect(url_for('onboarding'))
                
                if len(new_role) > 100:
                    flash('Role name is too long (max 100 characters).', category='error')
                    return redirect(url_for('onboarding'))

                # Safe integer conversions
                try:
                    new_weeks = int(request.form.get('prep_weeks') or 1)
                except ValueError:
                    new_weeks = 1
                    
                new_age = request.form.get('age')
                new_edu = request.form.get('education_level')
                new_time = request.form.get('available_time')
                
                print(f"DEBUG ONBOARDING: role='{new_role}', weeks={new_weeks}, edu='{new_edu}'")
                
                # Update basic info
                if new_age:
                    try:
                        current_user.age = int(new_age)
                    except ValueError:
                        pass # Non-critical field failure
                
                if new_edu: current_user.education_level = new_edu
                if new_time: current_user.available_time = new_time

                # Handle Role Switching/Updating
                current_role_clean = (current_user.desired_role or "").strip()
                if current_role_clean and current_role_clean != new_role:
                    print(f"DEBUG ONBOARDING: Switching role from '{current_role_clean}' to '{new_role}'")
                    # Save current progress for the OLD role
                    old_progress = UserProgress.query.filter_by(
                        user_id=current_user.id, 
                        role=current_role_clean
                    ).first()
                    
                    if not old_progress:
                        old_progress = UserProgress(user_id=current_user.id, role=current_role_clean)
                        db.session.add(old_progress)
                    
                    old_progress.completed_modules = current_user.completed_modules
                    old_progress.readiness_score = current_user.readiness_score
                    old_progress.prep_weeks = current_user.prep_weeks
                    
                    # Fetch or initialize progress for the NEW role
                    new_progress = UserProgress.query.filter_by(
                        user_id=current_user.id, 
                        role=new_role
                    ).first()
                    
                    if new_progress:
                        print(f"DEBUG ONBOARDING: Restoring progress for '{new_role}'")
                        current_user.completed_modules = new_progress.completed_modules
                        current_user.readiness_score = new_progress.readiness_score
                        current_user.prep_weeks = new_weeks # Still respect the form's duration choice
                        
                        # Clear cache if weeks changed
                        if new_progress.prep_weeks != new_weeks:
                            new_progress.roadmap_json = None
                    else:
                        print(f"DEBUG ONBOARDING: Initializing new role '{new_role}'")
                        current_user.completed_modules = ""
                        current_user.readiness_score = 0
                        current_user.prep_weeks = new_weeks
                else:
                    # Updating same role or first-time setup
                    print(f"DEBUG ONBOARDING: Initializing/Updating same role '{new_role}'")
                    # Clear cache if weeks changed
                    if current_user.prep_weeks != new_weeks:
                        existing_p = UserProgress.query.filter_by(user_id=current_user.id, role=new_role).first()
                        if existing_p: existing_p.roadmap_json = None
                        
                    current_user.prep_weeks = new_weeks
                
                current_user.desired_role = new_role
                db.session.commit()
                
                # Explicitly sync to ensure UserProgress exists for the new role immediately
                sync_user_progress(current_user)
                
                flash(f'Profile updated for {new_role}!', category='success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                db.session.rollback()
                print(f"ERROR ONBOARDING: {str(e)}")
                flash(f'Error updating profile: {str(e)}', category='error')
        return render_template('onboarding.html', role_query=role_query)
    @app.route('/switch_roadmap/<path:role_name>')
    @login_required
    def switch_roadmap(role_name):
        try:
            from models import UserProgress
            new_role = (role_name or "").strip()
            if not new_role:
                flash("Role name is empty.", category='error')
                return redirect(url_for('dashboard'))
            
            current_role_clean = (current_user.desired_role or "").strip()
            if current_role_clean and current_role_clean != new_role:
                old_p = UserProgress.query.filter_by(user_id=current_user.id, role=current_role_clean).first()
                if not old_p:
                    old_p = UserProgress(user_id=current_user.id, role=current_role_clean)
                    db.session.add(old_p)
                old_p.completed_modules = current_user.completed_modules
                old_p.readiness_score = current_user.readiness_score
                old_p.prep_weeks = current_user.prep_weeks
                
                new_p = UserProgress.query.filter_by(user_id=current_user.id, role=new_role).first()
                if new_p:
                    current_user.completed_modules = new_p.completed_modules
                    current_user.readiness_score = new_p.readiness_score
                    current_user.prep_weeks = new_p.prep_weeks
                else:
                    current_user.completed_modules = ""
                    current_user.readiness_score = 0
            
            current_user.desired_role = new_role
            db.session.commit()
            flash(f'Switched to {new_role} roadmap!', category='success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error switching roadmap: {str(e)}', category='error')
        return redirect(url_for('dashboard'))

    @app.route('/adopt_roadmap/<path:role_name>')
    @login_required
    def adopt_roadmap(role_name):
        try:
            from models import User, UserProgress
            new_role = (role_name or "").strip()
            
            if not new_role:
                flash("Invalid career path.", category='error')
                return redirect(url_for('dashboard'))

            current_role_clean = (current_user.desired_role or "").strip()
            if current_role_clean and current_role_clean != new_role:
                # Save old progress
                old_p = UserProgress.query.filter_by(user_id=current_user.id, role=current_role_clean).first()
                if not old_p:
                    old_p = UserProgress(user_id=current_user.id, role=current_role_clean)
                    db.session.add(old_p)
                old_p.completed_modules = current_user.completed_modules
                old_p.readiness_score = current_user.readiness_score
                old_p.prep_weeks = current_user.prep_weeks
                
                # Fetch new
                new_p = UserProgress.query.filter_by(user_id=current_user.id, role=new_role).first()
                if new_p:
                    current_user.completed_modules = new_p.completed_modules
                    current_user.readiness_score = new_p.readiness_score
                else:
                    current_user.completed_modules = ""
                    current_user.readiness_score = 0
            
            current_user.desired_role = new_role
            db.session.commit()
            sync_user_progress(current_user)
            flash(f'Now following the {new_role} path!', category='success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adopting path: {str(e)}", category='error')
            return redirect(url_for('dashboard'))

    @app.route('/regenerate_roadmap')
    @login_required
    def regenerate_roadmap():
        try:
            from models import UserProgress
            progress = UserProgress.query.filter_by(
                user_id=current_user.id, 
                role=current_user.desired_role
            ).first()
            if progress:
                progress.roadmap_json = None
                db.session.commit()
                flash('Roadmap will be regenerated on next load!', category='info')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error: {str(e)}", category='error')
            return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        from core.roadmap import generate_roadmap, get_recommendations
        from models import QuizAttempt
        
        roadmap_data = generate_roadmap(current_user)
        recommendations = get_recommendations(current_user)
        
        # Get list of weeks where the user has passed the quiz (>= 70%)
        passed_attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()
        passed_weeks = [
            a.week_number for a in passed_attempts 
            if a.score >= (a.total_questions * 0.7)
        ]

        # Calculate current prep week (first incomplete week)
        completed_str = current_user.completed_modules or ""
        completed_indices = [int(i) for i in completed_str.split(',') if i]
        current_prep_week = 1
        for i in range(current_user.prep_weeks or 1):
            if i not in completed_indices:
                current_prep_week = i + 1
                break
            else:
                # If all weeks up to this point are complete, the next week is the current one
                current_prep_week = i + 1
        
        return render_template('dashboard.html', 
                               user=current_user, 
                               roadmap=roadmap_data, 
                               passed_weeks=passed_weeks,
                               current_week=current_prep_week,
                               recommendations=recommendations)

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

def sync_user_progress(user):
    from models import UserProgress
    from extensions import db
    if not user.desired_role:
        return
    progress = UserProgress.query.filter_by(user_id=user.id, role=user.desired_role).first()
    if not progress:
        progress = UserProgress(user_id=user.id, role=user.desired_role)
        db.session.add(progress)
    progress.completed_modules = user.completed_modules
    progress.readiness_score = user.readiness_score
    progress.prep_weeks = user.prep_weeks
    db.session.commit()

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
    sync_user_progress(current_user)
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
        sync_user_progress(current_user)
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
