from datetime import datetime, timedelta

from backend.database.db import (
    SessionLocal
)

from backend.database.models import (
    AuditLog,
    Finding,
    Remediation,
    Approval,
    ContainerMetric,
    DockerHost,
    User,
    ContainerBaseline,
    ChatSession,
    ChatMessage,
)

import json


def create_host(
    name,
    host,
    port,
):

    db = SessionLocal()

    try:

        obj = DockerHost(
            name=name,
            host=host,
            port=port,
        )

        db.add(obj)

        db.commit()

        db.refresh(obj)

        return obj

    finally:

        db.close()

def update_host_record(
    host_id,
    name,
    host,
    port,
    enabled=True
):
    db = SessionLocal()
    try:
        obj = db.get(DockerHost, host_id)
        if not obj:
            return None
        
        obj.name = name
        obj.host = host
        obj.port = port
        obj.enabled = enabled
        
        db.commit()
        db.refresh(obj)
        return obj
    finally:
        db.close()

def delete_host_record(host_id):
    db = SessionLocal()
    try:
        obj = db.get(DockerHost, host_id)
        if not obj:
            return False
        
        db.delete(obj)
        db.commit()
        return True
    finally:
        db.close()
        
def get_hosts():

    db = SessionLocal()

    try:

        return db.query(
            DockerHost
        ).all()

    finally:

        db.close()
        
def get_host_by_name(
    name
):

    db = SessionLocal()

    try:

        return (
            db.query(
                DockerHost
            )
            .filter(
                DockerHost.name == name
            )
            .first()
        )

    finally:

        db.close()
        
        
def get_user_by_username(
    username
):

    db = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(
                User.username == username
            )
            .first()
        )

    finally:

        db.close()


def list_users():

    db = SessionLocal()

    try:

        return db.query(User).all()

    finally:

        db.close()


