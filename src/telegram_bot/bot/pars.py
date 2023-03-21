from . import errors


async def pars_function(function):
    async def wrapper(*args, **kwargs):
        try:
            return await function(*args, **kwargs)
        except KeyError as exc:
            message = f"couldn't find the field: {exc}"
            raise errors.ParserError(message=message)

    return wrapper()


def get_name_from_row_data(data: dict) -> str:
    return data["name"]

def get_description_from_row_data(data: dict) -> str:
    return data["description"]
