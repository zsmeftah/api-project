from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models import User

def promote_user(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.role = "admin"
            db.commit()
            print(f"User {email} is now an admin.")
        else:
            print(f"User {email} not found.")
    finally:
        db.close()

if __name__ == "__main__":
    promote_user("admin@gmail.com")