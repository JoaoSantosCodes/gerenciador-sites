from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import os
from datetime import datetime

# Create database directory if it doesn't exist
os.makedirs('database', exist_ok=True)

# Database configuration
DATABASE_URL = "sqlite:///database/password_manager.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)  # Store bcrypt hash
    salt = Column(String)  # Store encryption salt
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    credentials = relationship("Credential", back_populates="user")

class Credential(Base):
    __tablename__ = 'credentials'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    site_name = Column(String)
    url = Column(String)
    username = Column(String)
    password = Column(String)  # Encrypted password
    notes = Column(String, nullable=True)  # Encrypted notes
    created_at = Column(DateTime, default=datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="credentials")

# Create all tables
Base.metadata.create_all(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_user_id(username):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user.id if user else None 