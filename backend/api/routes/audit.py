from fastapi import APIRouter

from backend.database.db import (
    SessionLocal
)

from backend.database.models import (
    AuditLog
)

router = APIRouter()


@router.get("")
def get_audit_logs():

    db = SessionLocal()

    try:

        logs = db.query(
            AuditLog
        ).all()

        return logs

    finally:

        db.close()