def success(data):

    return {
        "success": True,
        "data": data,
        "error": None,
    }


def failure(error):

    return {
        "success": False,
        "data": None,
        "error": str(error),
    }