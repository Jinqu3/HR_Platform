from typing import TypeVar

from hr_service.database import Base
from pydantic import BaseModel

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        """
        Превращает модель alchemy в pydantic схему
        :param data: db_model: Alchemy model
        :return: Pydantic scheme
        """
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        """
        Превращает pydantic схему в модель alchemy
        :param data: schema: Pydantic scheme
        :return:
        """
        return cls.db_model(**data.model_dump())