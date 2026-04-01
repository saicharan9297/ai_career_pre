from app import create_app
from models import User, UserProgress
from extensions import db

app = create_app()
with app.app_context():
    # Simulate Saicharan (ID 10)
    user = db.session.get(User, 10)
    if not user:
        print("User 10 not found.")
        exit(1)
    
    # Test 1: Normal Update
    print("--- TEST 1: Normal Update ---")
    form_data = {
        'desired_role': 'Embedded Systems Engineer',
        'prep_weeks': '8',
        'age': '24',
        'education_level': 'B.Tech (4th Year)',
        'available_time': '5'
    }
    
    # Simulate the logic in app.py (copy-pasted from updated app.py)
    new_role = form_data.get('desired_role', '').strip()
    new_weeks = int(form_data.get('prep_weeks') or 1)
    new_age = form_data.get('age')
    if new_age:
        try:
            user.age = int(new_age)
        except ValueError:
            pass
    user.education_level = form_data.get('education_level')
    user.available_time = form_data.get('available_time')
    user.desired_role = new_role
    user.prep_weeks = new_weeks
    db.session.commit()
    
    # Check UserProgress
    up = UserProgress.query.filter_by(user_id=10, role='Embedded Systems Engineer').first()
    if up:
        print(f"SUCCESS: UserProgress created/synced for {up.role}")
    else:
        print("FAIL: UserProgress NOT created/synced.")

    # Test 2: Invalid Age (should not crash)
    print("\n--- TEST 2: Invalid Age ---")
    invalid_form = {'age': 'twenty-five'}
    if invalid_form.get('age'):
        try:
            user.age = int(invalid_form.get('age'))
        except ValueError:
            print("Caught expected ValueError for age, continuing...")
    
    db.session.commit()
    print("Final State - Role:", user.desired_role, "Age:", user.age)
