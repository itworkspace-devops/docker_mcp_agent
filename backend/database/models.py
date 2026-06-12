from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
    )

    action = Column(String)

    target = Column(Text)

    status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


class Finding(Base):

    __tablename__ = "findings"

    id = Column(
        Integer,
        primary_key=True,
    )

    severity = Column(String)

    category = Column(String)

    message = Column(Text)

    status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


class Remediation(Base):

    __tablename__ = "remediations"

    id = Column(
        Integer,
        primary_key=True,
    )

    finding_id = Column(Integer)

    status = Column(String)

    tool_name = Column(String)

    tool_args = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


class Approval(Base):

    __tablename__ = "approvals"

    id = Column(
        Integer,
        primary_key=True,
    )

    execution_id = Column(String)

    tool_name = Column(String)

    status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )