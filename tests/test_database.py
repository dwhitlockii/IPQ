import pytest
from app.models.database import Database, RequestLog  # Replace with your actual import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Database.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Database.metadata.drop_all(engine)


def test_database_connection(test_db):
    try:
        test_db.execute("SELECT 1")
        assert True
    except OperationalError:
        assert False, "Failed to connect to the database."

def test_log_request(test_db):
    log_entry = RequestLog(ip_address="127.0.0.1", risk_score=50, status_code=200)
    test_db.add(log_entry)
    test_db.commit()

    retrieved_log = test_db.query(RequestLog).filter_by(ip_address="127.0.0.1").first()
    assert retrieved_log is not None
    assert retrieved_log.ip_address == "127.0.0.1"
    assert retrieved_log.risk_score == 50
    assert retrieved_log.status_code == 200