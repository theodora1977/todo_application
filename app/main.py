from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()  # loads .env from project root into os.environ
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import random
from .send_mail import send_otp_email
from . import models, schema
from .database import SessionLocal, engine, Base

app = FastAPI(
    title="Todo Application",
    description="A simple Todo application with user authentication and OTP verification.",
    version="1.0.0",
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://127.0.0.1:8080", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use a hashing scheme that does not rely on the external `bcrypt` C-extension
# to avoid environment issues during development. For production, prefer
# `bcrypt` or `argon2` with correct native dependencies installed.
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


@app.on_event("startup")
def create_tables():
    """Create database tables on startup (useful for development).
    If you use Alembic for migrations in production, run migrations instead
    of relying on this helper.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to my todo application!"}

@app.post("/users/login")
def login_user(credentials: schema.UserCreate, db: Session = Depends(get_db)):
    """User login endpoint - returns token and user data"""
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    
    if not user or not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return {
        "access_token": f"user-{user.id}-token",  # Simple token (use JWT in production)
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
    }

@app.post("/users/", response_model=schema.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)): # Corrected type hint
    # check duplicate email
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # hash password
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # create otp
    otp_code = str(random.randint(100000, 999999))
    otp = models.Otp(
        user_id=db_user.id,
        otp_code=otp_code
    )
    db.add(otp)
    db.commit()

    # Send the OTP and return the user data
    send_otp_email(to_email=db_user.email, otp_code=otp_code)
    return db_user

@app.post("/tasks/", response_model=schema.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schema.TaskCreate, db: Session = Depends(get_db)):
    # In a real app, you'd get the owner_id from the authenticated user
    db_task = models.Task(
        **task.model_dump(),
        owner_id=1 # Placeholder owner_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=list[schema.Task])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@app.put("/tasks/{task_id}", response_model=schema.Task)
def update_task(task_id: int, task_update: dict, db: Session = Depends(get_db)):
    """Update a task (supports partial updates like marking as completed)"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    # Update only provided fields
    for key, value in task_update.items():
        if hasattr(db_task, key) and value is not None:
            setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return None
