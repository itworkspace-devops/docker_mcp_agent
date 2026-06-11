from backend.config.settings import (
    settings
)


def request_approval(
    tool_name,
    tool_args,
):

    if settings.approval_mode == "cli":

        print()
        print("=" * 60)

        print(
            f"Action : {tool_name}"
        )

        print(
            f"Arguments : {tool_args}"
        )

        print()

        answer = input(
            "Approve? (y/n): "
        )

        return (
            answer.lower() == "y"
        )

    return False