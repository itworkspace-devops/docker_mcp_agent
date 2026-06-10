from backend.agent.orchestrator import graph


def main():

    while True:

        query = input(
            "\nDocker Agent > "
        )

        if query.lower() in (
            "exit",
            "quit"
        ):
            break

        result = graph.invoke(
            {
                "query": query
            }
        )

        print(
            result["result"]
        )


if __name__ == "__main__":
    main()