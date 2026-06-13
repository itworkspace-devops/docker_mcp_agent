from fastapi import APIRouter

from backend.hosts.service import (
    register_host,
    list_hosts,
)

router = APIRouter()


@router.get("")
def hosts():

    return list_hosts()


@router.post("")
def add_host(
    payload: dict
):

    return register_host(

        payload["name"],

        payload["host"],

        payload["port"],
    )