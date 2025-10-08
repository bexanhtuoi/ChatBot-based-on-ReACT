from typing import List, Optional, TypeVar, Generic
from app.security import hash_password

CreateSchema = TypeVar("CreateSchema", bound=object)
ReadSchema = TypeVar("ReadSchema", bound=object)
UpdateSchema = TypeVar("UpdateSchema", bound=object)

class CRUDRepository():
    def __init__(
        self, collection, ReadSchema: ReadSchema, UpdateSchema: UpdateSchema
        ):
        self.collection = collection
        self.ReadSchema = ReadSchema
        self.UpdateSchema = UpdateSchema

    def create_one(self, obj_create: CreateSchema) ->  None:
        self.collection.insert_one(obj_create.dict())

    def get_many(self, skip: int = 0, limit: int = 10) -> List[Optional[ReadSchema]]:
        cursor = self.collection.find().skip(skip).limit(limit)
        return [self.ReadSchema(**obj) for obj in cursor]

    def get_one(self, obj_id: str) -> Optional[ReadSchema]:
        obj = self.collection.find_one({"id": obj_id})
        return self.ReadSchema(**obj) if obj else None

    def delete(self, obj_id: str) -> None:
        self.collection.delete_one({"id": obj_id})

    def update(self, obj_id: str, obj_data: UpdateSchema) -> None:
        update_data = {k: v for k, v in obj_data.dict().items() if v is not None}

        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data["password"])
            del update_data["password"]

        if update_data:
            print("Đây là data: ", update_data)
            self.collection.update_one({"id": obj_id}, {"$set": update_data})
            print("đã update")