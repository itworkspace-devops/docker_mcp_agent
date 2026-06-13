from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
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

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String,
        unique=True
    )

    password_hash = Column(
        String
    )

    role = Column(
        String
    )

    password_changed = Column(
        Boolean,
        default=False,
        server_default="false"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class ContainerBaseline(Base):

    __tablename__ = "container_baselines"

    id = Column(
        Integer,
        primary_key=True
    )

    container_name = Column(
        String,
        unique=True
    )

    image = Column(
        String
    )

    restart_policy = Column(
        String
    )

    expected_status = Column(
        String,
        default="running"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
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

class ContainerMetric(Base):

    __tablename__ = "container_metrics"

    id = Column(Integer, primary_key=True)

    container_name = Column(String)

    status = Column(String)

    cpu_percent = Column(Float)

    memory_mb = Column(Float)

    host = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class DockerHost(Base):

    __tablename__ = "docker_hosts"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        unique=True
    )

    host = Column(
        String
    )

    port = Column(
        Integer
    )

    enabled = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
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