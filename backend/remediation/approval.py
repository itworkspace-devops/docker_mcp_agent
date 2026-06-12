from backend.config.settings import (
    settings
)


def approve_remediation(
    remediation
):

    if (
        settings.approval_mode
        ==
        "cli"
    ):

        print()
        print("=" * 80)

        print(
            "AUTO REMEDIATION REQUEST"
        )

        print(
            remediation["plan"]
        )

        answer = input(
            "Approve? (y/n): "
        )

        return (
            answer.lower()
            ==
            "y"
        )

    return False