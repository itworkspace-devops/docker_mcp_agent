from sqlalchemy import text

from backend.database.db import engine
from backend.database.models import Base
from backend.database.repository import (
    get_user_by_username,
    create_user,
)
from backend.security.auth import (
    hash_password,
)


def initialize_database():

    Base.metadata.create_all(
        bind=engine
    )

    with engine.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE users "
                "ADD COLUMN IF NOT EXISTS password_changed boolean DEFAULT false"
            )
        )

    admin = get_user_by_username("admin")

    if not admin:
        create_user(
            username="admin",
            password_hash=hash_password("admin"),
            role="admin",
            password_changed=False,
        )

    print("Database initialized")
