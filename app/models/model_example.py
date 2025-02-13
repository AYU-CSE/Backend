from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    password: str
    email: str
    student_id: int
    role_id: int
    created_at: datetime
    updated_at: datetime
