from backend.security.auth import (
    get_current_role
)

from backend.security.policy import (
    is_allowed
)


def authorization_node(state):

    role = get_current_role()

    tool_name = state["tool_name"]

    allowed = is_allowed(
        role,
        tool_name
    )

    if not allowed:

        return {

            "authorized": False,

            "result": {

                "success": False,

                "error":
                    f"Role '{role}' "
                    f"cannot execute "
                    f"'{tool_name}'"
            }
        }

    return {

        "authorized": True,

        "role": role,
    }