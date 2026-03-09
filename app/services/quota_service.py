from sqlalchemy.orm import Session

from app.db.database import User


def get_remaining(db: Session, user_id: int) -> int:
    """Return total remaining quota for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return 0
    return user.free_quota + user.paid_quota


def check_and_deduct(db: Session, user_id: int) -> bool:
    """Check if user has quota and deduct 1. Returns True if successful."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False

    if user.free_quota > 0:
        user.free_quota -= 1
        db.commit()
        return True
    elif user.paid_quota > 0:
        user.paid_quota -= 1
        db.commit()
        return True

    return False
