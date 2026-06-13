from datetime import datetime

from backend.notifications.store import (
    NOTIFICATIONS
)


def create_notification(
    event_type,
    title,
    message,
):

    notification = {

        "id": len(NOTIFICATIONS) + 1,

        "timestamp":
            datetime.utcnow().isoformat(),

        "event_type":
            event_type,

        "title":
            title,

        "message":
            message,

        "read":
            False,
    }

    NOTIFICATIONS.insert(
        0,
        notification
    )

    return notification


def get_notifications():

    return NOTIFICATIONS


def mark_read(
    notification_id: int
):

    for notification in NOTIFICATIONS:

        if (
            notification["id"]
            == notification_id
        ):

            notification["read"] = True

            return notification

    return None