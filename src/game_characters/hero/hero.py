import logging

from src.game_characters.game_character.game_character import GameCharacter
from src.data_base.sqlite_db import HeroesDB
from . import errors

class Hero(GameCharacter):
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description)

    def get_short_info(self) -> dict:
        return {"name": self.name, "description": self.description}

    def uploading_to_database(self, user_id: int):
        data = {
            "name": self.name,
            "description": self.description,
        }

        logging.info(msg="Upload begins")
        try:
            HeroesDB.add_hero(user_id=user_id, data=data)
        except Exception:
            raise errors.UploadError()

        logging.info(msg="Uploaded successfully")