def create_user(
    username,
    password_hash,
    role,
    password_changed=False,
):

    db = SessionLocal()

    try:

        user = User(
            username=username,
            password_hash=password_hash,
            role=role,
            password_changed=password_changed,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    finally:

        db.close()


def update_user_password(
    username,
    password_hash,
    password_changed=True,
):

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

        if not user:
            return None

        user.password_hash = password_hash
        user.password_changed = password_changed

        db.commit()
        db.refresh(user)

        return user

    finally:

        db.close()


def create_baseline(
    container_name,
    image,
    restart_policy,
):

    db = SessionLocal()

    try:

        baseline = ContainerBaseline(

            container_name=container_name,

            image=image,

            restart_policy=restart_policy,
        )

        db.add(
            baseline
        )

        db.commit()

        return baseline

    finally:

        db.close()
        
def get_baselines():

    db = SessionLocal()

    try:

        return db.query(
            ContainerBaseline
        ).all()

    finally:

        db.close()

def get_latest_metrics():

    db = SessionLocal()

    try:

        return db.query(
            ContainerMetric
        ).order_by(
            ContainerMetric.id.desc()
        ).limit(
            100
        ).all()

    finally:

        db.close()


def save_container_metric(
    container_name,
    status,
    cpu_percent,
    memory_mb,
    host="local",
):

    db = SessionLocal()

    try:

        metric = ContainerMetric(

            container_name=
                container_name,

            status=
                status,

            cpu_percent=
                cpu_percent,

            memory_mb=
                memory_mb,

            host=
                host,
        )

        db.add(metric)

        db.commit()

        db.refresh(metric)

        return metric

    finally:

        db.close()


def save_remediation(
    finding_id,
    tool_name,
    tool_args,
):

    db = SessionLocal()

    try:

        remediation = Remediation(

            finding_id=finding_id,

            status="pending",

            tool_name=tool_name,

            tool_args=json.dumps(
                tool_args
            ),
        )

        db.add(
            remediation
        )

        db.commit()

        db.refresh(
            remediation
        )

        return remediation

    finally:

        db.close()
        
def update_remediation_record(
    remediation_id,
    status,
):

    db = SessionLocal()

    try:

        remediation = db.get(
            Remediation,
            remediation_id,
        )

        if not remediation:

            return None

        remediation.status = status

        db.commit()

        db.refresh(
            remediation
        )

        return remediation

    finally:

        db.close() 
        
def update_remediation_record(
    remediation_id,
    status,
):

    db = SessionLocal()

    try:

        remediation = db.get(
            Remediation,
            remediation_id,
        )

        if not remediation:

            return None

        remediation.status = status

        db.commit()

        db.refresh(
            remediation
        )

        return remediation

    finally:

        db.close()       
        

def close_finding_record(
    finding_id,
):

    db = SessionLocal()

    try:

        finding = db.get(
            Finding,
            finding_id,
        )

        if not finding:

            return None

        finding.status = "closed"

        db.commit()

        db.refresh(
            finding
        )

        return finding

    finally:

        db.close()

def save_remediation(
    finding_id,
    tool_name,
    tool_args,
):

    db = SessionLocal()

    try:

        remediation = Remediation(

            finding_id=finding_id,

            status="pending",

            tool_name=tool_name,

            tool_args=str(
                tool_args
            ),
        )

        db.add(
            remediation
        )

        db.commit()

        db.refresh(
            remediation
        )

        return remediation

    finally:

        db.close()
        
def get_remediations():

    db = SessionLocal()

    try:

        return db.query(
            Remediation
        ).all()

    finally:

        db.close()
      
def get_remediation_by_id(
    remediation_id,
):

    db = SessionLocal()

    try:

        return db.get(
            Remediation,
            remediation_id,
        )

    finally:

        db.close()  

def get_findings():

    db = SessionLocal()

    try:

        return db.query(
            Finding
        ).all()

    finally:

        db.close()
        
def save_approval(
    execution_id,
    tool_name,
    status,
):

    db = SessionLocal()

    try:

        approval = Approval(
            execution_id=execution_id,
            tool_name=tool_name,
            status=status,
        )

        db.add(approval)

        db.commit()

        db.refresh(approval)

        return approval

    finally:

        db.close()        

def save_finding(
    severity,
    category,
    message,
):

    db = SessionLocal()

    try:

        finding = Finding(

            severity=severity,

            category=category,

            message=message,

            status="open",
        )

        db.add(
            finding
        )

        db.commit()

        db.refresh(
            finding
        )

        return finding

    finally:

        db.close()


def save_audit_log(
    action,
    target,
    status,
):

    db = SessionLocal()

    try:

        log = AuditLog(
            action=action,
            target=target,
            status=status,
        )

        db.add(log)

        db.commit()

    finally:

        db.close()

def get_enabled_hosts():
    db = SessionLocal()
    try:
        return db.query(DockerHost).filter(DockerHost.enabled == True).all()
    finally:
        db.close()

def get_chat_sessions():
    db = SessionLocal()
    try:
        cleanup_old_chats()
        return db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    finally:
        db.close()

def get_chat_messages(session_id):
    db = SessionLocal()
    try:
        return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()
    finally:
        db.close()

def save_chat_message(session_id, role, content, title=None):
    db = SessionLocal()
    try:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            session = ChatSession(id=session_id, title=title or content[:50])
            db.add(session)
        elif title:
            session.title = title
        
        message = ChatMessage(session_id=session_id, role=role, content=content)
        db.add(message)
        db.commit()
        return message
    finally:
        db.close()

def cleanup_old_chats():
    db = SessionLocal()
    try:
        threshold = datetime.utcnow() - timedelta(days=15)
        # Delete old messages
        db.query(ChatMessage).filter(ChatMessage.created_at < threshold).delete()
        # Delete sessions with no messages
        sessions = db.query(ChatSession).all()
        for s in sessions:
            msg_count = db.query(ChatMessage).filter(ChatMessage.session_id == s.id).count()
            if msg_count == 0:
                db.delete(s)
        db.commit()
    finally:
        db.close()