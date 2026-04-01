from app import create_app
from models import User, UserProgress
from extensions import db
from flask import url_for

app = create_app()
with app.app_context():
    # Simulate Saicharan (ID 10)
    user = db.session.get(User, 10)
    if not user:
        print("User 10 not found.")
        exit(1)
    
    print(f"Current Role: {user.desired_role}, Age: {user.age}, Edu: {user.education_level}")
    
    # Simulate the POST data
    form_data = {
        'desired_role': 'Nuclear Engineer',
        'prep_weeks': '12',
        'age': '25',
        'education_level': 'M.Tech (2nd Year)',
        'available_time': '6'
    }
    
    print(f"Submitting new data: {form_data}")
    
    # Manually run the logic from app.py:onboarding
    try:
        new_role = form_data.get('desired_role', '').strip()
        new_weeks = int(form_data.get('prep_weeks') or 1)
        new_age = form_data.get('age')
        new_edu = form_data.get('education_level')
        new_time = form_data.get('available_time')
        
        if new_age: user.age = int(new_age)
        if new_edu: user.education_level = new_edu
        if new_time: user.available_time = new_time

        current_role_clean = (user.desired_role or "").strip()
        if current_role_clean and current_role_clean != new_role:
            # Save old progress
            old_p = UserProgress.query.filter_by(user_id=user.id, role=current_role_clean).first()
            if not old_p:
                old_p = UserProgress(user_id=user.id, role=current_role_clean)
                db.session.add(old_p)
            old_p.completed_modules = user.completed_modules
            old_p.readiness_score = user.readiness_score
            old_p.prep_weeks = user.prep_weeks
            
            # Load new
            new_p = UserProgress.query.filter_by(user_id=user.id, role=new_role).first()
            if new_p:
                user.completed_modules = new_p.completed_modules
                user.readiness_score = new_p.readiness_score
                user.prep_weeks = new_weeks
            else:
                user.completed_modules = ""
                user.readiness_score = 0
                user.prep_weeks = new_weeks
        else:
            user.prep_weeks = new_weeks
        
        user.desired_role = new_role
        db.session.commit()
        print("COMMIT SUCCESSFUL.")
    except Exception as e:
        db.session.rollback()
        print(f"COMMIT FAILED: {str(e)}")
    
    # Final check
    db.session.expire_all()
    user_final = db.session.get(User, 10)
    print(f"Final state in DB - Role: {user_final.desired_role}, Age: {user_final.age}, Edu: {user_final.education_level}")
