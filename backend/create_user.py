from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

new_user = User(
    username="admin",
    hashed_password=hash_password("Stacking_123"),
)

db.add(new_user)
db.commit()

print(f"Created user: {new_user.username}")

db.close()