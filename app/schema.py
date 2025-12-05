from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    first_name: str | None = None
    last_name: str | None = None

class UserOut(BaseModel):
    id: int
    email: str
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    date: str | None = None
    time: str | None = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int
    completed: bool

    class Config:
        orm_mode = True
