from app import create_app
from models import User, UserProgress
from datetime import datetime, timedelta
from extensions import db

app = create_app()
with app.app_context():
    users = User.query.all()
    # Note: User model doesn't have last_updated, but UserProgress does.
    # We'll check all UserProgress updated in the last 30 mins
    recent = datetime.utcnow() - timedelta(minutes=30)
    print(f"Checking for updates since {recent} (UTC)")
    
    ups = UserProgress.query.filter(UserProgress.last_updated >= recent).all()
    if not ups:
        print("No UserProgress updated recently.")
    for p in ups:
        user = db.session.get(User, p.user_id)
        print(f"RECENT PROGRESS: User {user.username} (ID {user.id}), Role {p.role}, Updated {p.last_updated}")

    # Also check the User table directly for current roles
    print("\nCURRENT USER ROLES:")
    for u in users:
        print(f"User {u.username} (ID {u.id}): {u.desired_role}")
