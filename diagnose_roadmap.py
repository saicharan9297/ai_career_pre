from app import create_app
from models import User
from core.roadmap import generate_roadmap
import json

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='saicharan').first()
    if not user:
        # Fallback to any user
        user = User.query.first()
        
    print(f"Testing roadmap for User: {user.username}, Role: {user.desired_role}")
    roadmap = generate_roadmap(user)
    
    print("\nROADMAP SUMMARY:")
    print(f"Strategy: {roadmap.get('strategy')}")
    print(f"Is AI: {roadmap.get('is_ai', False)}")
    print(f"Modules: {len(roadmap.get('modules', []))}")
    if roadmap.get('is_ai'):
        print("AI SUCCESSFUL.")
    else:
        print("FALLBACK USED.")
    
    # Check if titles reflect the role
    if roadmap.get('modules'):
        first_title = roadmap['modules'][0]['title']
        print(f"First Week Title: {first_title}")
