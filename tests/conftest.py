import pytest

from app.api.auth import create_token
from app.db.database import Base, SessionLocal, User, engine


@pytest.fixture(autouse=True)
def setup_db():
    """Create a fresh DB schema for each test and seed a test user."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = User(openid="test-openid", free_quota=10)
    db.add(user)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture()
def token():
    return create_token(user_id=1)
