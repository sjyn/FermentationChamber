import time
import uuid

from Data import Database


class ChamberApi:
    database = Database.Database.getInstance()

    @classmethod
    def createItem(cls, itemName: str, fermentLengthMs: int) -> dict:
        body = {
            'id': str(uuid.uuid4()),
            'name': itemName,
            'ferment_for_ms': fermentLengthMs,
            'created_at': time.time()
        }
        cls.database.createItem(body)
        return body

    @classmethod
    def deleteItem(cls, itemId: str):
        cls.database.deleteItem(itemId)

    @classmethod
    def getItems(cls) -> [dict]:
        return cls.database.listItems()
