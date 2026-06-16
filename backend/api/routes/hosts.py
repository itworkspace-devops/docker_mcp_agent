from fastapi import APIRouter

from backend.hosts.service import (
    register_host,
    list_hosts,
    update_host,
    remove_host,
    test_host_connectivity,
)

router = APIRouter()

@router.post("/test")
def test_host(payload: dict):
    return test_host_connectivity(payload["host"], payload["port"])

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

@router.put("/{host_id}")
def edit_host(
    host_id: int,
    payload: dict
):
    return update_host(
        host_id,
        payload["name"],
        payload["host"],
        payload["port"],
        payload.get("enabled", True)
    )

@router.delete("/{host_id}")
def delete_host(host_id: int):
    return remove_host(host_id)