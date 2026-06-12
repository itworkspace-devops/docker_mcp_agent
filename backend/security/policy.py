from backend.security.roles import (
    ROLES
)


def is_allowed(
    role,
    tool_name,
):

    permissions = ROLES.get(
        role,
        []
    )

    if "*" in permissions:

        return True

    return (
        tool_name
        in
        permissions
    )