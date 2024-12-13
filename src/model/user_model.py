import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class UserTeamLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(default=None, foreign_key="user.user_id", primary_key=True)
    team_id: uuid.UUID = Field(default=None, foreign_key="team.team_id", primary_key=True)


class UserProjectLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(default=None, foreign_key="user.user_id", primary_key=True)
    project_id: uuid.UUID = Field(default=None, foreign_key="project.project_id", primary_key=True)


class UserOrganisationLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(default=None, foreign_key="user.user_id", primary_key=True)
    organisation_id: uuid.UUID = Field(default=None, foreign_key="organisation.organisation_id", primary_key=True)


# Organisation Model
class Organisation(SQLModel, table=True):
    organisation_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organisation_name: str

    projects: list["Project"] | None = Relationship(back_populates="organization")
    users: list["User"] = Relationship(back_populates="organizations", link_model=UserOrganisationLink)



# User Model
class User(SQLModel, table=True):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_first_name: str
    user_last_name: str
    user_email: str
    is_email_verified: bool = Field(default=False)


    comments: list["Comment"] = Relationship(back_populates="user")
    teams: list["Team"] | None = Relationship(back_populates="users", link_model=UserTeamLink)
    projects: list["Project"] | None = Relationship(back_populates="users", link_model=UserProjectLink)
    organizations: list["Organisation"] = Relationship(back_populates="users", link_model=UserOrganisationLink)


# Project Model
class Project(SQLModel, table=True):
    project_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    project_name: str
    organisation_id: uuid.UUID = Field(foreign_key="organisation.organisation_id")

    organization: Organisation = Relationship(back_populates="projects")
    tasks: list["Task"] = Relationship(back_populates="project")
    users: list["User"] = Relationship(back_populates="projects", link_model=UserProjectLink)


# UserProject Model
class UserProject(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.user_id")
    project_id: uuid.UUID = Field(foreign_key="project.project_id")


# Team Model
class Team(SQLModel, table=True):
    team_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    team_name: str
    organisation_id: uuid.UUID = Field(foreign_key="organisation.organisation_id")

    users: list["User"] | None = Relationship(back_populates="teams", link_model=UserTeamLink)


# UserTeam Model
class UserTeam(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.user_id")
    team_id: uuid.UUID = Field(foreign_key="team.team_id")


# Task Model
class Task(SQLModel, table=True):
    task_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_name: str
    project_id: uuid.UUID = Field(foreign_key="project.project_id")
    status: str

    project: Project = Relationship(back_populates="tasks")
    activities: list["Activity"] = Relationship(back_populates="task")
    comments: list["Comment"] = Relationship(back_populates="task")


# Activity Model
class Activity(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: uuid.UUID = Field(foreign_key="task.task_id")
    keyboard: str
    mouse: str
    total_time: datetime
    working_time: datetime
    idle_time: datetime
    date: datetime

    task: Task = Relationship(back_populates="activities")
    screen_shots: list["Screenshot"] = Relationship(back_populates="activity")


# Screenshot Model
class Screenshot(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    activity_id: uuid.UUID = Field(foreign_key="activity.id")
    url: str

    activity: Activity = Relationship(back_populates="screen_shots")


# Comment Model
class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: uuid.UUID = Field(foreign_key="task.task_id")
    user_id: uuid.UUID = Field(foreign_key="user.user_id")
    text: str
    comment_date: datetime

    task: Task = Relationship(back_populates="comments")
    user: User = Relationship(back_populates="comments")