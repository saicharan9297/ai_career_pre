from app import create_app
from models import User
from extensions import db

app = create_app()
with app.app_context():
    # Find the first user
    user = User.query.first()
    if not user:
        print("No user found.")
        exit(1)
    
    old_role = user.desired_role
    new_role = "AI Research Scientist"
    
    print(f"Original Role: {old_role}")
    print(f"Updating to: {new_role}")
    
    user.desired_role = new_role
    db.session.commit()
    
    # Reload from DB
    db.session.expire_all()
    user_updated = db.session.get(User, user.id)
    print(f"Role after commit: {user_updated.desired_role}")
    
    if user_updated.desired_role == new_role:
        print("SUCCESS: Profile updated in DB.")
    else:
        print("FAIL: Profile NOT updated in DB.")
        
    # Revert
    user_updated.desired_role = old_role
    db.session.commit()
    print(f"Reverted to: {user_updated.desired_role}")
