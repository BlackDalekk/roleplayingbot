import logging


class UploadError(Exception):
    def __init__(self) -> None:
        msg_error = "Data could not be loaded into the database"
        logging.error(msg=msg_error)
