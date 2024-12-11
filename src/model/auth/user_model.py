import uuid
from datetime import datetime
from typing import Optional
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    user_id: uuid.UUID = Field(sa_column=Column(pg.UUID, default=uuid.uuid4(), primary_key=True))
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email_id: str = Field(
        index=True,
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    hashed_password: str = Field(
        index=True,
        regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    )
    created_at: Optional[datetime] = datetime.now()

    # # One-to-One relationship
    # user_team: Optional["UserTeam"] = Relationship(back_populates="user")

#
# class UserTeam(SQLModel, table=True):  # Associated table
#     user_id: str = Field(foreign_key="user.user_id", primary_key=True)
#     team_id: str = Field(index=True)
#
#     # # One-to-One relationship
#     # user: "User" = Relationship(back_populates="user_team")
