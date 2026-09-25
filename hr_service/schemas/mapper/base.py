from typing import TypeVar

from pydantic import BaseModel

from hr_service.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None # noqa
    schema: type[SchemaType] = None # noqa

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