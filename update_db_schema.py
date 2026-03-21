from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

def update_schema():
    with app.app_context():
        try:
            # Check if columns already exist
            db.session.execute(text("SELECT reset_token FROM user LIMIT 1"))
            print("Columns already exist.")
        except Exception:
            print("Adding columns to user table...")
            with db.engine.connect() as conn:
                try:
                    conn.execute(text("ALTER TABLE user ADD COLUMN reset_token VARCHAR(100)"))
                except Exception as e: print(e)
                try:
                    conn.execute(text("ALTER TABLE user ADD COLUMN reset_token_expiry DATETIME"))
                except Exception as e: print(e)
                conn.commit()
            print("Columns checked/added.")

if __name__ == "__main__":
    update_schema()
