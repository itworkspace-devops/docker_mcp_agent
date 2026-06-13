from fastapi import APIRouter

from backend.notifications.service import (
    get_notifications,
    mark_read,
)

router = APIRouter()


@router.get("")
def notifications():

    return get_notifications()


@router.post("/{notification_id}/read")
def read(
    notification_id: int
):

    return mark_read(
        notification_id
    )