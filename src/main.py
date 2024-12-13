from contextlib import asynccontextmanager

from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends
from sqlmodel import select, update

from src.core.routes import Routes
from src.database import get_db, init_db
from src.model.user_model import User, Organisation, UserOrganisationLink


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get(Routes.ROOT_URL)
async def root(db: AsyncSession = Depends(get_db)):
    # Fetch the user
    user_res = await db.execute(select(User).where(User.user_first_name == "sai"))
    user_db = user_res.first()
    if not user_db:
        return {"error": "User not found"}

    user: User = user_db[0]

    # Fetch the organisation
    org_res = await db.execute(
        select(Organisation).options(selectinload(Organisation.users)).where(
            Organisation.organisation_name == "soft suave"
        )
    )
    org_db = org_res.first()
    if not org_db:
        return {"error": "Organisation not found"}

    org: Organisation = org_db[0]

    # Check if the link exists in UserOrganisationLink
    link_res = await db.execute(
        select(UserOrganisationLink).where(
            UserOrganisationLink.user_id == user.user_id,
            UserOrganisationLink.organisation_id == org.organisation_id
        )
    )
    link_db = link_res.first()

    if link_db:
        # Update the existing link with a new role_id
        stmt = (
            update(UserOrganisationLink)
            .where(
                UserOrganisationLink.user_id == user.user_id,
                UserOrganisationLink.organisation_id == org.organisation_id
            )
            .values(role_id=2)  # Set the new role_id
        )
        await db.execute(stmt)
        await db.commit()
        return {"message": "UserOrganisationLink updated with new role_id."}
    else:
        # Add a new link if it doesn't exist
        new_link = UserOrganisationLink(
            user_id=user.user_id,
            organisation_id=org.organisation_id,
            role_id=2
        )
        db.add(new_link)
        await db.commit()
        await db.refresh(new_link)
        return {"message": "UserOrganisationLink created with new role_id."}
