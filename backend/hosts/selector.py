def extract_host(
    query: str
):

    query = query.lower()

    if "prod" in query:
        return "prod"

    if "qa" in query:
        return "qa"

    if "dev" in query:
        return "dev"

    return "local"