from ninja import Schema
from pydantic import ConfigDict, alias_generators


class CamelCaseModel(Schema):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=alias_generators.to_camel,
    )
