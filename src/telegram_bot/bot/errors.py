import logging


class ParserError(Exception):
    def __init__(self, message: str) -> None:
        msg_error = message
        logging.error(msg_error)
