from backend.database.db import (
    SessionLocal
)

from backend.database.models import (
    AuditLog,
    Finding,
    Remediation,
    Approval,
)

import json


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